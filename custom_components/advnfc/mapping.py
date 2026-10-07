"""Validated immutable tag-mapping snapshots for AdvNFC."""

from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass
from pathlib import Path
import re
from types import MappingProxyType
from typing import Any

import yaml

SCHEMA_VERSION = 1
ADMIN_INTERFACE_ID = "advnfc.tag_mapping.administration"
ADMIN_INTERFACE_VERSION = 1
SUPPORTED_ACTION_TYPES = ("astv_intent",)
ADMIN_OPERATIONS = ("capabilities", "list", "get", "query")
ROOT_FIELDS = frozenset({"tag_mapping_schema_version", "tags"})
TAG_FIELDS = frozenset({"label", "area_override", "action"})
ACTION_FIELDS = frozenset({"type", "intent_id"})
UID_PATTERN = re.compile(r"^[A-Z0-9]+$")
INTENT_ID_PATTERN = re.compile(r"^[a-z0-9]+(?:_[a-z0-9]+)*$")


class TagMappingValidationError(ValueError):
    """Raised when a candidate mapping does not satisfy schema v1."""


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


@dataclass(frozen=True, slots=True)
class TagMappingSnapshot:
    """One immutable, fully validated active mapping snapshot."""

    schema_version: int
    tags: Mapping[str, Mapping[str, Any]]

    @property
    def count(self) -> int:
        return len(self.tags)

    def _serialize_record(self, record: Mapping[str, Any]) -> dict[str, Any]:
        response: dict[str, Any] = {
            "uid": record["uid"],
            "label": record["label"],
            "action": dict(record["action"]),
        }
        if "area_override" in record:
            response["area_override"] = record["area_override"]
        return response

    def _administration_base(self) -> dict[str, Any]:
        return {
            "interface_id": ADMIN_INTERFACE_ID,
            "interface_version": ADMIN_INTERFACE_VERSION,
            "tag_mapping_schema_version": self.schema_version,
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

    @property
    def active(self) -> TagMappingSnapshot | None:
        return self._active

    def load_and_activate(
        self, path: Path, area_exists: Callable[[str], bool]
    ) -> TagMappingSnapshot:
        document = parse_yaml_document(path.read_text(encoding="utf-8"))
        tags = validate_document(document, area_exists)
        candidate = TagMappingSnapshot(schema_version=SCHEMA_VERSION, tags=tags)
        self._active = candidate
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
        return self._active_snapshot().administration_capabilities()

    def administration_list(self) -> dict[str, Any]:
        return self._active_snapshot().administration_list()

    def administration_get(self, uid: object) -> dict[str, Any]:
        return self._active_snapshot().administration_get(uid)

    def administration_query(
        self, action_type: object, intent_id: object
    ) -> dict[str, Any]:
        return self._active_snapshot().administration_query(action_type, intent_id)
