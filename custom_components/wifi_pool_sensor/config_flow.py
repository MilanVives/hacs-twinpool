import voluptuous as vol
from homeassistant import config_entries
from .const import DOMAIN

class WifiPoolSensorConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            return self.async_create_entry(title="WiFi Pool Sensor", data=user_input)

        data_schema = vol.Schema({
            vol.Required("email", description={"suggested_value": user_input.get("email") if user_input else ""}): str,
            vol.Required("password", description={"suggested_value": user_input.get("password") if user_input else ""}): str,
            vol.Required("domain", description={"suggested_value": user_input.get("domain") if user_input else ""}): str,
            vol.Optional("io", description={"suggested_value": user_input.get("io") if user_input else ""}): str,
            vol.Optional("io_flow", description={"suggested_value": user_input.get("io_flow") if user_input else ""}): str,
            vol.Optional("io_redox", description={"suggested_value": user_input.get("io_redox") if user_input else ""}): str
        })

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors
        )
