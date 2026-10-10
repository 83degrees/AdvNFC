"""Provider-boundary authorization tests for AdvNFC services."""

from __future__ import annotations

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import sys
from types import ModuleType, SimpleNamespace
import unittest


ROOT = Path(__file__).resolve().parents[1]
MODULE_NAME = "custom_components.advnfc"
STUBBED_MODULES = (
    "homeassistant",
    "homeassistant.const",
    "homeassistant.core",
    "homeassistant.helpers",
    "homeassistant.helpers.area_registry",
    "homeassistant.helpers.discovery",
    "homeassistant.helpers.dispatcher",
    "homeassistant.helpers.service",
    "homeassistant.helpers.typing",
    "custom_components",
    MODULE_NAME,
    f"{MODULE_NAME}.mapping",
)


class Unauthorized(Exception):
    """Stand in for Home Assistant's platform authorization failure."""


class UnknownUser(Exception):
    """Stand in for Home Assistant's unknown-user failure."""


class FakeTagMappingValidationError(Exception):
    """Stand in for the provider validation error used during setup."""


class FakeStore:
    """Record whether a provider handler crossed the authorization boundary."""

    latest: FakeStore | None = None

    def __init__(self) -> None:
        self.calls: list[str] = []
        FakeStore.latest = self

    def _response(self, operation: str) -> dict:
        self.calls.append(operation)
        return {"ok": True, "operation": operation}

    def load_and_activate(self, path, area_exists) -> None:
        self.calls.append("initial_load")

    def find(self, uid: str) -> dict:
        return self._response("find")

    def administration_capabilities(self) -> dict:
        return self._response("capabilities")

    def administration_list(self) -> dict:
        return self._response("list")

    def administration_status(self, path, area_exists) -> dict:
        return self._response("status")

    def administration_get(self, uid: str) -> dict:
        return self._response("get")

    def administration_query(self, action_type: str, intent_id: str) -> dict:
        return self._response("query")

    def administration_validate_document(self, candidate, area_exists) -> dict:
        return self._response("validate_document")

    def administration_validate_record(self, record, area_exists) -> dict:
        return self._response("validate_record")

    def administration_create(self, path, revision, record, area_exists) -> dict:
        return self._response("create")

    def administration_update(self, path, revision, record, area_exists) -> dict:
        return self._response("update")

    def administration_delete(self, path, revision, uid, area_exists) -> dict:
        return self._response("delete")

    def administration_activate(self, path, area_exists) -> dict:
        return self._response("activate")


class FakeServices:
    def __init__(self) -> None:
        self.handlers: dict[str, object] = {}

    def async_register(
        self,
        domain,
        service,
        handler,
        schema=None,
        supports_response=None,
        **kwargs,
    ) -> None:
        self.handlers[service] = handler


class FakeAuth:
    async def async_get_user(self, user_id: str):
        if user_id == "admin":
            return SimpleNamespace(is_admin=True)
        if user_id == "member":
            return SimpleNamespace(is_admin=False)
        return None


class FakeHass:
    def __init__(self) -> None:
        self.data: dict = {}
        self.services = FakeServices()
        self.auth = FakeAuth()
        self.admin_services: set[str] = set()
        self.path_reads: list[tuple[str, ...]] = []
        self.area_registry_reads = 0
        self.config = SimpleNamespace(path=self._path)

    def _path(self, *parts: str) -> str:
        self.path_reads.append(parts)
        return str(ROOT.joinpath(*parts))

    async def async_add_executor_job(self, target, *args):
        return target(*args)

    def async_create_task(self, coroutine) -> None:
        coroutine.close()


def _install_module(name: str, **attributes) -> ModuleType:
    module = ModuleType(name)
    for key, value in attributes.items():
        setattr(module, key, value)
    sys.modules[name] = module
    return module


