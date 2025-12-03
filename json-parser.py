import json
import os

def to_turtle_value(value):
    """
    Decide whether a value is a URI (prefix:value) or string literal.
    """
    if isinstance(value, str):
        if not value.startswith("http") and ":" in value and " " not in value:
            # likely CURIE (prefix:value)
            return value

    return json.dumps(str(value))


def convert_json_to_ttl(json_data):
    ttl_lines = []

    # --- Prefixes ---
    if "prefixes" in json_data:
        for prefix, uri in json_data["prefixes"].items():
            if prefix == "":
                ttl_lines.append(f"@prefix : <{uri}> .")
            else:
                ttl_lines.append(f"@prefix {prefix}: <{uri}> .")
        ttl_lines.append("")  # newline

    # --- Resources ---
    ttl_lines.append("### ================================")
    ttl_lines.append("### Resources")
    ttl_lines.append("### ================================")

    resources = json_data.get("resources", {})

    for subject, properties in resources.items():
        ttl_lines.append(f"\n{subject}")

        # Convert each predicate/object
        preds = []
        for pred, obj in properties.items():
            if pred == "rdf:type":
                preds.append(f"    a {obj}")
            else:
                preds.append(f"    {pred} {to_turtle_value(obj)}")

        ttl_lines.append(" ;\n".join(preds) + " .\n")

    return "\n".join(ttl_lines)


def convert_file(input_path, output_path):
    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    ttl_content = convert_json_to_ttl(data)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(ttl_content)


def process_folder(input_root, output_root):
    os.makedirs(output_root, exist_ok=True)

    for root, dirs, files in os.walk(input_root):
        for file in files:
            if file.endswith(".json"):
                input_path = os.path.join(root, file)

                # Preserve subfolder structure
                relative_path = os.path.relpath(root, input_root)
                output_dir = os.path.join(output_root, relative_path)
                os.makedirs(output_dir, exist_ok=True)

                output_name = file.replace(".json", ".ttl")
                output_path = os.path.join(output_dir, output_name)

                convert_file(input_path, output_path)
                print(f"Converted {input_path} → {output_path}")


if __name__ == "__main__":
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_root = os.path.join(script_dir, "data", "json_data")
    output_root = os.path.join(script_dir, "data", "ttl_data")
    process_folder(input_root, output_root)
