from homeassistant.components.sensor import SensorEntity, SensorDeviceClass, SensorStateClass 
from homeassistant.helpers.update_coordinator import ( 
    DataUpdateCoordinator, 
    UpdateFailed, 
    CoordinatorEntity 
) 
from homeassistant.core import HomeAssistant 
from homeassistant.helpers.entity import DeviceInfo, EntityCategory 
from homeassistant.const import UnitOfEnergy, UnitOfPower, UnitOfMass 
from homeassistant.exceptions import ConfigEntryNotReady 
from datetime import timedelta 
from homeassistant.exceptions import ConfigEntryNotReady 
from .const import ENERGY_STORAGE_SYS_NAME_POINT_MAP 
from .const import PLANT_TYPE_MAP 
from .const import BUILD_STATUS_MAP 
from .const import FAULT_STATUS_MAP 
from .const import PLANT_STATUS_MAP 
from .const import PLANT_SHARE_TYPE_MAP 
from .const import GRID_CONNECTION_TYPE_MAP 
from .const import DEVICE_FAULT_STATUS_MAP 
from .const import COMMON_MEASURING_PLANT_POINTS_MAP

import logging

_LOGGER = logging.getLogger(__name__)
DOMAIN = "sungrow_isolar"

async def async_setup_entry(hass: HomeAssistant, entry, async_add_entities):
    """Set up Sungrow iSolar integration from a config entry."""
    api = hass.data[DOMAIN][entry.entry_id]["api"]

    async def async_update_data():
         """Fetch latest data for the plant and all devices."""
        try:
            plant_data = await api.get_plant_data()
            device_list = await api.get_device_list()
            realtime_data = await api.get_all_devices_realtime_data(device_list)
            
            # 🔹 adaugă și datele plant în coordinator
            ps_id = (
                plant_data.get("result_data", {})
                .get("pageList", [{}])[0]
                .get("ps_id")
            )
            plant_realtime = await api.get_plant_realtime_data(ps_id) if ps_id else {}
            
            return {
                "plant_data": plant_data,
                "device_list": device_list,
                "realtime_data": realtime_data,
                "plant_realtime": plant_realtime
            }
        except Exception as err:
            raise UpdateFailed(f"Error fetching data: {err}")

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="Sungrow PowerStation Data",
        update_method=async_update_data,
        update_interval=timedelta(minutes=5),
    )
    
    # Perform first data fetch
    await coordinator.async_config_entry_first_refresh()

    data = coordinator.data or {}
    plant_data = data.get("plant_data", {})
    page_list = plant_data.get("result_data", {}).get("pageList", [])
    
    ps_name = page_list[0].get("ps_name") if page_list else "Sungrow Plant"
    ps_id = page_list[0].get("ps_id") if page_list else None
    model_raw = int(page_list[0].get("ps_type", 0)) if page_list else 0
    model_value = PLANT_TYPE_MAP.get(model_raw, "Unknown")
    req_serial = page_list[0].get("req_serial_num") if page_list else None
    
    plant_device_info = DeviceInfo(
        identifiers={(DOMAIN, f"plant_{ps_id}")},
        name=ps_name,
        manufacturer="Sungrow",
        model=model_value,
        serial_number=req_serial,
    )

    # Create entities for the Solar Plant itself
    entities = [
        SungrowCurrentPowerSensor(coordinator, entry.entry_id, plant_device_info),
        SungrowPlantAlarmCount(coordinator, entry.entry_id, plant_device_info),
        SungrowPlantCapacity(coordinator, entry.entry_id, plant_device_info),
        SungrowPlantFaultStatus(coordinator, entry.entry_id, plant_device_info),
        SungrowPlantShareStatus(coordinator, entry.entry_id, plant_device_info),
        SungrowPlantStatus(coordinator, entry.entry_id, plant_device_info),
        SungrowPlantBuildStatus(coordinator, entry.entry_id, plant_device_info),
        SungrowTotalEnergySensor(coordinator, entry.entry_id, plant_device_info),
        SungrowTotalCO2Sensor(coordinator, entry.entry_id, plant_device_info),
        SungrowTodayEnergySensor(coordinator, entry.entry_id, plant_device_info)
    ]

    # Fetch the list of devices for the plant
    try:
        device_list = await api.get_device_list()
        _LOGGER.debug("Found %s devices for plant %s", len(device_list), ps_name)
    except Exception as e:
        _LOGGER.error("Failed to fetch device list: %s", e)
        device_list = []
    
    # Add real-time plant sensors
    plant_ps_id = plant_data.get("result_data", {}).get("pageList", [{}])[0].get("ps_id")

    if plant_ps_id:
        plant_realtime = await api.get_plant_realtime_data(plant_ps_id)
    
        for point_key, value in plant_realtime.items():
            point_info = COMMON_MEASURING_PLANT_POINTS_MAP.get(point_key)
            if not point_info:
                continue
    
            entities.append(
                SungrowPlantRealtimeSensor(
                    coordinator=coordinator,
                    entry_id=entry.entry_id,
                    device_info=plant_device_info,
                    point_key=point_key,
                    point_info=point_info,
                    initial_value=value,
                )
            )
    
    
    # Fetch real-time data for all devices
    try:
        all_realtime_data = await api.get_all_devices_realtime_data(device_list)
    except Exception as e:
        _LOGGER.error("Failed to fetch realtime data for all devices: %s", e)
        all_realtime_data = {}

    # Create sensors for each device
    for dev in device_list:
        device_sn = dev.get("device_sn") or str(dev.get("uuid"))
        device_name = dev.get("device_name", "Unnamed Device")
        device_model = dev.get("device_model_code", "Unknown Model")
        manufacturer = dev.get("factory_name", "Sungrow")
        device_type = int(dev.get("device_type", 0))
        ps_key = dev.get("ps_key")

        device_info = DeviceInfo(
            identifiers={(DOMAIN, device_sn)},
            name=device_name,
            manufacturer=manufacturer,
            model=device_model,
            via_device=(DOMAIN, f"plant_{ps_id}"),
        )

        # Add a sensor for the device status
        entities.append(SungrowDeviceStatusSensor(coordinator, entry.entry_id, device_info, dev))

        # Add real-time point sensors for the device
        device_data = all_realtime_data.get(ps_key, {})

        for point_key, value in all_realtime_data.items():
            point_info = ENERGY_STORAGE_SYS_NAME_POINT_MAP.get(point_key)
            if not point_info or point_info.get("device_type") != device_type:
                continue
        
            device_sn = dev.get("device_sn") or str(dev.get("uuid"))
        
            entities.append(
                SungrowRealtimePointSensor(
                    coordinator,
                    entry.entry_id,
                    device_info,
                    device_sn,
                    device_name,
                    point_key
                )
            )

    async_add_entities(entities)


