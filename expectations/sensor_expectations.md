# Sensor Data Expectation Suite

This project validates incoming operational sensor data before loading it into the SQLite database.

## Validation Rules

1. timestamp must not be null.

2. Pressure_PSI must be greater than or equal to 0 PSI.

3. Temperature_C must not exceed the configured maximum temperature.

4. Zone must not be null.

5. Flow_Rate_LPM must be greater than zero.

The ETL pipeline stops immediately whenever any validation rule fails.