class NestDataExtraction:
    @staticmethod
    def get_temperature(device):
        return device["traits"]["sdm.devices.traits.Temperature"][
            "ambientTemperatureCelsius"
        ]

    @staticmethod
    def get_thermostat_mode(device):
        return device["traits"]["sdm.devices.traits.ThermostatMode"]["mode"]

    @staticmethod
    def get_thermostat_hvac_status(device):
        return device["traits"]["sdm.devices.traits.ThermostatHvac"]["status"]

    @staticmethod
    def get_thermostat_temp_set_points_heat(device):
        return device["traits"]["sdm.devices.traits.ThermostatTemperatureSetpoint"][
            "heatCelsius"
        ]

    @staticmethod
    def get_thermostat_temp_set_points_cool(device):
        return device["traits"]["sdm.devices.traits.ThermostatTemperatureSetpoint"][
            "coolCelsius"
        ]

    @staticmethod
    def convert_celsius_to_fahrenheit(celsius_temp):
        return (celsius_temp * 9 / 5) + 32