# ========================
# Solar Plant Sensors
# ========================
class SungrowCurrentPowerSensor(CoordinatorEntity, SensorEntity):
    """Sensor for current solar plant power output in real-time."""
    def __init__(self, coordinator, entry_id, device_info):
        super().__init__(coordinator)
        self._attr_name = "Solar Power Now"
        self._attr_device_class = SensorDeviceClass.POWER
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_icon = "mdi:solar-power"
        self._attr_unique_id = f"{entry_id}_current_power"
        self._attr_device_info = device_info
    
    @property
    def native_unit_of_measurement(self):
        """Return the unit for current power measurement, defaulting to Watts."""
        try: 
            plant_data = self.coordinator.data.get("plant_data", {})
            page = plant_data.get("result_data", {}).get("pageList", []) 
            if page and "curr_power" in page[0]: 
                return page[0]["curr_power"].get("unit", "W") 
        except Exception as err:
            _LOGGER.warning("Error reading unit for current power: %s", err) 
        return "W"
    
    @property
    def native_value(self):
        """Return the current power value in Watts."""
        try:
            plant_data = self.coordinator.data.get("plant_data", {})
            page = plant_data.get("result_data", {}).get("pageList", [])
            if page and "curr_power" in page[0]:
                return float(page[0]["curr_power"]["value"])
        except Exception as err:
            _LOGGER.warning("Error parsing current power: %s", err)
        return None

