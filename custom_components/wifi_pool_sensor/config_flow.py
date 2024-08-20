import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult
from .const import DOMAIN, CONF_EMAIL, CONF_PASSWORD, CONF_DOMAIN, CONF_IO, CONF_IO_FLOW, CONF_IO_REDOX

class WifiPoolSensorConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None) -> FlowResult:
        errors = {}
        if user_input is not None:
            return self.async_create_entry(title=user_input[CONF_DOMAIN], data=user_input)

        data_schema = vol.Schema({
            vol.Required(CONF_EMAIL): str,
            vol.Required(CONF_PASSWORD): str,
            vol.Required(CONF_DOMAIN): str,
            vol.Required(CONF_IO): str,
            vol.Required(CONF_IO_FLOW): str,
            vol.Required(CONF_IO_REDOX): str
        })

        return self.async_show_form(step_id="user", data_schema=data_schema, errors=errors)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return WifiPoolSensorOptionsFlowHandler(config_entry)

class WifiPoolSensorOptionsFlowHandler(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        return await self.async_step_user()

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        data_schema = vol.Schema({
            vol.Required(CONF_IO): str,
            vol.Required(CONF_IO_FLOW): str,
            vol.Required(CONF_IO_REDOX): str
        })

        return self.async_show_form(step_id="user", data_schema=data_schema, errors=errors)
