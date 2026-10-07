"""Validated immutable tag-mapping snapshots for AdvNFC."""

from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
import re
import tempfile
import threading
from types import MappingProxyType
from typing import Any

import yaml

SCHEMA_VERSION = 1
ADMIN_INTERFACE_ID = "advnfc.tag_mapping.administration"
ADMIN_INTERFACE_VERSION = 3
SUPPORTED_ACTION_TYPES = ("astv_intent",)
ADMIN_OPERATIONS = (
    "capabilities",
    "list",
    "get",
    "query",
    "status",
    "validate_document",
    "validate_record",
    "create",
    "update",
    "delete",
    "activate",
)
ROOT_FIELDS = frozenset({"tag_mapping_schema_version", "tags"})
TAG_FIELDS = frozenset({"label", "area_override", "action"})
ACTION_FIELDS = frozenset({"type", "intent_id"})
UID_PATTERN = re.compile(r"^[A-Z0-9]+$")
INTENT_ID_PATTERN = re.compile(r"^[a-z0-9]+(?:_[a-z0-9]+)*$")


class TagMappingValidationError(ValueError):
    """Raised when a candidate mapping does not satisfy schema v1."""

    def __init__(self, message: str, *, code: str = "invalid_candidate") -> None:
        super().__init__(message)
        self.code = code

    def administration_error(self) -> dict[str, str]:
        """Return the stable consumer-facing validation error shape."""

        return {"code": self.code, "message": str(self)}


class _UniqueKeyLoader(yaml.SafeLoader):
    """Safe YAML loader that rejects duplicate keys at every level."""


def _construct_unique_mapping(
    loader: _UniqueKeyLoader, node: yaml.MappingNode, deep: bool = False
) -> dict[Any, Any]:
    result: dict[Any, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in result:
            raise TagMappingValidationError(f"duplicate YAML key: {key!r}")
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


_UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    _construct_unique_mapping,
)


def _require_mapping(value: Any, location: str) -> Mapping[Any, Any]:
    if not isinstance(value, Mapping):
        raise TagMappingValidationError(f"{location} must be a mapping")
    return value


def _require_exact_fields(
    value: Mapping[Any, Any], expected: frozenset[str], location: str
) -> None:
    actual = set(value)
    unknown = actual - expected
    missing = expected - actual
    if unknown:
        raise TagMappingValidationError(
            f"{location} contains unknown fields: {sorted(unknown, key=str)}"
        )
    if missing:
        raise TagMappingValidationError(
            f"{location} is missing required fields: {sorted(missing)}"
        )