class SungrowPlantAlarmCount(CoordinatorEntity, SensorEntity):
    """Sensor representing the total number of alarms on the solar plant."""
    def __init__(self, coordinator, entry_id, device_info):
        super().__init__(coordinator)
        self._attr_name = "Total Solar Plant Alarms"
        self._attr_icon = "mdi:alarm-light"
        self._attr_entity_category = EntityCategory.DIAGNOSTIC
        self._attr_unique_id = f"{entry_id}_alarm_count"
        self._attr_device_info = device_info

    @property
    def native_value(self):
        """Return the number of active alarms on the plant."""
        try:
            plant_data = self.coordinator.data.get("plant_data", {})
            page = plant_data.get("result_data", {}).get("pageList", [])
            if page and "alarm_count" in page[0]:
                return page[0]["alarm_count"]
        except Exception as err:
            _LOGGER.warning("Error parsing alarm count: %s", err)
        return None

class SungrowPlantCapacity(CoordinatorEntity, SensorEntity):
    """Sensor representing the total installed capacity of the solar plant."""
    def __init__(self, coordinator, entry_id, device_info):
        super().__init__(coordinator)
        self._attr_name = "Solar Plant Capacity"
        self._attr_native_unit_of_measurement = "kWp"
        self._attr_entity_category = EntityCategory.DIAGNOSTIC
        self._attr_icon = "mdi:view-split-horizontal"
        self._attr_unique_id = f"{entry_id}_total_capcity"
        self._attr_device_info = device_info

    @property
    def native_value(self):
        """Return the total capacity of the solar plant in kWp."""
        try:
            plant_data = self.coordinator.data.get("plant_data", {})
            page = plant_data.get("result_data", {}).get("pageList", [])
            if page and "total_capcity" in page[0]:
                return float(page[0]["total_capcity"]["value"])
        except Exception as err:
            _LOGGER.warning("Error parsing Total Capacity: %s", err)
        return None

class SungrowPlantFaultStatus(CoordinatorEntity, SensorEntity):
    """Sensor representing the current fault status of the solar plant."""
    def __init__(self, coordinator, entry_id, device_info):
        super().__init__(coordinator)
        self._attr_name = "Plant Fault Status"
        self._attr_icon = "mdi:home-search-outline"
        self._attr_entity_category = EntityCategory.DIAGNOSTIC
        self._attr_unique_id = f"{entry_id}_ps_fault_status"
        self._attr_device_info = device_info

    @property
    def native_value(self):
        """Return the human-readable fault status of the plant."""
        try:
            plant_data = self.coordinator.data.get("plant_data", {})
            page = plant_data.get("result_data", {}).get("pageList", [])
            if page and "ps_fault_status" in page[0]:
                val = int(page[0]["ps_fault_status"])
                return FAULT_STATUS_MAP.get(val, "Unknown")
        except Exception as err:
            _LOGGER.warning("Error parsing fault status: %s", err)
        return None

class SungrowPlantShareStatus(CoordinatorEntity, SensorEntity): 
    def __init__(self, coordinator, entry_id, device_info): 
        super().__init__(coordinator) 
        self._attr_name = "Share Type" 
        self._attr_icon = "mdi:folder-account" 
        self._attr_entity_category = EntityCategory.DIAGNOSTIC 
        self._attr_unique_id = f"{entry_id}_share_type" 
        self._attr_device_info = device_info 
        
        @property 
        def native_value(self): 
            try: 
                plant_data = self.coordinator.data.get("plant_data", {}) 
                page = plant_data.get("result_data", {}).get("pageList", []) 
                if page and "share_type" in page[0]: 
                    val = int(page[0]["share_type"]) 
                    return PLANT_SHARE_TYPE_MAP.get(val, "Unknown") 
            except Exception as err: 
                _LOGGER.warning("Error parsing share type: %s", err) 
            return None

class SungrowPlantStatus(CoordinatorEntity, SensorEntity): 
    """Sensor representing the sharing type/status of the plant."""
    def __init__(self, coordinator, entry_id, device_info): 
        super().__init__(coordinator) 
        self._attr_name = "Plant Status" 
        self._attr_icon = "mdi:connection" 
        self._attr_entity_category = EntityCategory.DIAGNOSTIC 
        self._attr_unique_id = f"{entry_id}_valid_flag" 
        self._attr_device_info = device_info 
    
    @property 
    def native_value(self): 
        """Return the sharing type of the plant."""
        try: 
            plant_data = self.coordinator.data.get("plant_data", {}) 
            page = plant_data.get("result_data", {}).get("pageList", []) 
            if page and "valid_flag" in page[0]: 
                val = int(page[0]["valid_flag"]) 
                return PLANT_STATUS_MAP.get(val, "Unknown") 
        except Exception as err: 
            _LOGGER.warning("Error parsing fault status: %s", err) 
        return None

