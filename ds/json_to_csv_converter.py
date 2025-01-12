import sys
import os
import json
import csv
import argparse

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

def json_to_csv(json_file, output_file):
    """
    Converts nested JSON data from a file into a flat CSV file.

    :param json_file: The path to the input JSON file.
    :param output_file: The path to the output CSV file.
    """
    with open(json_file, 'r') as file:
        json_data = json.load(file)

    flattened_data = []
    for website, products in json_data.items():
        if not isinstance(products, list):
            print(f"Warning: Skipping non-list entry for website '{website}'")
            continue
        for product in products:
            if not isinstance(product, dict):
                print(f"Warning: Skipping non-dict entry in website '{website}'")
                continue
            product['Website'] = website
            flattened_data.append(product)

    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = flattened_data[0].keys() if flattened_data else []
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(flattened_data)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert JSON to CSV")
    parser.add_argument("json_file", help="The path to the input JSON file")
    parser.add_argument("output_file", help="The path to the output CSV file")
    args = parser.parse_args()

    json_to_csv(args.json_file, args.output_file)