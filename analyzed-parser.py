#!/usr/bin/env python3
"""
new.py
Universal pattern -> prefixes/resources JSON converter (one JSON per input .txt)

Behavior:
- Parses the analyzed pattern text (same headings you've used).
- Normalizes pattern into a structured representation per framework.
- Produces JSON with top-level "prefixes" and "resources" (ex:... keys).
- Auto-generates a goal and a task for every Agent (Version A behavior).
- Writes one JSON file per input .txt into data/json_data/.
"""

import json
import os
import re

# -------------------------
# Helpers (mostly your original functions, slightly adapted)
# -------------------------
def clean_lines(text):
    return [ln.strip() for ln in text.splitlines() if ln.strip()]

def chunk_list_safe(lst, n):
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
    # lines typically like: "Atribut", "Nilai", "Framework", "AutoGen", ...
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
    # lines are table rows; assume blocks of 5 (Entitas, Framework Class, Atribut, Contoh nilai, Catatan)
    # If the input is shorter, gracefully fallback.
    # If the first token is header-like skip it.
    if lines and lines[0].lower().startswith("entitas"):
        # skip header rows heuristically
        # find index of next blank or actual data - but keep simple:
        lines = lines[5:] if len(lines) > 5 else lines

    entities = []
    # chunk by 5 to extract ent, class, attrs, example, note
    for chunk in chunk_list_safe(lines, 5):
        while len(chunk) < 5:
            chunk.append("")
        ent, cls, attrs, example, note = chunk
        ent = ent.strip()
        cls = cls.strip()
        attrs = attrs.strip()
        example = example.strip()
        note = note.strip()

        # parse attributes and example values
        attr_dict = {}
        attr_names = [a.strip() for a in attrs.split(",")] if attrs else []
        example_values = [e.strip() for e in re.split(r',\s*(?=(?:[^"]*"[^"]*")*[^"]*$)', example)] if example else []
        # unquote example values
        example_values = [v.strip().strip('"').strip("“”") for v in example_values]

        for i, a in enumerate(attr_names):
            if i < len(example_values):
                attr_dict[a] = example_values[i]

        entities.append({
            "id": ent.lower().replace(" ", "_").strip() if ent else "",
            "vendorClass": cls,
            # mapsTo heuristic
            "mapsTo": "agento:Agent" if "Agent" in cls or "agent" in cls.lower() else
                      "agento:Task" if "Task" in cls else
                      "agento:Workflow" if "Flow" in cls or "workflow" in cls.lower() else
                      "",
            "attributes": attr_dict,
            "note": note,
            "raw_row": chunk
        })

    return entities