def _load_integration():
    """Load the integration against a focused Home Assistant service double."""

    class SupportsResponse:
        ONLY = "only"

    class Platform:
        SENSOR = "sensor"

    _install_module("homeassistant", __path__=[])
    _install_module("homeassistant.const", Platform=Platform)
    _install_module(
        "homeassistant.core",
        HomeAssistant=FakeHass,
        ServiceCall=object,
        ServiceResponse=dict,
        SupportsResponse=SupportsResponse,
    )
    helpers = _install_module("homeassistant.helpers", __path__=[])

    area_registry = _install_module("homeassistant.helpers.area_registry")

    def async_get(hass):
        hass.area_registry_reads += 1
        return SimpleNamespace(async_list_areas=lambda: [])

    area_registry.async_get = async_get
    helpers.area_registry = area_registry

    discovery = _install_module("homeassistant.helpers.discovery")

    async def async_load_platform(*args, **kwargs):
        return None

    discovery.async_load_platform = async_load_platform
    helpers.discovery = discovery
    _install_module(
        "homeassistant.helpers.dispatcher", async_dispatcher_send=lambda *args: None
    )
    _install_module("homeassistant.helpers.typing", ConfigType=dict)

    service = _install_module("homeassistant.helpers.service")

    def async_register_admin_service(
        hass,
        domain,
        service_name,
        handler,
        schema=None,
        supports_response=None,
        **kwargs,
    ) -> None:
        """Mirror Home Assistant's user/admin/system dispatch semantics."""

        async def admin_handler(call):
            if call.context.user_id:
                user = await hass.auth.async_get_user(call.context.user_id)
                if user is None:
                    raise UnknownUser(call.context.user_id)
                if not user.is_admin:
                    raise Unauthorized(call.context.user_id)
            return await handler(call)

        hass.admin_services.add(service_name)
        hass.services.async_register(
            domain,
            service_name,
            admin_handler,
            schema,
            supports_response=supports_response,
            **kwargs,
        )

    service.async_register_admin_service = async_register_admin_service

    custom_components = _install_module(
        "custom_components", __path__=[str(ROOT / "custom_components")]
    )
    mapping_module = _install_module(
        f"{MODULE_NAME}.mapping",
        TagMappingStore=FakeStore,
        TagMappingValidationError=FakeTagMappingValidationError,
    )
    custom_components.mapping = mapping_module

    path = ROOT / "custom_components" / "advnfc" / "__init__.py"
    spec = spec_from_file_location(
        MODULE_NAME,
        path,
        submodule_search_locations=[str(path.parent)],
    )
    assert spec is not None and spec.loader is not None
    module = module_from_spec(spec)
    sys.modules[MODULE_NAME] = module
    spec.loader.exec_module(module)
    return module


def _call(user_id: str | None, **data):
    return SimpleNamespace(
        context=SimpleNamespace(user_id=user_id),
        data=data,
    )


def _run(coroutine):
    """Run a coroutine whose focused test doubles complete without yielding."""

    try:
        coroutine.send(None)
    except StopIteration as completed:
        return completed.value
    raise AssertionError("authorization test double unexpectedly yielded")


class AdvNfcAuthorizationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.saved_modules = {
            name: sys.modules[name] for name in STUBBED_MODULES if name in sys.modules
        }
        self.integration = _load_integration()
        self.hass = FakeHass()
        self.assertTrue(_run(self.integration.async_setup(self.hass, {})))
        assert FakeStore.latest is not None
        self.store = FakeStore.latest
        self.store.calls.clear()

    def tearDown(self) -> None:
        for name in STUBBED_MODULES:
            sys.modules.pop(name, None)
        sys.modules.update(self.saved_modules)

    def test_service_registration_separates_runtime_read_and_manage(self):
        self.assertEqual(
            self.hass.admin_services,
            {
                "reload_tag_mapping",
                "validate_tag_mapping",
                "validate_tag_mapping_record",
                "create_tag_mapping",
                "update_tag_mapping",
                "delete_tag_mapping",
            },
        )
        self.assertTrue(
            {
                "find_tag_record",
                "get_administration_capabilities",
                "get_administration_status",
                "list_tag_mappings",
                "get_tag_mapping",
                "query_tag_mappings",
            }.isdisjoint(self.hass.admin_services)
        )

    def test_non_admin_and_unknown_users_are_rejected_before_provider_access(self):
        baseline_paths = list(self.hass.path_reads)
        baseline_area_reads = self.hass.area_registry_reads
        for service_name in sorted(self.hass.admin_services):
            with self.subTest(service=service_name):
                with self.assertRaises(Unauthorized):
                    _run(
                        self.hass.services.handlers[service_name](
                            _call("member", candidate={}, mapping={})
                        )
                    )
        with self.assertRaises(UnknownUser):
            _run(
                self.hass.services.handlers["validate_tag_mapping"](
                    _call("missing", candidate={})
                )
            )
        self.assertEqual(self.store.calls, [])
        self.assertEqual(self.hass.path_reads, baseline_paths)
        self.assertEqual(self.hass.area_registry_reads, baseline_area_reads)

    def test_admin_and_system_context_manage_calls_reach_provider(self):
        admin_response = _run(
            self.hass.services.handlers["validate_tag_mapping_record"](
                _call("admin", mapping={})
            )
        )
        system_response = _run(
            self.hass.services.handlers["reload_tag_mapping"](_call(None))
        )
        self.assertEqual(admin_response["operation"], "validate_record")
        self.assertEqual(system_response["operation"], "activate")
        self.assertEqual(self.store.calls, ["validate_record", "activate"])

    def test_non_admin_read_and_runtime_calls_remain_available(self):
        read_response = _run(
            self.hass.services.handlers["list_tag_mappings"](_call("member"))
        )
        runtime_response = _run(
            self.hass.services.handlers["find_tag_record"](
                _call("member", uid="A1")
            )
        )
        self.assertEqual(read_response["operation"], "list")
        self.assertEqual(runtime_response["operation"], "find")


if __name__ == "__main__":
    unittest.main()
