import logging
import aiohttp
from homeassistant.components.sensor import SensorEntity
from homeassistant.const import CONF_NAME, CONF_PASSWORD, CONF_EMAIL
import homeassistant.helpers.config_validation as cv
import voluptuous as vol

_LOGGER = logging.getLogger(__name__)

CONF_DOMAIN = "domain"

# Feste Werte für io_ph, io_flow und io_redox
FIXED_IO_PH = "e61d476d-bbd0-4527-a9f5-ef0170caa33c.o3"  # ID für den pH-Sensor
FIXED_IO_FLOW = "e61d476d-bbd0-4527-a9f5-ef0170caa33c.o0"  # ID für den Flow-Sensor
FIXED_IO_REDOX = "e61d476d-bbd0-4527-a9f5-ef0170caa33c.o4"  # ID für den Redox-Sensor

PLATFORM_SCHEMA = vol.Schema({
    vol.Required(CONF_EMAIL): cv.string,
    vol.Required(CONF_PASSWORD): cv.string,
    vol.Required(CONF_DOMAIN): cv.string,
    vol.Optional(CONF_NAME, default="WifiPoolSensor"): cv.string,
})

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Setup sensors from a config entry."""
    email = config_entry.data.get("email")
    password = config_entry.data.get("password")
    domain = config_entry.data.get("domain")
    name = "WifiPoolSensor"

    ph_sensor = WifiPoolSensorPh(name, email, password, domain)
    flow_sensor = WifiPoolSensorFlow(name, email, password, domain)
    redox_sensor = WifiPoolSensorRedox(name, email, password, domain)
    
    async_add_entities([ph_sensor, flow_sensor, redox_sensor])

class WifiPoolSensorPh(SensorEntity):
    """Representation of the WiFi Pool pH Sensor."""

    def __init__(self, name, email, password, domain):
        """Initialize the sensor."""
        self._name = f"{name}_ph"
        self._state = None
        self._email = email
        self._password = password
        self._domain = domain
        self._io_ph = FIXED_IO_PH
        self._cookies = None

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    async def login(self):
        """Perform login and return cookies if successful."""
        url = "https://api.wifipool.eu/native_mobile/users/login"
        login_data = {
            "email": self._email,
            "namespace": "default",
            "password": self._password
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=login_data) as response:
                if response.status == 200:
                    _LOGGER.info("Login erfolgreich!")
                    self._cookies = response.cookies
                else:
                    _LOGGER.error("Login fehlgeschlagen: %s", response.status)

    async def get_stats(self):
        """Get statistics for the sensor."""
        url = "https://api.wifipool.eu/native_mobile/harmopool/getStats"
        data = {
            "after": 1723973699831,
            "domain": self._domain,
            "io": self._io_ph
        }
        async with aiohttp.ClientSession(cookies=self._cookies) as session:
            async with session.post(url, json=data) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    _LOGGER.error("Datenabruf fehlgeschlagen: %s", response.status)
                    return None

    async def async_update(self):
        """Update the sensor state."""
        await self.login()
        if self._cookies:
            data = await self.get_stats()
            if data:
                latest_value = self.extract_latest_value(data)
                if latest_value is not None:
                    self._state = latest_value
                else:
                    self._state = "Kein gültiger Wert"
            else:
                self._state = "Datenabruf fehlgeschlagen"
        else:
            self._state = "Login fehlgeschlagen"

    def extract_latest_value(self, data):
        """Extract the latest value from the data."""
        _LOGGER.info("Daten zur Extraktion: %s", data)
        if isinstance(data, list) and len(data) > 0:
            latest_entry = data[-1]
            if "device_sensor_data" in latest_entry:
                sensor_data = latest_entry["device_sensor_data"]
                if "analog" in sensor_data and "4" in sensor_data["analog"]:
                    return sensor_data["analog"]["4"]
        _LOGGER.warning("'device_sensor_data' nicht in den Daten vorhanden.")
        return None

class WifiPoolSensorFlow(SensorEntity):
    """Representation of the WiFi Pool Flow Sensor."""

    def __init__(self, name, email, password, domain):
        """Initialize the sensor."""
        self._name = f"{name}_flow"
        self._state = None
        self._email = email
        self._password = password
        self._domain = domain
        self._io_flow = FIXED_IO_FLOW
        self._cookies = None

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    async def login(self):
        """Perform login and return cookies if successful."""
        url = "https://api.wifipool.eu/native_mobile/users/login"
        login_data = {
            "email": self._email,
            "namespace": "default",
            "password": self._password
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=login_data) as response:
                if response.status == 200:
                    _LOGGER.info("Login erfolgreich!")
                    self._cookies = response.cookies
                else:
                    _LOGGER.error("Login fehlgeschlagen: %s", response.status)

    async def get_stats(self):
        """Get statistics for the sensor."""
        url = "https://api.wifipool.eu/native_mobile/harmopool/getStats"
        data = {
            "after": 1724058213611,
            "domain": self._domain,
            "io": self._io_flow
        }
        async with aiohttp.ClientSession(cookies=self._cookies) as session:
            async with session.post(url, json=data) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    _LOGGER.error("Datenabruf fehlgeschlagen: %s", response.status)
                    return None

    async def async_update(self):
        """Update the sensor state."""
        await self.login()
        if self._cookies:
            data = await self.get_stats()
            if data:
                latest_value = self.extract_latest_value(data)
                if latest_value is not None:
                    self._state = latest_value
                else:
                    self._state = "Kein gültiger Wert"
            else:
                self._state = "Datenabruf fehlgeschlagen"
        else:
            self._state = "Login fehlgeschlagen"

    def extract_latest_value(self, data):
        """Extract the latest value from the data."""
        _LOGGER.info("Daten zur Extraktion: %s", data)
        if isinstance(data, list) and len(data) > 0:
            latest_entry = data[-1]
            if "device_sensor_data" in latest_entry:
                sensor_data = latest_entry["device_sensor_data"]
                if "switch" in sensor_data and "1" in sensor_data["switch"]:
                    return sensor_data["switch"]["1"]
        _LOGGER.warning("'device_sensor_data' nicht in den Daten vorhanden.")
        return None

class WifiPoolSensorRedox(SensorEntity):
    """Representation of the WiFi Pool Redox Sensor."""

    def __init__(self, name, email, password, domain):
        """Initialize the sensor."""
        self._name = f"{name}_redox"
        self._state = None
        self._email = email
        self._password = password
        self._domain = domain
        self._io_redox = FIXED_IO_REDOX
        self._cookies = None

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    async def login(self):
        """Perform login and return cookies if successful."""
        url = "https://api.wifipool.eu/native_mobile/users/login"
        login_data = {
            "email": self._email,
            "namespace": "default",
            "password": self._password
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=login_data) as response:
                if response.status == 200:
                    _LOGGER.info("Login erfolgreich!")
                    self._cookies = response.cookies
                else:
                    _LOGGER.error("Login fehlgeschlagen: %s", response.status)

    async def get_stats(self):
        """Get statistics for the sensor."""
        url = "https://api.wifipool.eu/native_mobile/harmopool/getStats"
        data = {
            "after": 0,
            "domain": self._domain,
            "io": self._io_redox
        }
        async with aiohttp.ClientSession(cookies=self._cookies) as session:
            async with session.post(url, json=data) as response:
                if response.status == 200:
                    json_data = await response.json()
                    _LOGGER.info("API-Antwort für Redox-Sensor: %s", json_data)
                    return json_data
                else:
                    _LOGGER.error("Datenabruf fehlgeschlagen: %s", response.status)
                    return None

    async def async_update(self):
        """Update the sensor state."""
        await self.login()
        if self._cookies:
            data = await self.get_stats()
            if data:
                latest_value = self.extract_latest_value(data)
                if latest_value is not None:
                    self._state = latest_value
                else:
                    self._state = "Kein gültiger Wert"
            else:
                self._state = "Datenabruf fehlgeschlagen"
        else:
            self._state = "Login fehlgeschlagen"

    def extract_latest_value(self, data):
        """Extract the latest value from the data."""
        _LOGGER.info("Daten zur Extraktion: %s", data)
        if isinstance(data, list) and len(data) > 0:
            latest_entry = data[-1]
            if "device_sensor_data" in latest_entry:
                sensor_data = latest_entry["device_sensor_data"]
                _LOGGER.info("Sensordaten für Redox: %s", sensor_data)
                if "analog" in sensor_data and "1" in sensor_data["analog"]:
                    return sensor_data["analog"]["1"]
        _LOGGER.warning("'device_sensor_data' nicht in den Daten vorhanden oder falsch formatiert.")
        return None