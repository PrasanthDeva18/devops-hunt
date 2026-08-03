from ruamel.yaml import YAML
from tabulate import tabulate
import os


def read_yaml(file_path):
    """
    Read a YAML file and return the parsed Python object.
    """
    yaml = YAML(typ="safe")
    yaml.version = (1, 2)

    with open(file_path, "r", encoding="utf-8") as file:
        return yaml.load(file)


def display_as_table(data, parent_key=""):
    """
    Recursively convert YAML data into table rows.
    """
    rows = []

    # Dictionary (Mapping)
    if isinstance(data, dict):

        # Handle empty dictionary
        if not data:
            rows.append([
                parent_key,
                "{}",
                type(parent_key).__name__,
                "dict"
            ])
        else:
            for key, value in data.items():
                full_key = f"{parent_key}.{key}" if parent_key else str(key)
                rows.extend(display_as_table(value, full_key))

    # List (Sequence)
    elif isinstance(data, list):

        # Handle empty list
        if not data:
            rows.append([
                parent_key,
                "[]",
                type(parent_key).__name__,
                "list"
            ])
        else:
            for index, item in enumerate(data):
                full_key = f"{parent_key}[{index}]"
                rows.extend(display_as_table(item, full_key))

    # Primitive values
    else:
        rows.append([
            parent_key,
            data,
            type(parent_key).__name__,
            type(data).__name__
        ])

    return rows


def main(file_path):
    try:
        data = read_yaml(file_path)

        if data is None:
            print("YAML file is empty.")
            return

        table_data = display_as_table(data)

        print(
            tabulate(
                table_data,
                headers=["Key", "Value", "Key Type", "Value Type"],
                tablefmt="grid"
            )
        )

    except FileNotFoundError:
        print(f"Error: File not found -> {file_path}")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    # YAML file should be in the same folder as this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    yaml_file_path = os.path.join(script_dir, "complex.yaml")

    main(yaml_file_path)