import aiohttp
import async_timeout
import logging

_LOGGER = logging.getLogger(__name__)

class SungrowAPI:
    """Asynchronous API client for Sungrow iSolarCloud."""

    def __init__(self, appkey, secret, username, password, base_url="https://gateway.isolarcloud.eu/"):
        """Initialize the API client."""
        self.appkey = appkey
        self.secret = secret
        self.username = username
        self.password = password
        self.token = None
        self.ps_id = None
        self.base_url = base_url.rstrip("/")  # Remove trailing slash if present
        
    async def login(self):
        """Authenticate with Sungrow iSolar Cloud and retrieve token."""
        url = f"{self.base_url}/openapi/login"
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Home Assistant",
            "x-access-key": self.secret
        }
        payload = {
            "appkey": self.appkey, "user_account": self.username, "user_password": self.password,
        }

        timeout = aiohttp.ClientTimeout(total=20)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with async_timeout.timeout(15):
                async with session.post(url, json=payload, headers=headers) as resp:
                    data = await resp.json()
                    token = data.get("result_data", {}).get("token")
                    if token:
                        self.token = token
                        _LOGGER.debug("Login successful, token=%s", self.token)
                        return self.token
                    else:
                        _LOGGER.error("Login failed: %s", data)
                        return None

    async def _post_with_token_retry(self, url, payload, headers):
        """Perform a POST request, retrying once if the token is invalid or expired."""
        timeout = aiohttp.ClientTimeout(total=20)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with async_timeout.timeout(15):
                async with session.post(url, json=payload, headers=headers) as resp:
                    data = await resp.json()

                    # Detect token expiration or invalid token errors
                    if (
                        data.get("result_code") in ["1002", "1003", "1004"]
                        or "token" in str(data).lower() and "invalid" in str(data).lower()
                    ):
                        _LOGGER.warning("Token expired or invalid, refreshing token...")
                        await self.login()
                        headers["token"] = self.token
                        async with aiohttp.ClientSession() as retry_session:
                            async with retry_session.post(url, json=payload, headers=headers) as retry_resp:
                                return await retry_resp.json()

                    return data
                    
    async def get_plant_data(self):
        """Fetch plant information such as power station list and details."""
        if not self.token:
            await self.login()

        url = f"{self.base_url}/openapi/getPowerStationList"
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Home Assistant",
            "x-access-key": self.secret,
            "token": self.token,
        }
        payload = {
            "appkey": self.appkey, 
            "curPage": 1, 
            "size": 10,
            "lang": "_en_US"
        }

        timeout = aiohttp.ClientTimeout(total=20)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with async_timeout.timeout(15):
                async with session.post(url, json=payload, headers=headers) as resp:
                    data = await resp.json()
                    page_list = data.get("result_data", {}).get("pageList", [])
                    if page_list:
                        self.ps_id = page_list[0].get("ps_id")
                    return data

    async def get_device_list(self):
        """Return the list of devices associated with the user."""
        if not self.token:
            await self.login()
        if not self.ps_id:
            await self.get_plant_data()

        url = f"{self.base_url}/openapi/getDeviceListByUser"
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Home Assistant",
            "x-access-key": self.secret,
            "token": self.token,
        }
        payload = {
            "appkey": self.appkey, 
            "curPage": "1", 
            "size": "100",
            "lang": "_en_US"
        }

        async with aiohttp.ClientSession() as session:
            async with async_timeout.timeout(15):
                async with session.post(url, json=payload, headers=headers) as resp:
                    data = await resp.json()
                    return data.get("result_data", {}).get("pageList", [])

    async def get_device_realtime_data(self, device_type: int, ps_key: str):
        """Fetch realtime data for a specific device."""
        if not self.token:
            await self.login()
        
        url = f"{self.base_url}/openapi/getDeviceRealTimeData"
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Home Assistant",
            "x-access-key": self.secret,
            "token": self.token,
        }

        payload = {
            "appkey": self.appkey,
            "device_type": device_type,
            "ps_key_list": [ps_key],
            "lang": "_en_US"
        }

        async with aiohttp.ClientSession() as session:
            async with async_timeout.timeout(15):
                async with session.post(url, json=payload, headers=headers) as resp:
                    data = await resp.json()
                    return data.get("result_data", {}).get("device_point_list", [])
    
    async def get_plant_realtime_data(self, ps_id: str):
        """Return real-time data for the plant (device_type=11)."""
        url = f"{self.base_url}/openapi/getDeviceRealTimeData"
        
        # Specific point IDs to query for the plant
        plant_point_id_list = [
            "83106",
            "83118",
            "83124",
            "83072",
            "83102"
        ]
        
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Home Assistant",
            "x-access-key": self.secret,
            "token": self.token
        }
        
        payload = {
            "appkey": self.appkey,
            "device_type": 11,
            "lang": "_en_US",
            "point_id_list": plant_point_id_list,
            "ps_key_list": [f"{ps_id}_11_0_0"]
        }
    
        try:
            timeout = aiohttp.ClientTimeout(total=20)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.post(url, json=payload, headers=headers) as response:
                    data = await response.json()
                    if data.get("result_code") != "1":
                        _LOGGER.warning("API error for getDeviceRealTimeData: %s", data)
                        return {}
        
                    result = {}
                    for dev in data.get("result_data", {}).get("device_point_list", []):
                        points = dev.get("device_point", {})
                        # Extract all available pXXXX values from response
                        for key, value in points.items():
                            if key.startswith("p"):
                                result[key] = float(value)
                    return result
        except Exception as err:
            _LOGGER.error("Error calling getDeviceRealTimeData: %s", err)
        return {}
        
    async def get_all_devices_realtime_data(self, device_list):
        """Collect real-time data for all devices in the plant."""
        results = {}
        if not self.token:
            await self.login()
        
        # List of measurement point IDs used for inverter data
        point_id_list = [
            "13003","13011","13012","13013",
            "13157","13158","13159",
            "13008","13009","13010",
            "13007",
            "13112","13134",
            "13161",
            "13001","13105",
            "13002","13106",
            "13122","13125",
            "13147","13148",
            "13149","13121",
            "13173","13175",
            "13019",
            "13141","13029","13028","13138","13139",
            "13035","13034","13142","13143","13162","13163",
            "13174","13176","13126","13150","13140",
            "18108","18109","18110"
        ]
        
        # Identify the inverter (device_type=14)
        inverter = next((d for d in device_list if int(d.get("device_type", 0)) == 14), None)
        if not inverter:
            _LOGGER.error("No inverter found (device_type=14)")
            return results
    
        ps_key_inverter = inverter.get("ps_key")
        if not ps_key_inverter:
            _LOGGER.error("Inverter ps_key not found")
            return results
    
        timeout = aiohttp.ClientTimeout(total=20)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            for device in device_list:
                ps_key = device.get("ps_key")
                device_type = int(device.get("device_type", 0))
    
                if not ps_key:
                    _LOGGER.warning("Skipping device with no ps_key: %s", device)
                    continue
    
                url = f"{self.base_url}/openapi/getDeviceRealTimeData"
                headers = {
                    "Content-Type": "application/json",
                    "User-Agent": "Home Assistant",
                    "x-access-key": self.secret,
                    "token": self.token,
                }
                payload = {
                    "appkey": self.appkey,
                    "device_type": 14,
                    "ps_key_list": [ps_key_inverter],
                    "point_id_list": point_id_list,
                    "lang": "_en_US"
                }
    
                try:
                    async with async_timeout.timeout(15):
                        async with session.post(url, json=payload, headers=headers) as resp:
                            data = await resp.json()
                            if data.get("result_code") != "1":
                                _LOGGER.error("Realtime fetch failed: %s", data.get("result_msg"))
                                continue
    
                            device_point_list = data.get("result_data", {}).get("device_point_list", [])
                            if device_point_list:
                                device_points = device_point_list[0].get("device_point", {})
                                for point_key, value in device_points.items():
                                    results[point_key] = value
    
                except Exception as e:
                    _LOGGER.error("Error fetching realtime data: %s", e)
    
            _LOGGER.debug("Collected realtime results for %d points", len(results))
            return results
    
