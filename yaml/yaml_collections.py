from ruamel.yaml import YAML
from tabulate import tabulate
import os


def read_yaml(file_path):
    """Read YAML file and return Python object."""
    yaml = YAML(typ="safe")
    yaml.version = (1, 2)

    with open(file_path, "r", encoding="utf-8") as file:
        return yaml.load(file)


def display_as_table(data, parent_key=""):
    """Recursively flatten YAML into table rows."""
    rows = []

    # Handle Dictionary
    if isinstance(data, dict):
        if not data:
            rows.append([
                parent_key,
                "{}",
                "dict"
            ])
        else:
            for key, value in data.items():
                full_key = f"{parent_key}.{key}" if parent_key else str(key)
                rows.extend(display_as_table(value, full_key))

    # Handle List
    elif isinstance(data, list):
        if not data:
            rows.append([
                parent_key,
                "[]",
                "list"
            ])
        else:
            for index, item in enumerate(data):
                full_key = f"{parent_key}[{index}]"
                rows.extend(display_as_table(item, full_key))

    # Handle Primitive Values
    else:
        rows.append([
            parent_key,
            data,
            type(data).__name__
        ])

    return rows


def main(file_path):
    data = read_yaml(file_path)

    if data is None:
        print("YAML file is empty.")
        return

    table_data = display_as_table(data)

    print(
        tabulate(
            table_data,
            headers=["Key", "Value", "Value Type"],
            tablefmt="grid"
        )
    )


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    yaml_file_path = os.path.join(script_dir, "yaml_sequence.yml")

    if os.path.exists(yaml_file_path):
        main(yaml_file_path)
    else:
        print(f"YAML file not found: {yaml_file_path}")