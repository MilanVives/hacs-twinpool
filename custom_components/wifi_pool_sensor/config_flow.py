import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from .const import DOMAIN

@callback
def configured_instances(hass):
    """Return a set of configured instances."""
    return {entry.title for entry in hass.config_entries.async_entries(DOMAIN)}

class WifiPoolConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for WiFi Pool."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            return self.async_create_entry(title=user_input["email"], data=user_input)

        data_schema = vol.Schema({
            vol.Required("email"): str,
            vol.Required("password"): str,
            vol.Required("domain"): str,
        })

        return self.async_show_form(step_id="user", data_schema=data_schema, errors=errors)