def _require_non_blank_string(value: Any, location: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise TagMappingValidationError(f"{location} must be a non-blank string")
    return value.strip()


def normalize_uid(value: object) -> str:
    """Normalize a runtime UID for exact lookup."""

    return str(value).strip().upper()


def normalize_intent_id(value: object) -> str:
    """Normalize an ASTV intent ID consistently with the provider boundary."""

    return str(value).strip().lower()


def parse_yaml_document(text: str) -> Mapping[str, Any]:
    """Parse a mapping document while rejecting duplicate YAML keys."""

    try:
        document = yaml.load(text, Loader=_UniqueKeyLoader)
    except TagMappingValidationError:
        raise
    except yaml.YAMLError as error:
        raise TagMappingValidationError(f"invalid YAML: {error}") from error
    return _require_mapping(document, "document")


def validate_document(
    document: Mapping[str, Any], area_exists: Callable[[str], bool]
) -> Mapping[str, Mapping[str, Any]]:
    """Validate and normalize one closed schema-v1 mapping document."""

    _require_exact_fields(document, ROOT_FIELDS, "document root")
    version = document["tag_mapping_schema_version"]
    if type(version) is not int or version != SCHEMA_VERSION:
        raise TagMappingValidationError(
            f"tag_mapping_schema_version must be integer {SCHEMA_VERSION}"
        )

    tags = _require_mapping(document["tags"], "tags")
    normalized_tags: dict[str, Mapping[str, Any]] = {}
    for raw_uid, raw_record in tags.items():
        if not isinstance(raw_uid, str):
            raise TagMappingValidationError("stored UID keys must be strings")
        uid = raw_uid.strip()
        if uid != raw_uid or uid != uid.upper() or not UID_PATTERN.fullmatch(uid):
            raise TagMappingValidationError(
                f"stored UID {raw_uid!r} must already be canonical uppercase"
            )
        if uid in normalized_tags:
            raise TagMappingValidationError(f"duplicate UID: {uid}")

        record = _require_mapping(raw_record, f"tags.{uid}")
        required_tag_fields = TAG_FIELDS - {"area_override"}
        actual_tag_fields = set(record)
        unknown_tag_fields = actual_tag_fields - TAG_FIELDS
        missing_tag_fields = required_tag_fields - actual_tag_fields
        if unknown_tag_fields:
            raise TagMappingValidationError(
                f"tags.{uid} contains unknown fields: "
                f"{sorted(unknown_tag_fields, key=str)}"
            )
        if missing_tag_fields:
            raise TagMappingValidationError(
                f"tags.{uid} is missing required fields: {sorted(missing_tag_fields)}"
            )

        label = _require_non_blank_string(record["label"], f"tags.{uid}.label")
        normalized_record: dict[str, Any] = {"uid": uid, "label": label}

        if "area_override" in record:
            area_override = _require_non_blank_string(
                record["area_override"], f"tags.{uid}.area_override"
            )
            if not area_exists(area_override):
                raise TagMappingValidationError(
                    f"tags.{uid}.area_override does not resolve: {area_override}"
                )
            normalized_record["area_override"] = area_override

        action = _require_mapping(record["action"], f"tags.{uid}.action")
        _require_exact_fields(action, ACTION_FIELDS, f"tags.{uid}.action")
        action_type = _require_non_blank_string(
            action["type"], f"tags.{uid}.action.type"
        )
        if action_type not in SUPPORTED_ACTION_TYPES:
            raise TagMappingValidationError(
                f"tags.{uid}.action.type is unsupported: {action_type}"
            )
        intent_id = normalize_intent_id(
            _require_non_blank_string(
                action["intent_id"], f"tags.{uid}.action.intent_id"
            )
        )
        if not INTENT_ID_PATTERN.fullmatch(intent_id):
            raise TagMappingValidationError(
                f"tags.{uid}.action.intent_id is structurally invalid: {intent_id}"
            )
        normalized_record["action"] = MappingProxyType(
            {"type": action_type, "intent_id": intent_id}
        )
        normalized_tags[uid] = MappingProxyType(normalized_record)

    return MappingProxyType(normalized_tags)


def _plain_record(record: Mapping[str, Any]) -> dict[str, Any]:
    result: dict[str, Any] = {
        "uid": record["uid"],
        "label": record["label"],
        "action": dict(record["action"]),
    }
    if "area_override" in record:
        result["area_override"] = record["area_override"]
    return result


def _revision_for_tags(tags: Mapping[str, Mapping[str, Any]]) -> str:
    canonical = [_plain_record(tags[uid]) for uid in sorted(tags)]
    payload = json.dumps(
        {"tag_mapping_schema_version": SCHEMA_VERSION, "mappings": canonical},
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    ).encode("utf-8")
    return f"v1-{hashlib.sha256(payload).hexdigest()}"


def _stored_document(tags: Mapping[str, Mapping[str, Any]]) -> dict[str, Any]:
    stored_tags: dict[str, Any] = {}
    for uid in sorted(tags):
        record = tags[uid]
        stored_record: dict[str, Any] = {"label": record["label"]}
        if "area_override" in record:
            stored_record["area_override"] = record["area_override"]
        stored_record["action"] = dict(record["action"])
        stored_tags[uid] = stored_record
    return {"tag_mapping_schema_version": SCHEMA_VERSION, "tags": stored_tags}


def _candidate_document_from_records(candidate: Mapping[str, Any]) -> Mapping[str, Any]:
    _require_exact_fields(
        candidate,
        frozenset({"tag_mapping_schema_version", "mappings"}),
        "candidate",
    )
    version = candidate["tag_mapping_schema_version"]
    if type(version) is not int or version != SCHEMA_VERSION:
        raise TagMappingValidationError(
            f"tag_mapping_schema_version must be integer {SCHEMA_VERSION}"
        )
    mappings = candidate["mappings"]
    if not isinstance(mappings, list):
        raise TagMappingValidationError("candidate.mappings must be a list")

    tags: dict[str, Any] = {}
    for index, value in enumerate(mappings):
        record = _require_mapping(value, f"candidate.mappings[{index}]")
        required = frozenset({"uid", "label", "action"})
        allowed = required | {"area_override"}
        actual = set(record)
        unknown = actual - allowed
        missing = required - actual
        if unknown:
            raise TagMappingValidationError(
                f"candidate.mappings[{index}] contains unknown fields: "
                f"{sorted(unknown, key=str)}"
            )
        if missing:
            raise TagMappingValidationError(
                f"candidate.mappings[{index}] is missing required fields: "
                f"{sorted(missing)}"
            )

        uid = normalize_uid(record["uid"])
        if not uid or not UID_PATTERN.fullmatch(uid):
            raise TagMappingValidationError(
                f"candidate.mappings[{index}].uid must normalize to a non-blank "
                "alphanumeric value"
            )
        if uid in tags:
            raise TagMappingValidationError(
                f"candidate contains duplicate normalized UID: {uid}",
                code="duplicate_uid",
            )

        stored_record: dict[str, Any] = {
            "label": _require_non_blank_string(
                record["label"], f"candidate.mappings[{index}].label"
            )
        }
        if "area_override" in record:
            stored_record["area_override"] = _require_non_blank_string(
                record["area_override"],
                f"candidate.mappings[{index}].area_override",
            )
        action = _require_mapping(
            record["action"], f"candidate.mappings[{index}].action"
        )
        _require_exact_fields(
            action,
            ACTION_FIELDS,
            f"candidate.mappings[{index}].action",
        )
        stored_record["action"] = {
            "type": _require_non_blank_string(
                action["type"], f"candidate.mappings[{index}].action.type"
            ).lower(),
            "intent_id": normalize_intent_id(
                _require_non_blank_string(
                    action["intent_id"],
                    f"candidate.mappings[{index}].action.intent_id",
                )
            ),
        }
        tags[uid] = stored_record
    return {"tag_mapping_schema_version": SCHEMA_VERSION, "tags": tags}


def validate_administration_candidate(
    candidate: Mapping[str, Any], area_exists: Callable[[str], bool]
) -> Mapping[str, Mapping[str, Any]]:
    """Validate normalized administration records against stored schema v1."""

    return validate_document(_candidate_document_from_records(candidate), area_exists)


def serialize_document(tags: Mapping[str, Mapping[str, Any]]) -> str:
    """Serialize validated tags to the sole authoritative stored representation."""

    return yaml.safe_dump(
        _stored_document(tags),
        sort_keys=False,
        allow_unicode=True,
        default_flow_style=False,
    )


def _atomic_write_text(path: Path, text: str) -> None:
    """Replace a mapping file atomically without exposing a partial candidate."""

    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            newline="\n",
            dir=path.parent,
            prefix=f".{path.name}.",
            suffix=".tmp",
            delete=False,
        ) as temporary:
            temporary.write(text)
            temporary.flush()
            os.fsync(temporary.fileno())
            temporary_path = Path(temporary.name)
        os.replace(temporary_path, path)
        temporary_path = None
    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)


