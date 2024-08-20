import voluptuous as vol
from homeassistant import config_entries
from .const import DOMAIN

class WifiPoolSensorConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            return self.async_create_entry(title="WiFi Pool Sensor", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("email"): str,
                vol.Required("password"): str,
                vol.Required("domain"): str,
                vol.Required("io"): str,
                vol.Required("io_flow"): str,
                vol.Required("io_redox"): str,
            }),
            errors=errors
        )
