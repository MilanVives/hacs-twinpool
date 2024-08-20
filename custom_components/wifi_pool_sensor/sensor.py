import requests
import logging
from homeassistant.helpers.entity import Entity

_LOGGER = logging.getLogger(__name__)

def setup_platform(hass, config, add_entities, discovery_info=None):
    email = config.get("email")
    password = config.get("password")
    domain = config.get("domain")
    io = config.get("io")
    io_flow = config.get("io_flow")
    io_redox = config.get("io_redox")

    sensors = [
        WifiPoolSensor(name="WifiPoolSensor_ph", email=email, password=password, domain=domain, io=io, sensor_type="pH"),
        WifiPoolSensor(name="WifiPoolSensor_flow", email=email, password=password, domain=domain, io=io_flow, sensor_type="flow"),
        WifiPoolSensor(name="WifiPoolSensor_redox", email=email, password=password, domain=domain, io=io_redox, sensor_type="redox")
    ]
    
    add_entities(sensors)

class WifiPoolSensor(Entity):
    def __init__(self, name, email, password, domain, io, sensor_type):
        self._name = name
        self._state = None
        self._email = email
        self._password = password
        self._domain = domain
        self._io = io
        self._sensor_type = sensor_type
        self.update()

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    def login(self):
        url = "https://api.wifipool.eu/native_mobile/users/login"
        login_data = {
            "email": self._email,
            "namespace": "default",
            "password": self._password
        }
        response = requests.post(url, json=login_data)
        if response.status_code == 200:
            _LOGGER.info("Login erfolgreich!")
            return response.cookies
        else:
            _LOGGER.error("Login fehlgeschlagen: %s", response.status_code)
            return None

    def get_stats(self, cookies):
        url = "https://api.wifipool.eu/native_mobile/harmopool/getStats"
        data = {
            "after": 0,
            "domain": self._domain,
            "io": self._io
        }
        response = requests.post(url, json=data, cookies=cookies)
        if response.status_code == 200:
            return response.json()
        else:
            _LOGGER.error("Datenabruf fehlgeschlagen: %s", response.status_code)
            return None

    def update(self):
        cookies = self.login()
        if cookies:
            data = self.get_stats(cookies)
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
        _LOGGER.info("Daten zur Extraktion: %s", data)
        if isinstance(data, list) and len(data) > 0:
            latest_entry = data[-1]
            if "device_sensor_data" in latest_entry:
                sensor_data = latest_entry["device_sensor_data"]
                if self._sensor_type == "pH":
                    return sensor_data.get("analog", {}).get("4")
                elif self._sensor_type == "flow":
                    return sensor_data.get("switch", {}).get("1")
                elif self._sensor_type == "redox":
                    return sensor_data.get("analog", {}).get("1")
        _LOGGER.warning("'device_sensor_data' nicht in den Daten vorhanden.")
        return None
