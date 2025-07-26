# 🌊 WiFi Pool Sensor Integration for Home Assistant

![License](https://img.shields.io/github/license/MilanVives/hacs-twinpool?style=flat-square)
![Last Commit](https://img.shields.io/github/last-commit/MilanVives/hacs-twinpool?style=flat-square)
![Version](https://img.shields.io/badge/version-1.0-blue?style=flat-square)

This custom Home Assistant integration allows you to monitor your pool's pH levels, flow, and redox values using a WiFi-connected pool sensor.

## 🚀 Features

- 📊 **Monitor pH levels** in real-time.
- 🌊 **Track flow status** of your pool system.
- ⚗️ **Measure redox values** for optimal pool water quality.
- 🔒 Secure login with email and password.

## 🏊‍♂️ Supported Applications and Devices

This integration can be used with the following mobile app:

- [WiFi Pool App on the App Store](https://apps.apple.com/de/app/wifipool/id1527010555)

Additionally, it supports these dosing systems:

- [POOLSANA pH/Chlor Dosieranlage WiFiPool Connect Go 2.0](https://www.poolsana.de/automatische-poolsana-ph/chlor-dosieranlage-wifipool-connect-go-2.0)
- [Beniferro WiFi Dosing Systems](https://beniferro.eu/)

## 🛠 Installation

### Option 1: HACS (Home Assistant Community Store)

1. Open HACS in your Home Assistant instance.
2. Go to **Integrations** and click on the three dots in the top-right corner.
3. Choose **Custom repositories**.
4. Add the URL of this repository: `https://github.com/MilanVives/hacs-twinpool`.
5. Select **Integration** as the category.
6. Once added, search for "WiFi Pool Sensor" in HACS and install it.
7. Restart Home Assistant.

### Option 2: Manual Installation

1. **Download or clone** this repository into your Home Assistant `custom_components` directory:

   ```bash
   git clone https://github.com/MilanVives/hacs-twinpool.git custom_components/wifi_pool_sensor

   ```

2. Restart Home Assistant.

3. In the Home Assistant UI, navigate to Settings > Devices & Services > Integrations and click on Add Integration. Search for "WiFi Pool Sensor" and follow the configuration steps.

⚙️ Configuration
No need to worry about configuring IO values—they are preset for your convenience. Simply provide your email, password, and domain during setup.

🔍 Troubleshooting

- Ensure your API credentials are correct.
- Check the logs for detailed error messages: Settings > System > Logs.
  📄 License
  This project is licensed under the MIT License. See the LICENSE file for details.

👏 Contributing
Contributions are welcome! Feel free to submit issues or pull requests.

🌐 Links

- Documentation
- [Home Assistant](https://www.home-assistant.io/)
- [WiFi Pool App](https://apps.apple.com/de/app/wifipool/id1527010555)
- [POOLSANA WiFiPool Connect Go 2.0](https://www.poolsana.de/automatische-poolsana-ph/chlor-dosieranlage-wifipool-connect-go-2.0)
- [Beniferro WiFi Dosing Systems](https://beniferro.eu/)
- Made with ❤️ by Milan

Project inspired by: https://github.com/flipkill1985/hacs-wifipool.git
