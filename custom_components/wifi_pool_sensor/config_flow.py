async def async_step_user(self, user_input=None):
    errors = {}
    if user_input is not None:
        return self.async_create_entry(title="WiFi Pool Sensor", data=user_input)

    data_schema = vol.Schema({
        vol.Required("email"): str,
        vol.Required("password"): str,
        vol.Required("domain"): str,
        vol.Optional("io"): str,
        vol.Optional("io_flow"): str,
        vol.Optional("io_redox"): str
    })

    return self.async_show_form(
        step_id="user",
        data_schema=data_schema,
        errors=errors,
        description_placeholders={
            "email": "your email",
            "password": "your password",
            "domain": "your domain ID",
            "io": "sensor ID for pH",
            "io_flow": "sensor ID for flow",
            "io_redox": "sensor ID for redox"
        }
    )
