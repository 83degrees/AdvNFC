"""Focused registration tests for the AdvNFC Home Assistant panel."""

from __future__ import annotations

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import sys
from types import ModuleType


ROOT = Path(__file__).resolve().parents[1]
MODULE_NAME = "custom_components.advnfc.panel"
STUBBED_MODULES = (
    "homeassistant",
    "homeassistant.components",
    "homeassistant.components.frontend",
    "homeassistant.components.http",
    "homeassistant.components.panel_custom",
    "homeassistant.core",
    "custom_components",
    "custom_components.advnfc",
    MODULE_NAME,
)


def _install_module(name: str, **attributes) -> ModuleType:
    module = ModuleType(name)
    for key, value in attributes.items():
        setattr(module, key, value)
    sys.modules[name] = module
    return module


def _load_panel():
    _install_module("homeassistant", __path__=[])
    components = _install_module("homeassistant.components", __path__=[])
    frontend = _install_module("homeassistant.components.frontend")
    http = _install_module("homeassistant.components.http")
    panel_custom = _install_module("homeassistant.components.panel_custom")
    _install_module("homeassistant.core", HomeAssistant=object)

    class StaticPathConfig:
        def __init__(self, url_path, path, cache_headers=True):
            self.url_path = url_path
            self.path = path
            self.cache_headers = cache_headers

    frontend.async_panel_exists = lambda hass, url_path: url_path in hass.panels
    http.StaticPathConfig = StaticPathConfig

    async def async_register_panel(hass, **kwargs):
        hass.panels[kwargs["frontend_url_path"]] = kwargs

    panel_custom.async_register_panel = async_register_panel
    components.frontend = frontend
    components.http = http
    components.panel_custom = panel_custom

    _install_module("custom_components", __path__=[str(ROOT / "custom_components")])
    _install_module(
        "custom_components.advnfc",
        __path__=[str(ROOT / "custom_components" / "advnfc")],
    )
    path = ROOT / "custom_components" / "advnfc" / "panel.py"
    spec = spec_from_file_location(MODULE_NAME, path)
    assert spec is not None and spec.loader is not None
    module = module_from_spec(spec)
    sys.modules[MODULE_NAME] = module
    spec.loader.exec_module(module)
    return module


class FakeHttp:
    def __init__(self) -> None:
        self.paths = []

    async def async_register_static_paths(self, paths) -> None:
        self.paths.extend(paths)


class FakeHass:
    def __init__(self) -> None:
        self.panels = {}
        self.http = FakeHttp()

    async def async_add_executor_job(self, target, *args):
        return target(*args)


def _run(coroutine):
    try:
        coroutine.send(None)
    except StopIteration as completed:
        return completed.value
    raise AssertionError("panel test double unexpectedly yielded")


def test_panel_is_digest_addressed_non_iframe_and_read_visible():
    saved = {name: sys.modules[name] for name in STUBBED_MODULES if name in sys.modules}
    try:
        panel = _load_panel()
        hass = FakeHass()
        _run(panel.async_register_frontend(hass))

        assert len(hass.http.paths) == 1
        static_path = hass.http.paths[0]
        assert static_path.url_path == "/advnfc_static"
        assert static_path.cache_headers is True
        registration = hass.panels["advnfc"]
        assert registration["webcomponent_name"] == "advnfc-administration-panel"
        assert registration["embed_iframe"] is False
        assert registration["require_admin"] is False
        assert registration["handle_safe_area"] is True
        assert registration["module_url"].startswith(
            "/advnfc_static/advnfc-administration-panel.mjs?v="
        )
        assert registration["config"] == {
            "interface_version": 3,
            "tag_mapping_schema_version": 1,
        }

        _run(panel.async_register_frontend(hass))
        assert len(hass.http.paths) == 1
        assert len(hass.panels) == 1
    finally:
        for name in STUBBED_MODULES:
            sys.modules.pop(name, None)
        sys.modules.update(saved)
