from app.database.connection import insert_reading, create_table
from app.auth.auth import get_data
from app.helpers.thermo_helpers import NestDataExtraction


def main():
    create_table("thermostat_readings", "idx_thermostat")
    reading = get_data()
    insert_reading(
        NestDataExtraction.convert_celsius_to_fahrenheit(
            reading[0]["current_temperature"]
        ),
        NestDataExtraction.convert_celsius_to_fahrenheit(reading[0]["set_point_heat"]),
        NestDataExtraction.convert_celsius_to_fahrenheit(reading[0]["set_point_cool"]),
        reading[0]["mode"],
        reading[0]["status"],
    )


if __name__ == "__main__":
    main()
