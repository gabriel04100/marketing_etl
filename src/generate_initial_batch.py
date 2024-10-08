import json
from generate_collection import generate_data
from datetime import date

def date_converter(o):
    """
    Convert date objects to string format for JSON serialization.
    """
    if isinstance(o, date):
        return o.isoformat()  # Convert to ISO format
    raise TypeError(f'Object of type {o.__class__.__name__} is not serializable')

# Generate the initial batch collection
initial_batch_collection = generate_data(10000)

# Print the generated data to the console
print(initial_batch_collection)

# Save the generated data into a JSON file
with open("./data/initial_batch_products.json", "w") as json_file:
    json.dump(initial_batch_collection, json_file, default=date_converter, indent=4)
