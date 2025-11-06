from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass
from homeassistant.const import (
    UnitOfEnergy, 
    UnitOfPower, 
    UnitOfTemperature, 
    UnitOfMass, 
    UnitOfIrradiance,
    PERCENTAGE,
    UnitOfElectricCurrent,
    UnitOfElectricPotential,
    UnitOfFrequency,
    UnitOfTime 
)

DOMAIN = "sungrow_isolar"
CONF_USERNAME = "username"
CONF_PASSWORD = "password"
CONF_APPKEY = "appkey"
CONF_SECRET = "secret"

REGIONS = {
    "China": "https://gateway.isolarcloud.com/",
    "International": "https://gateway.isolarcloud.com.hk/",
    "Europe": "https://gateway.isolarcloud.eu/",
    "Australia": "https://augateway.isolarcloud.com/",
}

DEFAULT_REGION = "Europe"

PLANT_TYPE_MAP = {
    1: "Utility Plant",
    3: "Distributed PV Plant",
    4: "Residential PV Plant",
    5: "Residential Energy Storage Plant",
    6: "Village Plant",
    7: "Distributed Energy Storage Plant",
    8: "Poverty Alleviation Plant",
    9: "Wind Power Plant",
    10: "Utility Energy Storage Plant",
    12: "C&I Energy Storage Plant",
}

BUILD_STATUS_MAP = {
    0: "Not Started",
    1: "Under Construction",
    2: "Connected",
    3: "Planned",
    4: "Not Connected",
}

FAULT_STATUS_MAP = {1: "Fault", 2: "Alarm", 3: "Normal"}
DEVICE_FAULT_STATUS_MAP = {1: "Fault", 2: "Alarm", 4: "Normal"}
PLANT_STATUS_MAP = {1: "Normal", 2: "Disabled", 3: "Connected"}
PLANT_SHARE_TYPE_MAP = {1: "Browsing Rights", 2: "Management Rights", 0: "Non-sharing"}
GRID_CONNECTION_TYPE_MAP = {1: "Full Grid", 2: "Self-Generated and Self-Used (Surplus Power)", 3: "Self-Generated and Self-Used (No Feed Network)", 4: "Off-Grid"}


