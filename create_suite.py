import great_expectations as gx
from great_expectations.expectations import (
    ExpectColumnValuesToNotBeNull,
    ExpectColumnValuesToBeBetween,
)

# Load the Great Expectations context
context = gx.get_context(project_root_dir="gx")

# Load the existing suite
suite = context.suites.get(name="sensor_suite")

# Clear any existing expectations so you can rerun this script safely
suite.expectations = []

# 1. Timestamp cannot be null
suite.add_expectation(
    ExpectColumnValuesToNotBeNull(
        column="timestamp"
    )
)

# 2. Zone cannot be null
suite.add_expectation(
    ExpectColumnValuesToNotBeNull(
        column="Zone"
    )
)

# 3. Pressure must be >= 0
suite.add_expectation(
    ExpectColumnValuesToBeBetween(
        column="Pressure_PSI",
        min_value=0
    )
)

# 4. Temperature must be <= 100
suite.add_expectation(
    ExpectColumnValuesToBeBetween(
        column="Temperature_C",
        max_value=100
    )
)

# 5. Flow rate must be greater than 0
suite.add_expectation(
    ExpectColumnValuesToBeBetween(
        column="Flow_Rate_LPM",
        min_value=0.000001
    )
)

# Save the suite
context.suites.add_or_update(suite)

print("✅ Expectation Suite updated successfully!")