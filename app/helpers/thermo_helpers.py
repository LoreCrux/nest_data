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
    def get_thermostat_temp_set_points(device):
        return (
            device["traits"]["sdm.devices.traits.ThermostatTemperatureSetpoint"][
                "heatCelsius"
            ],
            ["coolCelsius"],
        )