COMMON_MEASURING_PLANT_POINTS_MAP = {
    "p83022": {"name": "Daily Yield of Plant", "unit": UnitOfEnergy.WATT_HOUR, "icon": "mdi:flash", "device_class": SensorDeviceClass.ENERGY, "state_class": SensorStateClass.TOTAL_INCREASING},
    "p83024": {"name": "Plant Total Yield", "unit": UnitOfEnergy.WATT_HOUR, "icon": "mdi:flash", "device_class": SensorDeviceClass.ENERGY, "state_class": SensorStateClass.TOTAL_INCREASING},
    "p83033": {"name": "Plant Power", "unit": UnitOfPower.WATT, "icon": "mdi:solar-power", "device_class": SensorDeviceClass.POWER, "state_class": SensorStateClass.MEASUREMENT},
    "p83019": {"name": "Plant Power/Installed Power of Plant", "unit": "", "icon": "mdi:chart-line"},
    "p83006": {"name": "Meter Daily Yield", "unit": UnitOfEnergy.WATT_HOUR, "icon": "mdi:flash", "device_class": SensorDeviceClass.ENERGY, "state_class": SensorStateClass.TOTAL_INCREASING},
    "p83020": {"name": "Meter Total Yield", "unit": UnitOfEnergy.WATT_HOUR, "icon": "mdi:flash", "device_class": SensorDeviceClass.ENERGY, "state_class": SensorStateClass.TOTAL_INCREASING},
    "p83011": {"name": "Meter E-daily Consumption", "unit": UnitOfEnergy.WATT_HOUR, "icon": "mdi:flash", "device_class": SensorDeviceClass.ENERGY, "state_class": SensorStateClass.TOTAL_INCREASING},
    "p83021": {"name": "Accumulative Power Consumption by Meter", "unit": UnitOfEnergy.WATT_HOUR, "icon": "mdi:flash", "device_class": SensorDeviceClass.ENERGY, "state_class": SensorStateClass.TOTAL_INCREASING},
    "p83032": {"name": "Meter AC Power", "unit": UnitOfPower.WATT, "icon": "mdi:solar-power", "device_class": SensorDeviceClass.POWER, "state_class": SensorStateClass.MEASUREMENT},
    "p83002": {"name": "Inverter AC Power", "unit": UnitOfPower.WATT, "icon": "mdi:solar-power", "device_class": SensorDeviceClass.POWER, "state_class": SensorStateClass.MEASUREMENT},
    "p83004": {"name": "Inverter Total Yield", "unit": UnitOfEnergy.WATT_HOUR, "icon": "mdi:flash", "device_class": SensorDeviceClass.ENERGY, "state_class": SensorStateClass.TOTAL_INCREASING},
    "p83009": {"name": "Inverter Daily Yield", "unit": UnitOfEnergy.WATT_HOUR, "icon": "mdi:flash", "device_class": SensorDeviceClass.ENERGY, "state_class": SensorStateClass.TOTAL_INCREASING},
    "p83012": {"name": "P-radiation-H", "unit": "W/m²", "icon": "mdi:weather-sunny", "device_class": SensorDeviceClass.IRRADIANCE, "state_class": SensorStateClass.MEASUREMENT},
    "p83013": {"name": "Daily Irradiation", "unit": "Wh/m²", "icon": "mdi:weather-sunny"},
    "p83023": {"name": "Plant PR", "unit": None, "icon": "mdi:chart-line"},
    "p83025": {"name": "Plant Equivalent Hours", "unit": UnitOfTime.HOURS, "icon": "mdi:timer"},
    "p83005": {"name": "Daily Equivalent Hours", "unit": UnitOfTime.HOURS, "icon": "mdi:timer"},
    "p83007": {"name": "Meter PR", "unit": None, "icon": "mdi:chart-line"},
    "p83018": {"name": "Daily Yield (Theoretical)", "unit": UnitOfEnergy.WATT_HOUR, "icon": "mdi:flash", "device_class": SensorDeviceClass.ENERGY, "state_class": SensorStateClass.TOTAL_INCREASING},
    "p83001": {"name": "Inverter AC Power Normalization", "unit": "W/Wp", "icon": "mdi:solar-power"},
    "p83008": {"name": "Daily Equivalent Hours of Inverter", "unit": "h", "icon": "mdi:timer"},
    "p83010": {"name": "Inverter PR", "unit": None, "icon": "mdi:chart-line"},
    "p83016": {"name": "Plant Ambient Temperature", "unit": UnitOfTemperature.CELSIUS, "icon": "mdi:thermometer", "device_class": SensorDeviceClass.TEMPERATURE, "state_class": SensorStateClass.MEASUREMENT},
    "p83017": {"name": "Plant Module Temperature", "unit": UnitOfTemperature.CELSIUS, "icon": "mdi:thermometer", "device_class": SensorDeviceClass.TEMPERATURE, "state_class": SensorStateClass.MEASUREMENT},
    "p83046": {"name": "PCS Total Active Power", "unit": UnitOfPower.WATT, "icon": "mdi:solar-power", "device_class": SensorDeviceClass.POWER, "state_class": SensorStateClass.MEASUREMENT},
    "p83052": {"name": "Load Power", "unit": UnitOfPower.WATT, "icon": "mdi:home-lightning-bolt", "device_class": SensorDeviceClass.POWER, "state_class": SensorStateClass.MEASUREMENT},
    "p83067": {"name": "Total Active Power of PV", "unit": UnitOfPower.WATT, "icon": "mdi:solar-power", "device_class": SensorDeviceClass.POWER, "state_class": SensorStateClass.MEASUREMENT},
    "p83097": {"name": "Daily Direct Energy Consumption", "unit": UnitOfEnergy.WATT_HOUR, "icon": "mdi:flash", "device_class": SensorDeviceClass.ENERGY, "state_class": SensorStateClass.TOTAL_INCREASING},
    "p83100": {"name": "Total Direct Energy Consumption", "unit": UnitOfEnergy.WATT_HOUR, "icon": "mdi:flash", "device_class": SensorDeviceClass.ENERGY, "state_class": SensorStateClass.TOTAL_INCREASING},
    "p83102": {"name": "Energy Purchased Today", "unit": UnitOfEnergy.WATT_HOUR, "icon": "mdi:transmission-tower-export", "device_class": SensorDeviceClass.ENERGY, "state_class": SensorStateClass.TOTAL_INCREASING},
    "p83105": {"name": "Total Purchased Energy", "unit": UnitOfEnergy.WATT_HOUR, "icon": "mdi:transmission-tower-export", "device_class": SensorDeviceClass.ENERGY, "state_class": SensorStateClass.TOTAL_INCREASING},
    "p83106": {"name": "Load Power", "unit": UnitOfPower.WATT, "icon": "mdi:home-lightning-bolt", "device_class": SensorDeviceClass.POWER, "state_class": SensorStateClass.MEASUREMENT},
    "p83118": {"name": "Daily Load Consumption", "unit": UnitOfEnergy.WATT_HOUR, "icon": "mdi:home-lightning-bolt", "device_class": SensorDeviceClass.ENERGY, "state_class": SensorStateClass.TOTAL_INCREASING},
    "p83124": {"name": "Total Load Consumption", "unit": UnitOfEnergy.WATT_HOUR, "icon": "mdi:home-lightning-bolt", "device_class": SensorDeviceClass.ENERGY, "state_class": SensorStateClass.TOTAL_INCREASING},
    "p83119": {"name": "Daily Feed-in Energy (PV)", "unit": UnitOfEnergy.WATT_HOUR, "icon": "mdi:solar-power", "device_class": SensorDeviceClass.ENERGY, "state_class": SensorStateClass.TOTAL_INCREASING},
    "p83072": {"name": "Feed-in Energy Today", "unit": UnitOfEnergy.WATT_HOUR, "icon": "mdi:transmission-tower-import", "device_class": SensorDeviceClass.ENERGY, "state_class": SensorStateClass.TOTAL_INCREASING},
    "p83075": {"name": "Feed-in Energy Total", "unit": UnitOfEnergy.WATT_HOUR, "icon": "mdi:transmission-tower-import", "device_class": SensorDeviceClass.ENERGY, "state_class": SensorStateClass.TOTAL_INCREASING},
    "p83252": {"name": "Battery Level (SOC)", "unit": PERCENTAGE, "icon": "mdi:battery", "device_class": SensorDeviceClass.BATTERY, "state_class": SensorStateClass.MEASUREMENT},
    "p83129": {"name": "Battery SOC", "unit": PERCENTAGE, "icon": "mdi:battery", "device_class": SensorDeviceClass.BATTERY, "state_class": SensorStateClass.MEASUREMENT},
    "p83232": {"name": "Total field SOC", "unit": PERCENTAGE, "icon": "mdi:battery", "device_class": SensorDeviceClass.BATTERY, "state_class": SensorStateClass.MEASUREMENT},
    "p83233": {"name": "Total field maximum rechargeable power", "unit": UnitOfPower.WATT, "icon": "mdi:solar-power", "device_class": SensorDeviceClass.POWER, "state_class": SensorStateClass.MEASUREMENT},
    "p83234": {"name": "Total field maximum dischargeable power", "unit": UnitOfPower.WATT, "icon": "mdi:solar-power", "device_class": SensorDeviceClass.POWER, "state_class": SensorStateClass.MEASUREMENT},
    "p83235": {"name": "Total field chargeable energy", "unit": UnitOfEnergy.WATT_HOUR, "icon": "mdi:battery-charging", "device_class": SensorDeviceClass.ENERGY, "state_class": SensorStateClass.TOTAL_INCREASING},
    "p83236": {"name": "Total field dischargeable energy", "unit": UnitOfEnergy.WATT_HOUR, "icon": "mdi:battery-charging", "device_class": SensorDeviceClass.ENERGY, "state_class": SensorStateClass.TOTAL_INCREASING},
    "p83237": {"name": "Total field energy storage maximum reactive power", "unit": UnitOfPower.WATT, "icon": "mdi:solar-power", "device_class": SensorDeviceClass.POWER, "state_class": SensorStateClass.MEASUREMENT},
    "p83238": {"name": "Total field energy storage active power", "unit": UnitOfPower.WATT, "icon": "mdi:solar-power", "device_class": SensorDeviceClass.POWER, "state_class": SensorStateClass.MEASUREMENT},
    "p83239": {"name": "Total field reactive power", "unit": "var", "icon": "mdi:flash"},
    "p83240": {"name": "Total field power factor", "unit": None, "icon": "mdi:chart-line"},
    "p83241": {"name": "Total field charge capacity", "unit": UnitOfEnergy.WATT_HOUR, "icon": "mdi:battery-charging", "device_class": SensorDeviceClass.ENERGY, "state_class": SensorStateClass.TOTAL_INCREASING},
    "p83242": {"name": "Total field discharge capacity", "unit": UnitOfEnergy.WATT_HOUR, "icon": "mdi:battery-charging", "device_class": SensorDeviceClass.ENERGY, "state_class": SensorStateClass.TOTAL_INCREASING},
    "p83243": {"name": "Daily field charge capacity", "unit": UnitOfEnergy.WATT_HOUR, "icon": "mdi:battery-charging", "device_class": SensorDeviceClass.ENERGY, "state_class": SensorStateClass.TOTAL_INCREASING},
    "p83244": {"name": "Daily field discharge capacity", "unit": UnitOfEnergy.WATT_HOUR, "icon": "mdi:battery-charging", "device_class": SensorDeviceClass.ENERGY, "state_class": SensorStateClass.TOTAL_INCREASING},
    "p83548": {"name": "Total Number of Charge/Discharge", "unit": None, "icon": "mdi:chart-bar"},
    "p83549": {"name": "Grid Active Power", "unit": UnitOfPower.WATT, "icon": "mdi:solar-power", "device_class": SensorDeviceClass.POWER, "state_class": SensorStateClass.MEASUREMENT},
    "p83419": {"name": "Daily Highest Inverter Power/Inverter Installed Capacity", "unit": "", "icon": "mdi:chart-line"},
    "p83317": {"name": "Power Forecast", "unit": UnitOfPower.WATT, "icon": "mdi:solar-power", "device_class": SensorDeviceClass.POWER, "state_class": SensorStateClass.MEASUREMENT},
    "p83318": {"name": "Planned ES Charging/Discharging Power", "unit": UnitOfPower.WATT, "icon": "mdi:battery-charging", "device_class": SensorDeviceClass.POWER, "state_class": SensorStateClass.MEASUREMENT},
    "p83319": {"name": "Planned ES SOC", "unit": PERCENTAGE, "icon": "mdi:battery", "device_class": SensorDeviceClass.BATTERY, "state_class": SensorStateClass.MEASUREMENT},
    "p83320": {"name": "Planned Charging Power", "unit": UnitOfEnergy.WATT_HOUR, "icon": "mdi:battery-charging", "device_class": SensorDeviceClass.ENERGY, "state_class": SensorStateClass.TOTAL_INCREASING},
    "p83321": {"name": "Planned Discharging Power", "unit": UnitOfEnergy.WATT_HOUR, "icon": "mdi:battery-charging", "device_class": SensorDeviceClass.ENERGY, "state_class": SensorStateClass.TOTAL_INCREASING},
    "p83322": {"name": "ESS Daily Charge (EMS)", "unit": UnitOfEnergy.WATT_HOUR, "icon": "mdi:battery-charging", "device_class": SensorDeviceClass.ENERGY, "state_class": SensorStateClass.TOTAL_INCREASING},
    "p83323": {"name": "ESS Daily Discharge (EMS)", "unit": UnitOfEnergy.WATT_HOUR, "icon": "mdi:battery-charging", "device_class": SensorDeviceClass.ENERGY, "state_class": SensorStateClass.TOTAL_INCREASING},
    "p83324": {"name": "Energy Storage Cumulative Charge", "unit": UnitOfEnergy.WATT_HOUR, "icon": "mdi:battery-charging", "device_class": SensorDeviceClass.ENERGY, "state_class": SensorStateClass.TOTAL_INCREASING},
    "p83325": {"name": "Cumulative Discharge", "unit": UnitOfEnergy.WATT_HOUR, "icon": "mdi:battery-charging", "device_class": SensorDeviceClass.ENERGY, "state_class": SensorStateClass.TOTAL_INCREASING},
    "p83326": {"name": "Energy Storage Active Power (EMS)", "unit": UnitOfPower.WATT, "icon": "mdi:solar-power", "device_class": SensorDeviceClass.POWER, "state_class": SensorStateClass.MEASUREMENT},
    "p83327": {"name": "Energy Storage Remaining Charge", "unit": UnitOfEnergy.WATT_HOUR, "icon": "mdi:battery-charging", "device_class": SensorDeviceClass.ENERGY, "state_class": SensorStateClass.TOTAL_INCREASING},
    "p83328": {"name": "Grid Active Power (EMS)", "unit": UnitOfPower.WATT, "icon": "mdi:solar-power", "device_class": SensorDeviceClass.POWER, "state_class": SensorStateClass.MEASUREMENT},
    "p83329": {"name": "PV Active Power (EMS)", "unit": UnitOfPower.WATT, "icon": "mdi:solar-power", "device_class": SensorDeviceClass.POWER, "state_class": SensorStateClass.MEASUREMENT},
    "p83330": {"name": "Load Active Power (EMS)", "unit": UnitOfPower.WATT, "icon": "mdi:flash", "device_class": SensorDeviceClass.POWER, "state_class": SensorStateClass.MEASUREMENT},
    "p83331": {"name": "Daily PV Yield (EMS)", "unit": UnitOfEnergy.WATT_HOUR, "icon": "mdi:flash", "device_class": SensorDeviceClass.ENERGY, "state_class": SensorStateClass.TOTAL_INCREASING},
    "p83332": {"name": "Total PV Yield", "unit": UnitOfEnergy.WATT_HOUR, "icon": "mdi:flash", "device_class": SensorDeviceClass.ENERGY, "state_class": SensorStateClass.TOTAL_INCREASING},
    "p83334": {"name": "Energy Storage SOC (EMS)", "unit": PERCENTAGE, "icon": "mdi:battery", "device_class": SensorDeviceClass.BATTERY, "state_class": SensorStateClass.MEASUREMENT}
}

