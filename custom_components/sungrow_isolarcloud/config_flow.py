import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import HomeAssistant

from .const import (
    DOMAIN,
    CONF_USERNAME,
    CONF_PASSWORD,
    CONF_APPKEY,
    CONF_SECRET,
    REGIONS,
    DEFAULT_REGION,
)
from .api import SungrowAPI

# Base configuration form schema (user input)
DATA_SCHEMA = vol.Schema({
    vol.Required(CONF_USERNAME): str,
    vol.Required(CONF_PASSWORD): str,
    vol.Required(CONF_APPKEY): str,
    vol.Required(CONF_SECRET): str,
})

class SungrowConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
     """Handle the configuration flow for the Sungrow iSolarCloud integration."""
    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            # Determine selected region and build the base API URL
            region = user_input.get("region", DEFAULT_REGION)
            base_url = REGIONS[region]
            
            # Initialize API instance with provided credentials
            api = SungrowAPI(
                user_input[CONF_APPKEY],
                user_input[CONF_SECRET],
                user_input[CONF_USERNAME],
                user_input[CONF_PASSWORD],
                base_url=base_url,
            )
            
            # Validate credentials by attempting a login
            try:
                token = await api.login()
                if token:
                    # Successfully authenticated, create configuration entry
                    return self.async_create_entry(title="Sungrow iSolar", data=user_input)
                else:
                    errors["base"] = "invalid_auth"
            except Exception:
                errors["base"] = "cannot_connect"
        
        # Build the setup form schema, including region selection
        data_schema = vol.Schema({
            vol.Required(CONF_USERNAME): str,
            vol.Required(CONF_PASSWORD): str,
            vol.Required(CONF_APPKEY): str,
            vol.Required(CONF_SECRET): str,
            vol.Required("region", default=DEFAULT_REGION): vol.In(list(REGIONS.keys())),
        })
        
        # Display the configuration form to the user
        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
            description_placeholders={
                "icon_url": "/local/my_component/my_icon.png",
                "help_text": "Add Sungrow Credentials"
            }
        )
