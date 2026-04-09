class NestDataExtraction:
    @staticmethod
    def get_temperature(device):
        trait = device.get("traits", {}).get("sdm.devices.traits.Temperature", {})
        return trait.get("ambientTemperatureCelsius")

    @staticmethod
    def get_thermostat_mode(device):
        trait = device.get("traits", {}).get("sdm.devices.traits.ThermostatMode", {})
        return trait.get("mode")

    @staticmethod
    def get_thermostat_hvac_status(device):
        trait = device.get("traits", {}).get("sdm.devices.traits.ThermostatHvac", {})
        return trait.get("status")

    @staticmethod
    def get_thermostat_temp_set_points_heat(device):
        trait = device.get("traits", {}).get("sdm.devices.traits.ThermostatTemperatureSetpoint", {})
        return trait.get("heatCelsius")

    @staticmethod
    def get_thermostat_temp_set_points_cool(device):
        trait = device.get("traits", {}).get("sdm.devices.traits.ThermostatTemperatureSetpoint", {})
        return trait.get("coolCelsius")

    @staticmethod
    def convert_celsius_to_fahrenheit(celsius_temp):
        return (celsius_temp * 9 / 5) + 32
