# Sungrow iSolarCloud Integration for Home Assistant

A custom Home Assistant integration that connects your **Sungrow iSolarCloud** account to Home Assistant, allowing you to monitor **solar plant production, inverter data, and real-time device information** directly in your dashboard.

---

**Features**

-  Login securely using your **Sungrow iSolarCloud** credentials  
-  Supports multiple **Sungrow Cloud regions** (China, International, Europe, Australia)  
-  Fetch real-time inverter and plant data  
-  Automatically detects your power stations and devices  
-  Automatic token refresh when session expires  
-  Ready for use with Home Assistant Energy Dashboard
-  Currently, the Solar Plant is configured to fetch only these Common Measuring points: 83106, 83118, 83124, 83072, 83102. In case more points are needed, edit the apy.py file and add more points in the plant_point_id_list.
   (the const.py contains description for all of the available common measuring points).
---

**Installation**

### Manual Installation

1. Copy the `custom_components/sungrow_isolarcloud` folder into your Home Assistant config directory:
2. Restart Home Assistant.

---

**Configuration**
You can set up the integration directly from **Home Assistant UI**:

1. Go to **Settings → Devices & Services → Add Integration**
2. Search for **Sungrow iSolarCloud**
3. Enter your credentials and API keys:
- `Username`
- `Password`
- `App Key`
- `Secret Key`
4. Select your **Region** from the dropdown:
-  **China** → `https://gateway.isolarcloud.com/`
-  **International** → `https://gateway.isolarcloud.com.hk/`
-  **Europe** → `https://gateway.isolarcloud.eu/`
-  **Australia** → `https://augateway.isolarcloud.com/`
5. Click **Submit** — if login is successful, your devices will be discovered automatically.

---

**Data Provided**
Depending on your Sungrow devices, the integration can provide:
- Current power generation (W)
- Daily energy production (kWh)
- Lifetime energy (kWh)
- Inverter status
- Fault and alarm status
- Plant summary data (voltage, current, power, etc.)

---

**Technical Details**
- Uses the official **Sungrow iSolarCloud open API**
- Fully asynchronous using `aiohttp`
- Supports automatic token refresh and retry on expired sessions
- Written in modern Python 3.12 for compatibility with latest Home Assistant versions
- Testes it with a Sungrow SH6.0-RT Inverter + SBR064 Battery and a DTSU666-20D5 Smart Meter. On all of the device, it shows common sensors
---

**Contributing**
Contributions are welcome!
Feel free to open issues or submit pull requests for:

Additional sensors or metrics
Optimizations
UI improvements
Localization / translation

**Disclaimer**
This integration is not officially affiliated with Sungrow. All data is retrieved using the public Sungrow iSolarCloud API.
Use at your own risk.

**Troubleshooting**

If you see login or connection errors:
- Double-check your **App Key** and **Secret Key**
- Verify your **region selection**
- Make sure your **Sungrow account** has access to your plant data
  
**Screenshots**
<img width="1292" height="871" alt="image" src="https://github.com/user-attachments/assets/606e2e50-f137-46d9-9abd-899b6ce7af3d" />
<img width="527" height="1027" alt="image" src="https://github.com/user-attachments/assets/8ae35ad7-3bd4-4e1f-a6d4-e7ec0e3677ce" />
<img width="534" height="1110" alt="image" src="https://github.com/user-attachments/assets/09695392-e116-45e1-905a-251eb60dff35" />
<img width="527" height="880" alt="image" src="https://github.com/user-attachments/assets/aeb31eea-2eca-4066-907f-b27dee0fc1d5" />