@dataclass(frozen=True, slots=True)
class TagMappingSnapshot:
    """One immutable, fully validated active mapping snapshot."""

    schema_version: int
    tags: Mapping[str, Mapping[str, Any]]
    revision: str = ""

    def __post_init__(self) -> None:
        if not self.revision:
            object.__setattr__(self, "revision", _revision_for_tags(self.tags))

    @property
    def count(self) -> int:
        return len(self.tags)

    def _serialize_record(self, record: Mapping[str, Any]) -> dict[str, Any]:
        return _plain_record(record)

    def _administration_base(self) -> dict[str, Any]:
        return {
            "interface_id": ADMIN_INTERFACE_ID,
            "interface_version": ADMIN_INTERFACE_VERSION,
            "tag_mapping_schema_version": self.schema_version,
            "revision": self.revision,
        }

    def _administration_error(
        self, code: str, message: str, **context: Any
    ) -> dict[str, Any]:
        return {
            **self._administration_base(),
            "ok": False,
            **context,
            "error": {"code": code, "message": message},
        }

    def find(self, uid: object) -> dict[str, Any]:
        record = self.tags.get(normalize_uid(uid))
        return {} if record is None else self._serialize_record(record)

    def administration_capabilities(self) -> dict[str, Any]:
        return {
            **self._administration_base(),
            "ok": True,
            "supported_action_types": list(SUPPORTED_ACTION_TYPES),
            "operations": list(ADMIN_OPERATIONS),
        }

    def administration_list(self) -> dict[str, Any]:
        mappings = [
            self._serialize_record(self.tags[uid]) for uid in sorted(self.tags)
        ]
        return {
            **self._administration_base(),
            "ok": True,
            "count": len(mappings),
            "mappings": mappings,
        }

    def administration_get(self, uid: object) -> dict[str, Any]:
        canonical_uid = normalize_uid(uid)
        query = {"uid": canonical_uid}
        if not canonical_uid or not UID_PATTERN.fullmatch(canonical_uid):
            return self._administration_error(
                "invalid_query",
                "uid must normalize to a non-blank alphanumeric value",
                query=query,
            )
        record = self.tags.get(canonical_uid)
        if record is None:
            return self._administration_error(
                "not_found",
                f"no active mapping exists for UID {canonical_uid}",
                query=query,
            )
        return {
            **self._administration_base(),
            "ok": True,
            "query": query,
            "mapping": self._serialize_record(record),
        }

    def administration_query(
        self, action_type: object, intent_id: object
    ) -> dict[str, Any]:
        normalized_action_type = str(action_type).strip().lower()
        normalized_intent_id = normalize_intent_id(intent_id)
        query = {
            "action": {
                "type": normalized_action_type,
                "intent_id": normalized_intent_id,
            }
        }
        if normalized_action_type not in SUPPORTED_ACTION_TYPES:
            return self._administration_error(
                "invalid_query",
                f"unsupported action_type: {normalized_action_type or '<blank>'}",
                query=query,
            )
        if not normalized_intent_id or not INTENT_ID_PATTERN.fullmatch(
            normalized_intent_id
        ):
            return self._administration_error(
                "invalid_query",
                "intent_id must normalize to lowercase underscore identifier form",
                query=query,
            )
        matches = [
            self._serialize_record(self.tags[uid])
            for uid in sorted(self.tags)
            if self.tags[uid]["action"]["type"] == normalized_action_type
            and self.tags[uid]["action"]["intent_id"] == normalized_intent_id
        ]
        return {
            **self._administration_base(),
            "ok": True,
            "query": query,
            "count": len(matches),
            "mappings": matches,
        }