def parse_relational(lines):
    # lines likely contain the relational property table; parse in groups of 5 like before
    if lines and lines[0].lower().startswith("property"):
        lines = lines[5:]
    props = []
    for chunk in chunk_list_safe(lines, 5):
        while len(chunk) < 5:
            chunk.append("")
        prop, domain_range, definisi, bukti, status = [c.strip() for c in chunk]
        if not prop:
            continue
        if "→" in domain_range:
            domain, range_ = [x.strip() for x in domain_range.split("→")]
        else:
            # try "Agent -> Agent" style with arrow ascii
            domain, range_ = (domain_range, "")
            m = re.search(r'([A-Za-z0-9_]+)\s*(?:->|→)\s*([A-Za-z0-9_]+)', domain_range)
            if m:
                domain, range_ = m.group(1), m.group(2)
        status_clean = status.lower().replace("disarankan", "suggested").replace("opsional", "optional")
        props.append({
            "name": prop,
            "domain": domain,
            "range": range_,
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
        jenis, nama, desc, just = [x.strip() for x in r]
        if not jenis:
            continue
        if "class" in jenis.lower():
            new_classes.append({"name": nama, "definition": desc, "status_in_pattern": "used"})
        elif "datatype property" in jenis.lower() or "datatype" in jenis.lower():
            datatype_props.append({"name": nama, "domain": "agento:Agent", "range": "xsd:string", "justification": just})
        elif "opsional property" in jenis.lower() or "optional" in jenis.lower():
            optional_props.append({"name": nama, "domain": "agento:Agent", "range":"xsd:string", "justification": just})
    return {"newClasses": new_classes, "datatypeProperties": datatype_props, "optionalProperties": optional_props}

# -------------------------
# Convert raw analyzed text -> intermediate structured "autogen" object
# -------------------------
def convert_pattern_to_autogen(text):
    sections = split_sections(text)
    output = {}

    if "Identitas Pattern" in sections:
        ident = parse_two_column(sections["Identitas Pattern"])
        output["framework"] = ident.get("Framework", "").strip()
        output["file_name"] = ident.get("File name", "").strip()
        output["pattern_type"] = ident.get("Pattern Type", "").strip()
        output["description"] = ident.get("Deskripsi", "").strip()

    if "Analisis Struktur Pattern" in sections:
        output["entities"] = parse_entities(sections["Analisis Struktur Pattern"])

    if "Properti relasional" in sections:
        output["ontologyRelationalProperties"] = parse_relational(sections["Properti relasional"])

    if "Penyesuaian AgentO" in sections:
        output["newOntologyTerms"] = parse_penyesuaian(sections["Penyesuaian AgentO"])

    # keep original text to allow title extraction fallbacks
    output["_raw_text"] = text
    return output

# -------------------------
# Framework detection (same logic, tolerant)
# -------------------------
def detect_framework(data):
    fw = (data.get("framework") or "").strip().lower()
    if "autogen" in fw:
        return "autogen"
    if "crewai" in fw:
        return "crewai"
    if "langraph" in fw or "langgraph" in fw:
        return "langgraph"
    if "mastra" in fw:
        return "mastraai"

    # fallback heuristics: inspect vendorClass names
    entities = [e.get("vendorClass","").lower() for e in data.get("entities",[])]
    joined = " ".join(entities)
    if "assistantagent" in joined or "userproxyagent" in joined or "assistant" in joined:
        return "autogen"
    if "crew" in joined or "flow" in joined:
        return "crewai"
    if "stategraph" in joined or "node" in joined or "workflow" in joined:
        return "langgraph"
    return "unknown"

# -------------------------
# Title / name extraction helper
# -------------------------
def extract_title_from_data(data):
    # 1) try to find a system name in entities attributes
    for ent in data.get("entities", []):
        name = ent.get("attributes", {}).get("name")
        if name:
            return name.strip().strip('"').strip("“”")
    # 2) try file name -> use it
    fn = data.get("file_name") or ""
    if fn:
        base = os.path.splitext(os.path.basename(fn))[0]
        if base:
            return base.replace("_", " ").title()
    # 3) fallback to pattern_type or description
    if data.get("pattern_type"):
        return data.get("pattern_type")
    if data.get("description"):
        return data.get("description").split(".")[0].strip()
    return "Unknown"

# -------------------------
# Normalizers per framework (kept small & consistent)
# -------------------------
def normalize_autogen_to_required_format(data):
    title = extract_title_from_data(data)
    title_slug = title.lower().replace(" ", "_")

    result = {
        "agents": [],
        "goals": [],
        "workflowPatterns": []
    }

    # entities parsed earlier likely contain AssistantAgent and UserProxyAgent
    for ent in data.get("entities", []):
        vc = (ent.get("vendorClass") or "").lower()
        attrs = ent.get("attributes", {}) or {}
        ent_id = ent.get("id") or attrs.get("name") or ""
        if "assistant" in vc or "assistantagent" in vc or "assistant" in ent_id:
            agent_id = attrs.get("name") or ent_id or f"{title_slug}_assistant"
            # pick system_message or systemMessage
            system_msg = attrs.get("system_message") or attrs.get("systemMessage") or attrs.get("system message") or ""
            result["agents"].append({
                "id": "assistant",
                "type": "agento:Agent",
                "agentID": agent_id,
                "agentRole": "Assistant Agent",
                "title": f"{title} Assistant",
                "description": system_msg or f"You are a helpful AI assistant for {title.lower()}",
            })
        elif "userproxy" in vc or "user proxy" in vc or "userproxyagent" in vc or "user" in ent_id:
            agent_name = attrs.get("name") or ent_id or "user"
            human_mode = attrs.get("human_input_mode") or attrs.get("humanInputMode") or attrs.get("human input mode") or "NEVER"
            result["agents"].append({
                "id": "userproxy",
                "type": "agento:Agent",
                "agentID": agent_name,
                "agentRole": "User Proxy Agent",
                "title": "User Proxy",
                "description": f"Human input proxy with {human_mode} mode",
            })

    # auto-generate goals and a workflow pattern name for the pattern
    # (Version A: every agent gets a hasGoal and hasTask; goal/task objects will be generated later in the resource mapper)
    result["workflowPatterns"].append({
        "id": f"{title_slug}_workflow",
        "type": "agento:WorkflowPattern",
        "title": f"{title} Workflow",
        "description": data.get("description","")
    })

    return result

def normalize_crewai(data):
    title = extract_title_from_data(data)
    title_slug = title.lower().replace(" ", "_")
    result = {
        "systems": [],
        "agents": [],
        "workflowPatterns": []
    }

    # create flow/workflow entry for the Flow entity
    result["workflowPatterns"].append({
        "id": f"{title_slug}_workflow",
        "type": "agento:Workflow",
        "title": f"{title} Flow",
        "description": data.get("description","")
    })

    for ent in data.get("entities", []):
        vc = (ent.get("vendorClass") or "").lower()
        attrs = ent.get("attributes", {}) or {}
        ent_id = ent.get("id") or attrs.get("name") or ""
        if "flow" in vc or "contentcreatorflow" in ent_id or "flow" in ent_id:
            result["systems"].append({
                "id": ent_id or attrs.get("name") or "flow_system",
                "type": "agento:System",
                "title": attrs.get("name") or ent_id
            })
        if "crew" in vc or "system" in vc or "crew" in ent_id or "crew" in attrs.get("name", ""):
            result["systems"].append({
                "id": ent_id or attrs.get("name"),
                "type": "agento:System",
                "title": attrs.get("name") or ent_id
            })
        # treat agents found in attributes
        if attrs.get("agents") or attrs.get("name") and "crew" not in vc:
            # if agents present as "blog_researcher, blog_writer" parse and add them
            agents_field = attrs.get("agents") or attrs.get("name")
            if isinstance(agents_field, str) and "," in agents_field:
                for a in [x.strip() for x in agents_field.split(",")]:
                    result["agents"].append({
                        "id": a,
                        "type": "agento:Agent",
                        "agentID": a,
                        "agentRole": "Crew Agent",
                        "title": a
                    })

    return result

def normalize_langgraph(data):
    title = extract_title_from_data(data)
    title_slug = title.lower().replace(" ", "_")
    result = {"workflowPatterns": [], "nodes": []}
    result["workflowPatterns"].append({
        "id": f"{title_slug}_workflow",
        "type": "agento:Workflow",
        "title": f"{title} Graph",
        "description": data.get("description","")
    })
    for ent in data.get("entities", []):
        vendor = ent.get("vendorClass", "") or ""
        attrs = ent.get("attributes", {}) or {}
        if "node" in vendor.lower() or "node" in ent.get("id",""):
            result["nodes"].append({
                "id": ent.get("id"),
                "type": "agento:Node",
                "nodeName": attrs.get("name"),
                "callableLabel": attrs.get("callable") or attrs.get("callableLabel")
            })
    return result

def normalize_mastraai(data):
    systems = []
    agents = []
    llm_models = []
    # look for system name in entities attributes
    system_name = None
    for ent in data.get("entities", []):
        if ent.get("id","").lower().startswith("pattern"):
            system_name = ent.get("attributes", {}).get("name")
            if system_name:
                break
    if not system_name:
        system_name = data.get("file_name") or data.get("description") or "MastraAI System"
    if isinstance(system_name, str):
        system_name = system_name.strip().strip('"').strip("“”")
    else:
        system_name = "MastraAI System"
    systems.append({
        "id": system_name.lower().replace(" ", "_"),
        "type": "agento:System",
        "title": system_name,
        "description": data.get("description", "")
    })
    # Agents: look for ent.attributes with name/role/instructions/model
    for ent in data.get("entities", []):
        attrs = ent.get("attributes", {}) or {}
        if any(k in attrs for k in ("role","instructions","model","name")) and ent.get("id") != "pattern":
            agent_id = attrs.get("name") or ent.get("id")
            if isinstance(agent_id, str):
                agent_id = agent_id.strip().strip('"').strip("“”").lower().replace(" ", "_")
            role = attrs.get("role", "")
            instructions = attrs.get("instructions", "")
            model_name = attrs.get("model", "")
            agent_obj = {
                "id": agent_id,
                "type": "agento:Agent",
                "agentID": attrs.get("name", agent_id),
                "agentRole": role,
                "instructions": instructions,
                "partOfSystem": systems[0]["id"]
            }
            if model_name:
                model_id = f"llm_{model_name.lower().replace(' ', '_')}"
                llm_models.append({
                    "id": model_id,
                    "type": "agento:LLMModel",
                    "modelName": model_name
                })
                agent_obj["configuredBy"] = model_id
            agents.append(agent_obj)
    return {
        "systems": systems,
        "agents": agents,
        "llmModels": llm_models
    }

# -------------------------
# Framework router to get structured representation
# -------------------------
def convert_autogen_to_structured_json(data):
    fw = detect_framework(data)
    if fw == "autogen":
        return normalize_autogen_to_required_format(data)
    if fw == "crewai":
        return normalize_crewai(data)
    if fw == "langgraph":
        return normalize_langgraph(data)
    if fw == "mastraai":
        return normalize_mastraai(data)
    # fallback (wrap entities):
    return {"entities": data.get("entities", []), "description": data.get("description","")}

# -------------------------
# Mapper: structured representation -> prefixes/resources JSON shape
# -------------------------
DEFAULT_PREFIXES = {
    "": "http://www.w3id.org/agentic-ai/onto#",
    "agento": "http://www.w3id.org/agentic-ai/onto#",
    "ex": "http://www.w3id.org/agentic-ai/instances#",
    "dcterms": "http://purl.org/dc/terms/",
    "xsd": "http://www.w3.org/2001/XMLSchema#",
    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
    "owl": "http://www.w3.org/2002/07/owl#"
}

def mk_ex(key):
    # ensure ex:key format (no leading slash)
    return f"ex:{key}"

def safe_id_for_resource(base):
    # convert name to safe resource id
    return re.sub(r'[^a-zA-Z0-9_]', '_', base.strip().lower())

def add_agent_resources(resources, agent_obj):
    """
    Add agent resource and auto-generated goal/task resources (Version A).
    agent_obj expected keys: id, agentID, agentRole, title, description
    """
    aid = agent_obj.get("id") or safe_id_for_resource(agent_obj.get("agentID") or agent_obj.get("title") or "agent")
    ex_agent = mk_ex(aid)
    # build agent resource
    agent_res = {"rdf:type": ":Agent"}
    # agentID (prefer the agentID field; fallback to id)
    if agent_obj.get("agentID"):
        agent_res[":agentID"] = agent_obj.get("agentID")
    else:
        agent_res[":agentID"] = agent_obj.get("id") or aid
    if agent_obj.get("agentRole"):
        agent_res[":agentRole"] = agent_obj.get("agentRole")
    # title and description - prefer dcterms keys where possible
    if agent_obj.get("title"):
        agent_res["dcterms:title"] = agent_obj.get("title")
    if agent_obj.get("description"):
        agent_res["dcterms:description"] = agent_obj.get("description")
    # make goal & task ids (Version A: always make)
    goal_id = f"goal_{aid}"
    task_id = f"task_{aid}"
    agent_res[":hasGoal"] = mk_ex(goal_id)
    agent_res[":hasTask"] = mk_ex(task_id)
    resources[ex_agent] = agent_res

    # create goal resource
    goal_res = {
        "rdf:type": ":Goal",
        "dcterms:title": f"Goal for {agent_res.get(':agentID')}",
        "dcterms:description": f"Automatically generated goal for {agent_res.get(':agentID')}"
    }
    resources[mk_ex(goal_id)] = goal_res

    # create task resource with expected output
    task_res = {
        "rdf:type": ":Task",
        "dcterms:title": f"Task for {agent_res.get(':agentID')}",
        "dcterms:description": f"Automatically generated task for {agent_res.get(':agentID')}",
        ":taskExpectedOutput": f"Automatically generated expected output for {agent_res.get(':agentID')}"
    }
    resources[mk_ex(task_id)] = task_res

def add_goal_resource(resources, gid, title=None, desc=None):
    resources[mk_ex(gid)] = {
        "rdf:type": ":Goal",
        "dcterms:title": title or gid,
        "dcterms:description": desc or ""
    }

def add_task_resource(resources, tid, title=None, desc=None, expected=None):
    task = {"rdf:type": ":Task"}
    if title:
        task["dcterms:title"] = title
    if desc:
        task["dcterms:description"] = desc
    task[":taskExpectedOutput"] = expected or ""
    resources[mk_ex(tid)] = task

def add_workflow_resource(resources, wf):
    # wf expected keys: id, type, title, description
    wid = wf.get("id") or safe_id_for_resource(wf.get("title","workflow"))
    res = {"rdf:type": ":WorkflowPattern"}
    if wf.get("title"):
        res["dcterms:title"] = wf.get("title")
    if wf.get("description"):
        res["dcterms:description"] = wf.get("description")
    resources[mk_ex(wid)] = res

def add_datatype_property_resource(resources, name, domain="agento:Agent", justification="", range_="xsd:string"):
    rid = safe_id_for_resource(name)
    resources[mk_ex(f"DatatypeProperty_{rid}")] = {
        "rdf:type": "agento:DatatypeProperty",
        "agento:domain": domain,
        "agento:justification": justification,
        "agento:name": name,
        "agento:range": range_
    }

def structured_to_prefixes_resources(structured, raw_autogen):
    """
    Turn normalized structured representation into the prefixes/resources JSON shape.
    This function attempts to support outputs from normalize_{autogen,crewai,langgraph,mastraai}.
    """
    prefixes = DEFAULT_PREFIXES.copy()
    resources = {}

    # 1) map agents if present
    # different normalizers put agents under different keys: 'agents', 'systems', 'agents' inside mastra etc.
    agents_list = structured.get("agents") or []
    # if crewi used 'systems' plus separate agents, we still handle systems below
    for agent in agents_list:
        # agent may be a simple id string or dict
        if isinstance(agent, str):
            agent_obj = {"id": agent, "agentID": agent, "title": agent}
        else:
            agent_obj = agent
        add_agent_resources(resources, agent_obj)

    # 2) if mastra produced 'systems', add them as Workflow/System resources
    for sys_obj in structured.get("systems", []) if isinstance(structured.get("systems", []), list) else []:
        sid = sys_obj.get("id") or safe_id_for_resource(sys_obj.get("title","system"))
        res = {"rdf:type": ":System" if sys_obj.get("type","").lower().endswith("system") else ":WorkflowPattern"}
        if sys_obj.get("title"):
            res["dcterms:title"] = sys_obj.get("title")
        if sys_obj.get("description"):
            res["dcterms:description"] = sys_obj.get("description")
        resources[mk_ex(sid)] = res
        # if system lists agents, create simple agent resources (do not duplicate goals/tasks if already created)
        if isinstance(sys_obj.get("agents"), (list, tuple)):
            for a in sys_obj.get("agents"):
                aid = a if isinstance(a, str) else a.get("id")
                if mk_ex(aid) not in resources:
                    add_agent_resources(resources, {"id": aid, "agentID": aid, "title": aid})

    # 3) workflowPatterns
    for wf in structured.get("workflowPatterns", []):
        add_workflow_resource(resources, wf)

    # 4) nodes (langgraph)
    for node in structured.get("nodes", []):
        nid = node.get("id") or safe_id_for_resource(node.get("nodeName","node"))
        node_res = {"rdf:type": ":Node"}
        if node.get("nodeName"):
            node_res["dcterms:title"] = node.get("nodeName")
        if node.get("callableLabel"):
            node_res[":callableLabel"] = node.get("callableLabel")
        resources[mk_ex(nid)] = node_res

    # 5) llmModels
    for model in structured.get("llmModels", []):
        mid = model.get("id") or safe_id_for_resource(model.get("modelName","llm"))
        resources[mk_ex(mid)] = {
            "rdf:type": ":LanguageModel",
            "dcterms:title": model.get("modelName", mid)
        }

    # 6) newOntologyTerms (datatype properties etc.) from autogen parsing
    new_terms = raw_autogen.get("newOntologyTerms") or {}
    # datatypeProperties and optionalProperties list
    for dp in new_terms.get("datatypeProperties", []):
        add_datatype_property_resource(resources, dp.get("name"), domain=dp.get("domain", "agento:Agent"), justification=dp.get("justification",""), range_=dp.get("range","xsd:string"))
    for op in new_terms.get("optionalProperties", []):
        add_datatype_property_resource(resources, op.get("name"), domain=op.get("domain", "agento:Agent"), justification=op.get("justification",""), range_=op.get("range","xsd:string"))
    # also add newClasses
    for nc in new_terms.get("newClasses", []):
        cid = safe_id_for_resource(nc.get("name","class"))
        resources[mk_ex(cid)] = {
            "rdf:type": "owl:Class",
            "dcterms:title": nc.get("name"),
            "dcterms:description": nc.get("definition","")
        }

    # 7) If the structured map is very sparse but raw_autogen.entities exist, try to add agents from those entities
    # This is to cover corner cases where framework wasn't confidently detected
    if not agents_list and raw_autogen.get("entities"):
        for ent in raw_autogen.get("entities", []):
            vc = ent.get("vendorClass","").lower()
            attrs = ent.get("attributes", {}) or {}
            name = attrs.get("name") or ent.get("id") or ""
            if "agent" in vc or "assistant" in vc or "userproxy" in vc:
                # don't overwrite existing resource if present
                rid = mk_ex(safe_id_for_resource(name or ent.get("id","agent")))
                if rid not in resources:
                    agent_obj = {
                        "id": safe_id_for_resource(name or ent.get("id","agent")),
                        "agentID": name or ent.get("id"),
                        "agentRole": attrs.get("role") or vc.title(),
                        "title": name or ent.get("id"),
                        "description": attrs.get("system_message") or attrs.get("systemMessage") or attrs.get("instructions","")
                    }
                    add_agent_resources(resources, agent_obj)

    return {"prefixes": prefixes, "resources": resources}


# -------------------------
# File processing
# -------------------------
def process_file_text_to_json(text):
    # parse raw -> autogen intermediate
    raw = convert_pattern_to_autogen(text)
    # structured normalization
    structured = convert_autogen_to_structured_json(raw)
    # convert to prefixes/resources shape
    packaged = structured_to_prefixes_resources(structured, raw)
    return packaged

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

                try:
                    packaged = process_file_text_to_json(text)
                except Exception as e:
                    print(f"[ERROR] Failed parsing {input_path}: {e}")
                    packaged = {"prefixes": DEFAULT_PREFIXES, "resources": {}, "error": str(e)}

                output_file = os.path.join(output_dir, file.replace(".txt", ".json"))
                with open(output_file, "w", encoding="utf-8") as f:
                    json.dump(packaged, f, ensure_ascii=False, indent=2)

                print(f"Processed: {input_path} -> {output_file}")

# -------------------------
# MAIN ENTRY
# -------------------------
if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_root = os.path.join(script_dir, "data", "analyzed_data")
    output_root = os.path.join(script_dir, "data", "json_data")
    process_folder(input_root, output_root)
