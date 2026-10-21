"""Register the integration-owned AdvNFC administration proof panel."""

from __future__ import annotations

from hashlib import sha256
from pathlib import Path

from homeassistant.components import frontend, panel_custom
from homeassistant.components.http import StaticPathConfig
from homeassistant.core import HomeAssistant


PANEL_URL_PATH = "advnfc"
PANEL_WEB_COMPONENT = "advnfc-administration-panel"
PANEL_STATIC_URL = "/advnfc_static"
PANEL_MODULE = "advnfc-administration-panel.mjs"
FRONTEND_DIRECTORY = Path(__file__).parent / "frontend"
FRONTEND_MODULE_PATH = FRONTEND_DIRECTORY / PANEL_MODULE


def _module_digest() -> str:
    """Return a content identity used to invalidate the browser module cache."""
    return sha256(FRONTEND_MODULE_PATH.read_bytes()).hexdigest()[:16]


async def async_register_frontend(hass: HomeAssistant) -> None:
    """Expose the bundled module and register one non-iframe sidebar panel."""
    if frontend.async_panel_exists(hass, PANEL_URL_PATH):
        return

    digest = await hass.async_add_executor_job(_module_digest)
    await hass.http.async_register_static_paths(
        [
            StaticPathConfig(
                PANEL_STATIC_URL,
                str(FRONTEND_DIRECTORY),
                cache_headers=True,
            )
        ]
    )
    await panel_custom.async_register_panel(
        hass=hass,
        frontend_url_path=PANEL_URL_PATH,
        webcomponent_name=PANEL_WEB_COMPONENT,
        module_url=f"{PANEL_STATIC_URL}/{PANEL_MODULE}?v={digest}",
        sidebar_title="AdvNFC",
        sidebar_icon="mdi:nfc-variant",
        embed_iframe=False,
        require_admin=False,
        handle_safe_area=True,
        config={"interface_version": 3, "tag_mapping_schema_version": 1},
    )