ENERGY_STORAGE_SYS_NAME_POINT_MAP = {
    # 🔹 Inverter (device_type 14)
    "p13003": {"name": "Total DC Power", "unit": UnitOfPower.WATT, "icon": "mdi:flash", "device_type": 14, "device_class": SensorDeviceClass.POWER, "state_class": SensorStateClass.MEASUREMENT},
    "p13011": {"name": "Active Power", "unit": UnitOfPower.WATT, "icon": "mdi:flash", "device_type": 14, "device_class": SensorDeviceClass.POWER, "state_class": SensorStateClass.MEASUREMENT},
    "p13012": {"name": "Total Reactive Power", "unit": "var", "icon": "mdi:flash", "device_type": 14, "device_class": SensorDeviceClass.POWER, "state_class": SensorStateClass.MEASUREMENT},
    "p13013": {"name": "Power Factor", "unit": None, "icon": "mdi:math-cos", "device_type": 14},
    "p13157": {"name": "Phase A Voltage", "unit": UnitOfElectricPotential.VOLT, "icon": "mdi:sine-wave", "device_type": 14, "device_class": SensorDeviceClass.VOLTAGE, "state_class": SensorStateClass.MEASUREMENT},
    "p13158": {"name": "Phase B Voltage", "unit": UnitOfElectricPotential.VOLT, "icon": "mdi:sine-wave", "device_type": 14, "device_class": SensorDeviceClass.VOLTAGE, "state_class": SensorStateClass.MEASUREMENT},
    "p13159": {"name": "Phase C Voltage", "unit": UnitOfElectricPotential.VOLT, "icon": "mdi:sine-wave", "device_type": 14, "device_class": SensorDeviceClass.VOLTAGE, "state_class": SensorStateClass.MEASUREMENT},
    "p13008": {"name": "Phase A Current", "unit": UnitOfElectricCurrent.AMPERE, "icon": "mdi:current-ac", "device_type": 14, "device_class": SensorDeviceClass.CURRENT, "state_class": SensorStateClass.MEASUREMENT},
    "p13009": {"name": "Phase B Current", "unit": UnitOfElectricCurrent.AMPERE, "icon": "mdi:current-ac", "device_type": 14, "device_class": SensorDeviceClass.CURRENT, "state_class": SensorStateClass.MEASUREMENT},
    "p13010": {"name": "Phase C Current", "unit": UnitOfElectricCurrent.AMPERE, "icon": "mdi:current-ac", "device_type": 14, "device_class": SensorDeviceClass.CURRENT, "state_class": SensorStateClass.MEASUREMENT},
    "p13007": {"name": "Grid Frequency", "unit": UnitOfFrequency.HERTZ, "icon": "mdi:waveform", "device_type": 14,"device_class": SensorDeviceClass.FREQUENCY, "state_class": SensorStateClass.MEASUREMENT},
    "p13112": {"name": "Daily PV Yield", "unit": UnitOfEnergy.WATT_HOUR, "icon": "mdi:home-lightning-bolt", "device_type": 14, "device_class": SensorDeviceClass.ENERGY, "state_class": SensorStateClass.TOTAL_INCREASING},
    "p13134": {"name": "Total PV Yield", "unit": UnitOfEnergy.WATT_HOUR, "icon": "mdi:home-lightning-bolt", "device_type": 14, "device_class": SensorDeviceClass.ENERGY, "state_class": SensorStateClass.TOTAL_INCREASING},
    "p13161": {"name": "Bus Voltage", "unit": UnitOfElectricPotential.VOLT, "icon": "mdi:sine-wave", "device_type": 14, "device_class": SensorDeviceClass.VOLTAGE, "state_class": SensorStateClass.MEASUREMENT},
    "p13001": {"name": "MPPT1 Voltage", "unit": UnitOfElectricPotential.VOLT, "icon": "mdi:solar-panel", "device_type": 14, "device_class": SensorDeviceClass.VOLTAGE, "state_class": SensorStateClass.MEASUREMENT},
    "p13105": {"name": "MPPT2 Voltage", "unit": UnitOfElectricPotential.VOLT, "icon": "mdi:solar-panel", "device_type": 14, "device_class": SensorDeviceClass.VOLTAGE, "state_class": SensorStateClass.MEASUREMENT},
    "p13002": {"name": "MPPT1 Current", "unit": UnitOfElectricCurrent.AMPERE, "icon": "mdi:current-dc", "device_type": 14, "device_class": SensorDeviceClass.CURRENT, "state_class": SensorStateClass.MEASUREMENT},
    "p13106": {"name": "MPPT2 Current", "unit": UnitOfElectricCurrent.AMPERE, "icon": "mdi:current-dc", "device_type": 14, "device_class": SensorDeviceClass.CURRENT, "state_class": SensorStateClass.MEASUREMENT},
    "p13122": {"name": "Feed-In Energy Today", "unit": UnitOfEnergy.WATT_HOUR, "icon": "mdi:current-dc", "device_type": 14, "device_class": SensorDeviceClass.ENERGY, "state_class": SensorStateClass.TOTAL_INCREASING},
    "p13125": {"name": "Total Feed-In Energy", "unit": UnitOfEnergy.WATT_HOUR, "icon": "mdi:current-dc", "device_type": 14, "device_class": SensorDeviceClass.ENERGY, "state_class": SensorStateClass.TOTAL_INCREASING},
    "p13147": {"name": "Energy Purchased Today", "unit": UnitOfEnergy.WATT_HOUR, "icon": "mdi:current-dc", "device_type": 14, "device_class": SensorDeviceClass.ENERGY, "state_class": SensorStateClass.TOTAL_INCREASING},
    "p13148": {"name": "Total Purchased Energy", "unit": UnitOfEnergy.WATT_HOUR, "icon": "mdi:current-dc", "device_type": 14, "device_class": SensorDeviceClass.ENERGY, "state_class": SensorStateClass.TOTAL_INCREASING},
    "p13149": {"name": "Purchased Power", "unit": UnitOfPower.WATT, "icon": "mdi:flash", "device_type": 14, "device_class": SensorDeviceClass.POWER, "state_class": SensorStateClass.MEASUREMENT},
    "p13121": {"name": "Feed-In Power", "unit": UnitOfPower.WATT, "icon": "mdi:flash", "device_type": 14, "device_class": SensorDeviceClass.POWER, "state_class": SensorStateClass.MEASUREMENT},
    "p13173": {"name": "PV Feed-in Energy Today", "unit": UnitOfEnergy.WATT_HOUR, "icon": "mdi:solar-power", "device_type": 14, "device_class": SensorDeviceClass.ENERGY, "state_class": SensorStateClass.TOTAL_INCREASING},
    "p13175": {"name": "PV Total Feed-in Energy", "unit": UnitOfEnergy.WATT_HOUR, "icon": "mdi:solar-power", "device_type": 14, "device_class": SensorDeviceClass.ENERGY, "state_class": SensorStateClass.TOTAL_INCREASING},
    "p13019": {"name": "Internal Air Temperature", "unit": UnitOfTemperature.CELSIUS, "icon": "mdi:thermometer-lines", "device_type": 14, "device_class": SensorDeviceClass.TEMPERATURE, "state_class": SensorStateClass.MEASUREMENT},

    # 🔹 Battery (device_type 43)
    "p13141": {"name": "Battery Level SOC", "unit": PERCENTAGE, "icon": "mdi:battery", "device_type": 43, "device_class": SensorDeviceClass.BATTERY, "state_class": SensorStateClass.MEASUREMENT},
    "p13029": {"name": "Battery Discharging Energy Today", "unit": UnitOfEnergy.WATT_HOUR, "icon": "mdi:battery-minus", "device_type": 43, "device_class": SensorDeviceClass.ENERGY, "state_class": SensorStateClass.TOTAL_INCREASING},
    "p13028": {"name": "Battery Charging Energy Today", "unit": UnitOfEnergy.WATT_HOUR, "icon": "mdi:battery-plus", "device_type": 43, "device_class": SensorDeviceClass.ENERGY, "state_class": SensorStateClass.TOTAL_INCREASING},
    "p13138": {"name": "Battery Voltage", "unit": UnitOfElectricPotential.VOLT, "icon": "mdi:battery", "device_type": 43, "device_class": SensorDeviceClass.VOLTAGE, "state_class": SensorStateClass.MEASUREMENT},
    "p13139": {"name": "Battery Current", "unit": UnitOfElectricCurrent.AMPERE, "icon": "mdi:current-dc", "device_type": 43, "device_class": SensorDeviceClass.CURRENT, "state_class": SensorStateClass.MEASUREMENT},
    "p13035": {"name": "Total Battery Discharging Energy", "unit": UnitOfEnergy.WATT_HOUR, "icon": "mdi:battery-minus", "device_type": 43, "device_class": SensorDeviceClass.ENERGY, "state_class": SensorStateClass.TOTAL_INCREASING},
    "p13034": {"name": "Total Battery Charging Energy", "unit": UnitOfEnergy.WATT_HOUR, "icon": "mdi:battery-plus", "device_type": 43, "device_class": SensorDeviceClass.ENERGY, "state_class": SensorStateClass.TOTAL_INCREASING},
    "p13142": {"name": "Battery Health SOH", "unit": PERCENTAGE, "icon": "mdi:battery-heart", "device_type": 43, "device_class": SensorDeviceClass.BATTERY, "state_class": SensorStateClass.MEASUREMENT},
    "p13143": {"name": "Battery Temperature", "unit": UnitOfTemperature.CELSIUS, "icon": "mdi:thermometer-lines", "device_type": 43, "device_class": SensorDeviceClass.TEMPERATURE, "state_class": SensorStateClass.MEASUREMENT},
    "p13162": {"name": "BMS Max Charging Current", "unit": UnitOfElectricCurrent.AMPERE, "icon": "mdi:current-dc", "device_type": 43, "device_class": SensorDeviceClass.CURRENT, "state_class": SensorStateClass.MEASUREMENT},
    "p13163": {"name": "BMS Max Discharging Current", "unit": UnitOfElectricCurrent.AMPERE, "icon": "mdi:current-dc", "device_type": 43, "device_class": SensorDeviceClass.CURRENT, "state_class": SensorStateClass.MEASUREMENT},
    "p13174": {"name": "Daily Battery Charging Energy from PV", "unit": UnitOfEnergy.WATT_HOUR, "icon": "mdi:battery-charging", "device_type": 43, "device_class": SensorDeviceClass.ENERGY, "state_class": SensorStateClass.TOTAL_INCREASING},
    "p13176": {"name": "Total Battery Charging Energy from PV", "unit": UnitOfEnergy.WATT_HOUR, "icon": "mdi:battery-charging", "device_type": 43, "device_class": SensorDeviceClass.ENERGY, "state_class": SensorStateClass.TOTAL_INCREASING},
    "p13126": {"name": "Battery Charging Power", "unit": UnitOfPower.WATT, "icon": "mdi:battery-plus", "device_type": 43, "device_class": SensorDeviceClass.POWER, "state_class": SensorStateClass.MEASUREMENT},
    "p13150": {"name": "Battery Discharging Power", "unit": UnitOfPower.WATT, "icon": "mdi:battery-minus", "device_type": 43, "device_class": SensorDeviceClass.POWER, "state_class": SensorStateClass.MEASUREMENT},
    "p13140": {"name": "Battery Capacity kWh", "unit": UnitOfEnergy.KILO_WATT_HOUR, "icon": "mdi:battery", "device_type": 43, "device_class": SensorDeviceClass.ENERGY, "state_class": SensorStateClass.TOTAL_INCREASING},

    # 🔹 Smart Meter / Energy Meter (device_type 7)
    "p18108": {"name": "Meter Phase A Voltage", "unit": UnitOfElectricPotential.VOLT, "icon": "mdi:solar-panel", "device_type": 7, "device_class": SensorDeviceClass.VOLTAGE, "state_class": SensorStateClass.MEASUREMENT},
    "p18109": {"name": "Meter Phase B Voltage", "unit": UnitOfElectricPotential.VOLT, "icon": "mdi:solar-panel", "device_type": 7, "device_class": SensorDeviceClass.VOLTAGE, "state_class": SensorStateClass.MEASUREMENT},
    "p18110": {"name": "Meter Phase C Voltage", "unit": UnitOfElectricPotential.VOLT, "icon": "mdi:solar-panel", "device_type": 7, "device_class": SensorDeviceClass.VOLTAGE, "state_class": SensorStateClass.MEASUREMENT}
}
