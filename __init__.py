from homeassistant.helpers.typing import ConfigType
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from .const import DOMAIN
from .api import SungrowAPI  

import os
import shutil
import logging

# Initialize logger for this integration
_LOGGER = logging.getLogger(__name__)

# Define supported platforms for this integration
PLATFORMS = ["sensor"]

async def async_setup(hass: HomeAssistant, config: ConfigType):
    """Set up the Sungrow iSolar integration from YAML (not used here)."""
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up Sungrow iSolar from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    
    # Copy the integration icon to the /www/icons folder (for UI use)
    copy_integration_icon(hass)
    
    # Create API instance using credentials from config entry
    api = SungrowAPI(
        appkey=entry.data.get("appkey"),
        secret=entry.data.get("secret"),
        username=entry.data.get("username"),
        password=entry.data.get("password")
    )

    # Authenticate and obtain API token
    await api.login()

    # Store API instance in hass.data for later use by platforms
    hass.data[DOMAIN][entry.entry_id] = {
        "api": api
    }

    # Forward setup to supported platforms (e.g., sensor)
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload Sungrow iSolar config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    
    # Properly close the API session if available
    api = hass.data[DOMAIN][entry.entry_id]["api"]
    await api.close()
    
    # Remove from hass data if unload succeeded
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok
    
def copy_integration_icon(hass: HomeAssistant):
    """Copiază icon-ul în folderul www dacă nu există deja."""
    www_path = os.path.join(hass.config.path("www"), "icons")
    os.makedirs(www_path, exist_ok=True)

    src_icon = os.path.join(os.path.dirname(__file__), "icons", "sungrow_icon.png")
    dest_icon = os.path.join(www_path, "sungrow_icon.png")

    if not os.path.exists(dest_icon):
        try:
            shutil.copyfile(src_icon, dest_icon)
            _LOGGER.info("Sungrow icon copied successfully to /www/icons/")
        except Exception as e:
            _LOGGER.error("Error copying Sungrow icon: %s", e)