class TagMappingStore:
    """Own the active snapshot and atomically replace it after validation."""

    def __init__(self) -> None:
        self._active: TagMappingSnapshot | None = None
        self._persisted_revision: str | None = None
        self._last_activation_error: dict[str, str] | None = None
        self._write_lock = threading.Lock()

    @property
    def active(self) -> TagMappingSnapshot | None:
        return self._active

    @property
    def persisted_revision(self) -> str | None:
        """Return the most recently verified persisted revision."""

        return self._persisted_revision

    @property
    def activation_required(self) -> bool:
        """Return whether verified persisted state differs from active state."""

        active_revision = None if self._active is None else self._active.revision
        return active_revision != self._persisted_revision

    @property
    def last_activation_error(self) -> dict[str, str] | None:
        """Return the last managed activation failure, if any."""

        return (
            None
            if self._last_activation_error is None
            else dict(self._last_activation_error)
        )

    def load_and_activate(
        self, path: Path, area_exists: Callable[[str], bool]
    ) -> TagMappingSnapshot:
        with self._write_lock:
            candidate = self._persisted_snapshot(path, area_exists)
            self._active = candidate
            self._persisted_revision = candidate.revision
            self._last_activation_error = None
            return candidate

    def find(self, uid: object) -> dict[str, Any]:
        if self._active is None:
            return {}
        return self._active.find(uid)

    def _active_snapshot(self) -> TagMappingSnapshot:
        if self._active is None:
            raise RuntimeError("AdvNFC tag mapping has not been activated")
        return self._active

    def administration_capabilities(self) -> dict[str, Any]:
        return self._with_state(
            self._active_snapshot().administration_capabilities()
        )

    def administration_list(self) -> dict[str, Any]:
        return self._with_state(self._active_snapshot().administration_list())

    def administration_get(self, uid: object) -> dict[str, Any]:
        return self._with_state(self._active_snapshot().administration_get(uid))

    def administration_query(
        self, action_type: object, intent_id: object
    ) -> dict[str, Any]:
        return self._with_state(
            self._active_snapshot().administration_query(action_type, intent_id)
        )

    def _with_state(self, response: dict[str, Any]) -> dict[str, Any]:
        """Add the manager-facing active/persisted state to a response."""

        active = self._active
        active_revision = None if active is None else active.revision
        return {
            **response,
            "active_revision": active_revision,
            "persisted_revision": self._persisted_revision,
            "activation_required": (
                active_revision != self._persisted_revision
            ),
        }

    def _base_response(self, **values: Any) -> dict[str, Any]:
        active = self._active
        active_revision = None if active is None else active.revision
        return {
            "interface_id": ADMIN_INTERFACE_ID,
            "interface_version": ADMIN_INTERFACE_VERSION,
            "tag_mapping_schema_version": SCHEMA_VERSION,
            "active_revision": active_revision,
            "persisted_revision": self._persisted_revision,
            "activation_required": active_revision != self._persisted_revision,
            **values,
        }

    def _validation_failure(self, error: TagMappingValidationError) -> dict[str, Any]:
        return self._base_response(ok=False, error=error.administration_error())

    def administration_validate_document(
        self,
        candidate: object,
        area_exists: Callable[[str], bool],
    ) -> dict[str, Any]:
        try:
            candidate_mapping = _require_mapping(candidate, "candidate")
            tags = validate_administration_candidate(candidate_mapping, area_exists)
        except TagMappingValidationError as error:
            return self._validation_failure(error)
        snapshot = TagMappingSnapshot(SCHEMA_VERSION, tags)
        return self._base_response(
            ok=True,
            revision=snapshot.revision,
            count=snapshot.count,
            mappings=[_plain_record(tags[uid]) for uid in sorted(tags)],
        )

    def administration_validate_record(
        self,
        record: object,
        area_exists: Callable[[str], bool],
    ) -> dict[str, Any]:
        candidate = {
            "tag_mapping_schema_version": SCHEMA_VERSION,
            "mappings": [record],
        }
        response = self.administration_validate_document(candidate, area_exists)
        if response["ok"]:
            response["mapping"] = response.pop("mappings")[0]
            response.pop("count")
        return response

    def _persisted_snapshot(
        self, path: Path, area_exists: Callable[[str], bool]
    ) -> TagMappingSnapshot:
        document = parse_yaml_document(path.read_text(encoding="utf-8"))
        return TagMappingSnapshot(
            SCHEMA_VERSION,
            validate_document(document, area_exists),
        )

    def administration_status(
        self, path: Path, area_exists: Callable[[str], bool]
    ) -> dict[str, Any]:
        """Report the verified persisted candidate and active snapshot state."""

        with self._write_lock:
            try:
                persisted = self._persisted_snapshot(path, area_exists)
            except TagMappingValidationError as error:
                self._persisted_revision = None
                return self._base_response(
                    ok=False,
                    state="persisted_invalid",
                    last_activation_error=self._last_activation_error,
                    error=error.administration_error(),
                )
            except OSError:
                self._persisted_revision = None
                return self._base_response(
                    ok=False,
                    state="persisted_unavailable",
                    last_activation_error=self._last_activation_error,
                    error={
                        "code": "persisted_state_unavailable",
                        "message": (
                            "the authoritative persisted mapping could not be read"
                        ),
                    },
                )

            self._persisted_revision = persisted.revision
            return self._base_response(
                ok=True,
                state=(
                    "active"
                    if self._active is not None
                    and self._active.revision == persisted.revision
                    else "activation_required"
                ),
                active_count=0 if self._active is None else self._active.count,
                persisted_count=persisted.count,
                last_activation_error=self._last_activation_error,
            )

    def administration_activate(
        self, path: Path, area_exists: Callable[[str], bool]
    ) -> dict[str, Any]:
        """Validate and atomically activate the complete persisted candidate."""

        with self._write_lock:
            try:
                candidate = self._persisted_snapshot(path, area_exists)
            except TagMappingValidationError as error:
                self._persisted_revision = None
                self._last_activation_error = error.administration_error()
                return self._base_response(
                    ok=False,
                    operation="activate",
                    state="persisted_invalid",
                    error=self._last_activation_error,
                )
            except OSError:
                self._persisted_revision = None
                self._last_activation_error = {
                    "code": "persisted_state_unavailable",
                    "message": "the authoritative persisted mapping could not be read",
                }
                return self._base_response(
                    ok=False,
                    operation="activate",
                    state="persisted_unavailable",
                    error=self._last_activation_error,
                )

            self._persisted_revision = candidate.revision
            self._active = candidate
            self._last_activation_error = None
            return self._base_response(
                ok=True,
                operation="activate",
                state="active",
                count=candidate.count,
            )

    def _mutation_error(self, code: str, message: str, **values: Any) -> dict[str, Any]:
        return self._base_response(
            ok=False,
            **values,
            error={"code": code, "message": message},
        )

    def _mutate(
        self,
        operation: str,
        path: Path,
        expected_revision: object,
        area_exists: Callable[[str], bool],
        *,
        record: object | None = None,
        uid: object = "",
    ) -> dict[str, Any]:
        with self._write_lock:
            try:
                persisted = self._persisted_snapshot(path, area_exists)
            except (OSError, TagMappingValidationError):
                return self._mutation_error(
                    "persisted_state_unavailable",
                    "the authoritative persisted mapping could not be validated",
                )

            self._persisted_revision = persisted.revision

            expected = str(expected_revision).strip()
            if not expected or expected != persisted.revision:
                return self._mutation_error(
                    "stale_revision",
                    "the persisted mapping changed after the consumer read it",
                    persisted_revision=persisted.revision,
                )

            candidate_records = {
                key: _plain_record(value) for key, value in persisted.tags.items()
            }
            result_values: dict[str, Any]
            if operation in {"create", "update"}:
                validation = self.administration_validate_record(record, area_exists)
                if not validation["ok"]:
                    return validation
                normalized = validation["mapping"]
                canonical_uid = normalized["uid"]
                exists = canonical_uid in candidate_records
                if operation == "create" and exists:
                    return self._mutation_error(
                        "already_exists",
                        f"a persisted mapping already exists for UID {canonical_uid}",
                        persisted_revision=persisted.revision,
                    )
                if operation == "update" and not exists:
                    return self._mutation_error(
                        "not_found",
                        f"no persisted mapping exists for UID {canonical_uid}",
                        persisted_revision=persisted.revision,
                    )
                candidate_records[canonical_uid] = normalized
                result_values = {"mapping": normalized}
            else:
                canonical_uid = normalize_uid(uid)
                if not canonical_uid or not UID_PATTERN.fullmatch(canonical_uid):
                    return self._mutation_error(
                        "invalid_candidate",
                        "uid must normalize to a non-blank alphanumeric value",
                        persisted_revision=persisted.revision,
                    )
                if canonical_uid not in candidate_records:
                    return self._mutation_error(
                        "not_found",
                        f"no persisted mapping exists for UID {canonical_uid}",
                        persisted_revision=persisted.revision,
                    )
                del candidate_records[canonical_uid]
                result_values = {"uid": canonical_uid}

            complete_candidate = {
                "tag_mapping_schema_version": SCHEMA_VERSION,
                "mappings": list(candidate_records.values()),
            }
            try:
                candidate_tags = validate_administration_candidate(
                    complete_candidate, area_exists
                )
                candidate = TagMappingSnapshot(SCHEMA_VERSION, candidate_tags)
                _atomic_write_text(path, serialize_document(candidate.tags))
            except TagMappingValidationError as error:
                return self._validation_failure(error)
            except OSError:
                return self._mutation_error(
                    "atomic_write_failed",
                    "the persisted mapping was not replaced",
                    persisted_revision=persisted.revision,
                )

            self._persisted_revision = candidate.revision
            return self._base_response(
                ok=True,
                operation=operation,
                **result_values,
            )

    def administration_create(
        self,
        path: Path,
        expected_revision: object,
        record: object,
        area_exists: Callable[[str], bool],
    ) -> dict[str, Any]:
        return self._mutate(
            "create", path, expected_revision, area_exists, record=record
        )

    def administration_update(
        self,
        path: Path,
        expected_revision: object,
        record: object,
        area_exists: Callable[[str], bool],
    ) -> dict[str, Any]:
        return self._mutate(
            "update", path, expected_revision, area_exists, record=record
        )

    def administration_delete(
        self,
        path: Path,
        expected_revision: object,
        uid: object,
        area_exists: Callable[[str], bool],
    ) -> dict[str, Any]:
        return self._mutate(
            "delete", path, expected_revision, area_exists, uid=uid
        )