class SungrowPlantBuildStatus(CoordinatorEntity, SensorEntity):
    """Sensor representing the construction or build status of the plant."""
    def __init__(self, coordinator, entry_id, device_info):
        super().__init__(coordinator)
        self._attr_name = "Plant Construction Status"
        self._attr_entity_category = EntityCategory.DIAGNOSTIC
        self._attr_icon = "mdi:hammer-wrench"
        self._attr_unique_id = f"{entry_id}_build_status"
        self._attr_device_info = device_info

    @property
    def native_value(self):
        """Return the plant construction status in human-readable format."""
        try:
            plant_data = self.coordinator.data.get("plant_data", {})
            page = plant_data.get("result_data", {}).get("pageList", [])
            if page and "build_status" in page[0]:
                val = int(page[0]["build_status"])
                return BUILD_STATUS_MAP.get(val, "Unknown")
        except Exception as err:
            _LOGGER.warning("Error parsing plant build status: %s", err)
        return None

class SungrowTotalEnergySensor(CoordinatorEntity, SensorEntity):
    """Sensor for total energy produced by the solar plant."""
    def __init__(self, coordinator, entry_id, device_info):
        super().__init__(coordinator)
        self._attr_name = "Total Produced Energy"
        self._attr_device_class = SensorDeviceClass.ENERGY 
        self._attr_state_class = SensorStateClass.TOTAL_INCREASING
        self._attr_icon = "mdi:lightning-bolt"
        self._attr_unique_id = f"{entry_id}_total_energy"
        self._attr_device_info = device_info
    
    @property 
    def native_unit_of_measurement(self): 
        """Return the unit of total energy produced, defaulting to Wh."""
        try: 
            plant_data = self.coordinator.data.get("plant_data", {}) 
            page = plant_data.get("result_data", {}).get("pageList", []) 
            if page and "total_energy" in page[0]: 
                return page[0]["total_energy"].get("unit", "W") 
        except Exception as err: 
            _LOGGER.warning("Error reading unit for current power: %s", err) 
        return "W"
    
    @property
    def native_value(self):
        """Return the total energy produced."""
        try:
            plant_data = self.coordinator.data.get("plant_data", {})
            page = plant_data.get("result_data", {}).get("pageList", [])
            if page and "total_energy" in page[0]:
                return float(page[0]["total_energy"]["value"])
        except Exception as err:
            _LOGGER.warning("Error parsing Total Energy: %s", err)
        return None

class SungrowTotalCO2Sensor(CoordinatorEntity, SensorEntity): 
    """Sensor for the total CO₂ reduction achieved by the plant."""
    def __init__(self, coordinator, entry_id, device_info): 
        super().__init__(coordinator) 
        self._attr_name = "Total CO₂ reduced" 
        self._attr_native_unit_of_measurement = UnitOfMass.KILOGRAMS 
        self._attr_state_class = SensorStateClass.MEASUREMENT 
        self._attr_icon = "mdi:molecule-co2" 
        self._attr_unique_id = f"{entry_id}_co2_reduce_total" 
        self._attr_device_info = device_info 
    
    @property 
    def native_value(self): 
        """Return total CO₂ reduction in kilograms."""
        try: 
            plant_data = self.coordinator.data.get("plant_data", {}) 
            page = plant_data.get("result_data", {}).get("pageList", []) 
            if page and "co2_reduce_total" in page[0]: 
                return float(page[0]["co2_reduce_total"]["value"]) 
        except Exception as err: 
            _LOGGER.warning("Error parsing co2_reduce_total value: %s", err) 
        return None

class SungrowTodayCO2Sensor(CoordinatorEntity, SensorEntity): 
    
    def __init__(self, coordinator, entry_id, device_info): 
        super().__init__(coordinator) 
        self._attr_name = "Today CO₂ Reduction" 
        self._attr_native_unit_of_measurement = UnitOfMass.KILOGRAMS 
        self._attr_state_class = SensorStateClass.MEASUREMENT 
        self._attr_icon = "mdi:leaf" 
        self._attr_unique_id = f"{entry_id}_co2_reduce" 
        self._attr_device_info = device_info 
    
    @property 
    def native_value(self): 
        """Return total energy produced today in kWh."""
        try: 
            plant_data = self.coordinator.data.get("plant_data", {}) 
            page = plant_data.get("result_data", {}).get("pageList", []) 
            if page and "co2_reduce" in page[0]: 
                return float(page[0]["co2_reduce"]["value"]) 
        except Exception as err: 
            _LOGGER.warning("Error parsing co2_reduce value: %s", err) 
        return None

class SungrowTodayEnergySensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, entry_id, device_info):
        super().__init__(coordinator)
        self._attr_name = "Today Total Energy"
        self._attr_native_unit_of_measurement = UnitOfEnergy.KILO_WATT_HOUR
        self._attr_device_class = SensorDeviceClass.ENERGY 
        self._attr_state_class = SensorStateClass.TOTAL_INCREASING
        self._attr_icon = "mdi:sun-clock"
        self._attr_unique_id = f"{entry_id}_today_energy"
        self._attr_device_info = device_info

    @property
    def native_value(self):
        try:
            plant_data = self.coordinator.data.get("plant_data", {})
            page = plant_data.get("result_data", {}).get("pageList", [])
            if page and "today_energy" in page[0]:
                return float(page[0]["today_energy"]["value"])
        except Exception as err:
            _LOGGER.warning("Error parsing Today Energy: %s", err)
        return None

# Set Device Sensors
class SungrowDeviceStatusSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, entry_id, device_info, device):
        super().__init__(coordinator)
        self._device = device
        self._attr_name = f"{device.get('device_name', 'Unnamed Device')} Status"
        self._attr_unique_id = f"{entry_id}_{device.get('device_sn', device.get('uuid'))}_status"
        self._attr_entity_category = EntityCategory.DIAGNOSTIC
        self._attr_icon = "mdi:power-plug"
        self._attr_device_info = device_info

    @property
    def native_value(self):
        status = int(self._device.get("dev_fault_status", "0"))
        return DEVICE_FAULT_STATUS_MAP.get(status, "Unknown")

class SungrowPlantRealtimeSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, entry_id, device_info, point_key, point_info, initial_value):
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry_id}_plant_{point_key}"
        self._attr_device_info = device_info
        self._attr_name = point_info.get("name")
        self._attr_device_class = point_info.get("device_class")
        self._attr_state_class = point_info.get("state_class")
        self._attr_native_unit_of_measurement = point_info.get("unit")
        self._attr_icon = point_info.get("icon")
        self._point_key = point_key
        self._value = initial_value

    @property
    def native_value(self):
        # Returnează ultima valoare stocată din coordinator
        all_data = self.coordinator.data.get("plant_realtime", {})
        return all_data.get(self._point_key, self._value)

class SungrowRealtimePointSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, entry_id, device_info, device_sn, device_name, point_key):
        super().__init__(coordinator)
        self._point_key = point_key
        self._device_sn = device_sn
        self._device_name = device_name

        point_info = ENERGY_STORAGE_SYS_NAME_POINT_MAP.get(point_key, {})
        name = point_info.get("name", point_key)
        self._attr_name = f"{device_name} {name}"
        self._attr_icon = point_info.get("icon", "mdi:gauge")
        self._attr_device_class = point_info.get("device_class")
        self._attr_state_class = point_info.get("state_class")
        self._attr_native_unit_of_measurement = point_info.get("unit")
        self._attr_device_info = device_info

        # Using serial/device_sn for unique_id and not "unknown"
        self._attr_unique_id = f"{entry_id}_{device_sn}_{point_key}"

    @property
    def native_value(self):
        try:
            # Read updated data from coordinator
            all_data = self.coordinator.data.get("realtime_data", {})
            value = all_data.get(self._point_key)
            
            if isinstance(value, str) and value.replace(".", "", 1).isdigit():
                value = float(value)
            elif isinstance(value, (int, float)):
                value = float(value)
            else:
                return value  # if not numeric, return raw

            # Battery SOC and Battery SOH must be converted in percent
            if self._point_key in ["p13141", "p13142"]:  # SOC și SOH
                return round(value * 100, 1)  # ex: 0.378 -> 37.8
            
            return value
        except Exception as err:
            _LOGGER.warning("Error parsing value for %s: %s", self._attr_name, err)
        return None
