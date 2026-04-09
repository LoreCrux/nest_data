from app.database.connection import insert_reading, create_table
from app.auth.auth import fetch_devices
from app.helpers.thermo_helpers import NestDataExtraction


def main():
    create_table("thermostat_readings", "idx_thermostat")
    try:
        readings = fetch_devices()
    except RuntimeError as e:
        print(f"Failed to fetch devices: {e}")
        return
    if not readings:
        print("No devices returned from API")
        return
    reading = readings[0]
    insert_reading(
        NestDataExtraction.convert_celsius_to_fahrenheit(reading["current_temperature"]),
        NestDataExtraction.convert_celsius_to_fahrenheit(reading["set_point_heat"]),
        NestDataExtraction.convert_celsius_to_fahrenheit(reading["set_point_cool"]),
        reading["mode"],
        reading["status"],
    )


if __name__ == "__main__":
    main()
