from homeassistant.helpers.entity import Entity
from .const import DOMAIN, CONF_EMAIL, CONF_PASSWORD, CONF_DOMAIN, CONF_IO, CONF_IO_FLOW, CONF_IO_REDOX

async def async_setup_entry(hass, config_entry, async_add_entities):
    config = config_entry.data

    email = config[CONF_EMAIL]
    password = config[CONF_PASSWORD]
    domain = config[CONF_DOMAIN]
    io = config[CONF_IO]
    io_flow = config[CONF_IO_FLOW]
    io_redox = config[CONF_IO_REDOX]
    name = config.get(CONF_NAME, DEFAULT_NAME)

    entities = [
        WifiPoolSensorPh(name, email, password, domain, io),
        WifiPoolSensorFlow(name, email, password, domain, io_flow),
        WifiPoolSensorRedox(name, email, password, domain, io_redox)
    ]
    async_add_entities(entities, True)

# Hier folgen die Klassen für WifiPoolSensorPh, WifiPoolSensorFlow, WifiPoolSensorRedox
# ...
