import json
import os

# -------------------------
# Helpers (same as your parser)
# -------------------------
def clean_lines(text):
    return [ln.strip() for ln in text.splitlines() if ln.strip()]

def chunk_list_safe(lst, n):
    """Split list into chunks of size n; last chunk may be shorter."""
    for i in range(0, len(lst), n):
        yield lst[i:i+n]

HEADERS = [
    "Identitas Pattern",
    "Analisis Struktur Pattern",
    "kelas (classes)",
    "Properti relasional",
    "Properti atributif",
    "Penyesuaian AgentO"
]

def split_sections(text):
    lines = clean_lines(text)
    sections = {}
    current = None
    for ln in lines:
        if ln in HEADERS:
            current = ln
            sections[current] = []
        elif current:
            sections[current].append(ln)
    return sections

def parse_two_column(lines):
    if lines and lines[0].lower() in ("atribut", "attribute"):
        lines = lines[2:]
    obj = {}
    for p in chunk_list_safe(lines, 2):
        if len(p) == 2:
            obj[p[0]] = p[1]
        elif len(p) == 1:
            obj[p[0]] = ""
    return obj

def parse_entities(lines):
    if lines and lines[0].lower().startswith("entitas"):
        lines = lines[5:]
    entities = []
    for chunk in chunk_list_safe(lines, 5):
        while len(chunk) < 5:
            chunk.append("")
        ent, cls, attrs, example, note = chunk
        attr_dict = {}
        attr_names = [a.strip() for a in attrs.split(",")] if attrs else []
        example_values = [e.strip() for e in example.split(",")] if example else []
        for i, a in enumerate(attr_names):
            if i < len(example_values):
                attr_dict[a] = example_values[i].strip('" ')
        entities.append({
            "id": ent.lower().replace("agent", "").strip() or ent,
            "vendorClass": cls,
            "mapsTo": "agento:Agent",
            "attributes": attr_dict,
            "relations": {}
        })
    return entities

def parse_relational(lines):
    if lines and lines[0].lower().startswith("property"):
        lines = lines[5:]
    props = []
    for chunk in chunk_list_safe(lines, 5):
        while len(chunk) < 5:
            chunk.append("")
        prop, domain_range, definisi, bukti, status = chunk
        if not prop:
            continue
        if "→" in domain_range:
            domain, range_ = [x.strip() for x in domain_range.split("→")]
        else:
            domain, range_ = domain_range, ""
        status_clean = status.lower().replace("disarankan", "suggested").replace("opsional", "optional").replace("tidak muncul","not_used")
        props.append({
            "name": prop,
            "domain": f"agento:{domain}",
            "range": f"agento:{range_}" if range_ else "",
            "definition": definisi,
            "status_in_pattern": status_clean
        })
    return props

def parse_penyesuaian(lines):
    rows = list(chunk_list_safe(lines, 4))
    new_classes = []
    datatype_props = []
    optional_props = []
    for r in rows:
        while len(r) < 4:
            r.append("")
        jenis, nama, desc, just = r
        if "class" in jenis.lower():
            new_classes.append({"name": f"agento:{nama}", "definition": desc, "status_in_pattern": "used"})
        elif "datatype property" in jenis.lower():
            datatype_props.append({"name": nama, "domain": "agento:Agent", "range": "xsd:string", "justification": just})
        elif "opsional property" in jenis.lower():
            optional_props.append({"name": "vendorClass", "domain": "agento:Agent", "range":"xsd:string", "justification": just})
    return {"newClasses": new_classes, "datatypeProperties": datatype_props, "optionalProperties": optional_props}

def convert_pattern_to_autogen(text):
    sections = split_sections(text)
    output = {}
    if "Identitas Pattern" in sections:
        ident = parse_two_column(sections["Identitas Pattern"])
        output["framework"] = ident.get("Framework", "")
        output["file_name"] = ident.get("File name", "")
        output["pattern_type"] = ident.get("Pattern Type", "").replace(" ", "")
        output["description"] = ident.get("Deskripsi", "")
    if "Analisis Struktur Pattern" in sections:
        output["entities"] = parse_entities(sections["Analisis Struktur Pattern"])
    if "Properti relasional" in sections:
        output["ontologyRelationalProperties"] = parse_relational(sections["Properti relasional"])
    if "Penyesuaian AgentO" in sections:
        output["newOntologyTerms"] = parse_penyesuaian(sections["Penyesuaian AgentO"])
    return output

# -------------------------
# Recursive folder processing
# -------------------------
def process_folder(input_root, output_root):
    for root, dirs, files in os.walk(input_root):
        for file in files:
            if file.endswith(".txt"):
                input_path = os.path.join(root, file)
                rel_path = os.path.relpath(root, input_root)
                output_dir = os.path.join(output_root, rel_path)
                os.makedirs(output_dir, exist_ok=True)
                with open(input_path, "r", encoding="utf-8") as f:
                    text = f.read()
                json_data = convert_pattern_to_autogen(text)
                output_file = os.path.join(output_dir, file.replace(".txt", ".json"))
                with open(output_file, "w", encoding="utf-8") as f:
                    json.dump(json_data, f, ensure_ascii=False, indent=4)
                print(f"Processed: {input_path} -> {output_file}")

# -------------------------
# Main
# -------------------------
if __name__ == "__main__":
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_root = os.path.join(script_dir, "data", "analyzed_data")
    output_root = os.path.join(script_dir, "data", "json_data")
    process_folder(input_root, output_root)
