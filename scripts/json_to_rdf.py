"""
JSON to RDF Converter for Agentic Patterns
Converts normalized JSON patterns to RDF/Turtle format using AgentO ontology
"""
import json
import sys
from pathlib import Path
from urllib.parse import quote
from rdflib import Graph, Namespace, Literal, URIRef, RDF, RDFS, XSD
from rdflib.namespace import DCTERMS
from datetime import datetime

# Setup namespaces
AGENTO = Namespace("http://www.w3id.org/agentic-ai/onto#")
BASE = Namespace("http://www.w3id.org/agentic-ai/data/")

# Directories
PROJECT_ROOT = Path(__file__).parent.parent
JSON_DIR = PROJECT_ROOT / "data" / "normalized"
RDF_DIR = PROJECT_ROOT / "data" / "rdf"
RDF_DIR.mkdir(parents=True, exist_ok=True)


class JSONtoRDFConverter:
    """Convert JSON agentic patterns to RDF"""

    def __init__(self):
        self.graph = Graph()
        self.graph.bind("agento", AGENTO)
        self.graph.bind("dcterms", DCTERMS)
        self.graph.bind("data", BASE)

    def convert_pattern(self, json_data):
        """Convert single pattern from JSON to RDF"""

        # Pattern URI
        pattern_id = json_data["id"]
        # URL-encode pattern ID
        pattern_uri = BASE[quote(pattern_id, safe='')]

        # Pattern type
        self.graph.add((pattern_uri, RDF.type, AGENTO.Pattern))

        # Pattern attributes
        self.graph.add((pattern_uri, AGENTO.patternId, Literal(pattern_id, datatype=XSD.string)))
        self.graph.add((pattern_uri, AGENTO.framework, Literal(json_data["framework"], datatype=XSD.string)))

        if json_data.get("source_file"):
            self.graph.add((pattern_uri, AGENTO.sourceFile, Literal(json_data["source_file"], datatype=XSD.string)))

        if json_data.get("title"):
            self.graph.add((pattern_uri, DCTERMS.title, Literal(json_data["title"], lang="en")))

        if json_data.get("description"):
            self.graph.add((pattern_uri, DCTERMS.description, Literal(json_data["description"], lang="en")))

        if json_data.get("objective"):
            self.graph.add((pattern_uri, AGENTO.objective, Literal(json_data["objective"], datatype=XSD.string)))

        if json_data.get("created_at"):
            self.graph.add((pattern_uri, DCTERMS.created, Literal(json_data["created_at"], datatype=XSD.dateTime)))

        # Provenance
        if json_data.get("provenance"):
            prov = json_data["provenance"]
            if prov.get("extracted_from"):
                self.graph.add((pattern_uri, AGENTO.extractedFrom, Literal(prov["extracted_from"], datatype=XSD.string)))
            if prov.get("extraction_date"):
                self.graph.add((pattern_uri, AGENTO.extractionDate, Literal(prov["extraction_date"], datatype=XSD.dateTime)))
            if prov.get("extractor_version"):
                self.graph.add((pattern_uri, AGENTO.extractorVersion, Literal(prov["extractor_version"], datatype=XSD.string)))

        # Convert agents
        for agent in json_data.get("agents", []):
            agent_uri = self._convert_agent(agent, pattern_uri)
            self.graph.add((pattern_uri, AGENTO.hasAgentMember, agent_uri))

        # Convert tasks
        task_uris = {}
        for task in json_data.get("tasks", []):
            task_uri = self._convert_task(task)
            task_uris[task["id"]] = task_uri

        # Convert tools
        tool_uris = {}
        for tool in json_data.get("tools", []):
            tool_uri = self._convert_tool(tool)
            tool_uris[tool["id"]] = tool_uri

        # Convert resources
        for resource in json_data.get("resources", []):
            self._convert_resource(resource)

        # Convert workflow
        if json_data.get("workflow_pattern"):
            self._convert_workflow(json_data["workflow_pattern"], pattern_uri)

        # Convert team
        if json_data.get("team") and json_data["team"].get("name"):
            self._convert_team(json_data["team"], pattern_uri)

        return pattern_uri

    def _convert_agent(self, agent_data, pattern_uri):
        """Convert agent to RDF"""
        agent_id = agent_data["id"]
        # URL-encode agent ID
        agent_uri = BASE[quote(agent_id, safe='')]

        # Agent type
        self.graph.add((agent_uri, RDF.type, AGENTO.Agent))

        # Agent attributes
        self.graph.add((agent_uri, AGENTO.agentId, Literal(agent_id, datatype=XSD.string)))

        if agent_data.get("name"):
            self.graph.add((agent_uri, AGENTO.agentName, Literal(agent_data["name"], datatype=XSD.string)))

        if agent_data.get("role"):
            self.graph.add((agent_uri, AGENTO.role, Literal(agent_data["role"], datatype=XSD.string)))
            # Store vendor class (framework-specific class name)
            self.graph.add((agent_uri, AGENTO.vendorClass, Literal(agent_data["role"], datatype=XSD.string)))

        if agent_data.get("description"):
            self.graph.add((agent_uri, AGENTO.description, Literal(agent_data["description"], datatype=XSD.string)))
            # Also map to systemMessage for AutoGen agents
            if "assistant" in agent_data.get("name", "").lower() or "AssistantAgent" in agent_data.get("role", ""):
                self.graph.add((agent_uri, AGENTO.systemMessage, Literal(agent_data["description"], datatype=XSD.string)))

        if agent_data.get("goal"):
            self.graph.add((agent_uri, AGENTO.goalDescription, Literal(agent_data["goal"], datatype=XSD.string)))

        if agent_data.get("backstory"):
            self.graph.add((agent_uri, AGENTO.backstory, Literal(agent_data["backstory"], datatype=XSD.string)))

        if "memory" in agent_data:
            self.graph.add((agent_uri, AGENTO.hasMemory, Literal(agent_data["memory"], datatype=XSD.boolean)))

        # AutoGen-specific: humanInputMode
        if agent_data.get("humanInputMode"):
            self.graph.add((agent_uri, AGENTO.humanInputMode, Literal(agent_data["humanInputMode"], datatype=XSD.string)))

        # Language model
        if agent_data.get("language_model"):
            llm_id = f"llm_{agent_id}"
            # URL-encode LLM ID
            llm_uri = BASE[quote(llm_id, safe='')]
            self.graph.add((llm_uri, RDF.type, AGENTO.LLMModel))
            self.graph.add((llm_uri, AGENTO.modelName, Literal(agent_data["language_model"], datatype=XSD.string)))
            self.graph.add((agent_uri, AGENTO.usesLanguageModel, llm_uri))

        # Link tasks
        for task_id in agent_data.get("tasks", []):
            task_uri = BASE[quote(task_id, safe='')]
            self.graph.add((agent_uri, AGENTO.hasTask, task_uri))
            self.graph.add((task_uri, AGENTO.assignedTo, agent_uri))

        # Link tools
        for tool_id in agent_data.get("tools", []):
            tool_uri = BASE[quote(tool_id, safe='')]
            self.graph.add((agent_uri, AGENTO.usesTool, tool_uri))

        return agent_uri

    def _convert_task(self, task_data):
        """Convert task to RDF"""
        task_id = task_data["id"]
        # URL-encode the task ID to handle spaces and special characters
        task_uri = BASE[quote(task_id, safe='')]

        # Task type
        self.graph.add((task_uri, RDF.type, AGENTO.Task))

        # Task attributes
        self.graph.add((task_uri, AGENTO.taskId, Literal(task_id, datatype=XSD.string)))

        if task_data.get("title"):
            self.graph.add((task_uri, AGENTO.taskTitle, Literal(task_data["title"], datatype=XSD.string)))

        if task_data.get("description"):
            self.graph.add((task_uri, AGENTO.description, Literal(task_data["description"], datatype=XSD.string)))

        if task_data.get("expected_output"):
            self.graph.add((task_uri, AGENTO.expectedOutput, Literal(task_data["expected_output"], datatype=XSD.string)))

        return task_uri

    def _convert_tool(self, tool_data):
        """Convert tool to RDF"""
        tool_id = tool_data["id"]
        # URL-encode the tool ID
        tool_uri = BASE[quote(tool_id, safe='')]

        # Tool type
        self.graph.add((tool_uri, RDF.type, AGENTO.Tool))

        # Tool attributes
        self.graph.add((tool_uri, AGENTO.toolId, Literal(tool_id, datatype=XSD.string)))

        if tool_data.get("name"):
            self.graph.add((tool_uri, AGENTO.toolName, Literal(tool_data["name"], datatype=XSD.string)))

        if tool_data.get("description"):
            self.graph.add((tool_uri, AGENTO.description, Literal(tool_data["description"], datatype=XSD.string)))

        if tool_data.get("type"):
            self.graph.add((tool_uri, AGENTO.toolType, Literal(tool_data["type"], datatype=XSD.string)))

        # Link resource if present
        if tool_data.get("resource"):
            resource_uri = BASE[quote(tool_data["resource"], safe='')]
            self.graph.add((tool_uri, AGENTO.accessesResource, resource_uri))

        return tool_uri

    def _convert_resource(self, resource_data):
        """Convert resource to RDF"""
        resource_id = resource_data["id"]
        # URL-encode the resource ID
        resource_uri = BASE[quote(resource_id, safe='')]

        # Resource type
        self.graph.add((resource_uri, RDF.type, AGENTO.Resource))

        # Resource attributes
        self.graph.add((resource_uri, AGENTO.resourceId, Literal(resource_id, datatype=XSD.string)))

        if resource_data.get("name"):
            self.graph.add((resource_uri, AGENTO.resourceName, Literal(resource_data["name"], datatype=XSD.string)))

        if resource_data.get("type"):
            self.graph.add((resource_uri, AGENTO.resourceType, Literal(resource_data["type"], datatype=XSD.string)))

        if resource_data.get("description"):
            self.graph.add((resource_uri, AGENTO.description, Literal(resource_data["description"], datatype=XSD.string)))

        return resource_uri

    def _convert_workflow(self, workflow_data, pattern_uri):
        """Convert workflow pattern to RDF"""
        workflow_id = f"workflow_{pattern_uri.split('/')[-1]}"
        # URL-encode workflow ID
        workflow_uri = BASE[quote(workflow_id, safe='')]

        # Workflow type
        workflow_type = workflow_data.get("type", "Sequential")
        if workflow_type == "Sequential":
            self.graph.add((workflow_uri, RDF.type, AGENTO.SequentialPattern))
        elif workflow_type == "Parallel":
            self.graph.add((workflow_uri, RDF.type, AGENTO.ParallelPattern))
        elif workflow_type == "Nested":
            self.graph.add((workflow_uri, RDF.type, AGENTO.NestedPattern))
        else:
            self.graph.add((workflow_uri, RDF.type, AGENTO.WorkflowPattern))

        self.graph.add((workflow_uri, AGENTO.workflowType, Literal(workflow_type, datatype=XSD.string)))
        self.graph.add((pattern_uri, AGENTO.hasWorkflowPattern, workflow_uri))

        # Workflow steps
        for i, step in enumerate(workflow_data.get("steps", [])):
            step_id = f"step_{workflow_id}_{i}"
            # URL-encode step ID
            step_uri = BASE[quote(step_id, safe='')]
            self.graph.add((step_uri, RDF.type, AGENTO.WorkflowStep))
            self.graph.add((step_uri, AGENTO.stepOrder, Literal(step.get("order", i+1), datatype=XSD.integer)))
            self.graph.add((workflow_uri, AGENTO.hasWorkflowStep, step_uri))

            # Link to agent/task if present
            if step.get("agent"):
                agent_uri = BASE[quote(step["agent"], safe='')]
                self.graph.add((step_uri, AGENTO.performedBy, agent_uri))

            if step.get("task"):
                task_uri = BASE[quote(step["task"], safe='')]
                self.graph.add((step_uri, AGENTO.hasAssociatedTask, task_uri))

            # Link to next step
            if step.get("next_step"):
                next_step_id = f"step_{workflow_id}_{step['next_step']-1}"
                next_step_uri = BASE[quote(next_step_id, safe='')]
                self.graph.add((step_uri, AGENTO.nextStep, next_step_uri))

        return workflow_uri

    def _convert_team(self, team_data, pattern_uri):
        """Convert team to RDF"""
        team_id = f"team_{pattern_uri.split('/')[-1]}"
        # URL-encode team ID
        team_uri = BASE[quote(team_id, safe='')]

        # Team type
        self.graph.add((team_uri, RDF.type, AGENTO.Team))

        if team_data.get("name"):
            self.graph.add((team_uri, DCTERMS.title, Literal(team_data["name"], lang="en")))

        if team_data.get("process"):
            self.graph.add((team_uri, AGENTO.processType, Literal(team_data["process"], datatype=XSD.string)))

        return team_uri

    def save_to_file(self, output_path):
        """Save RDF graph to Turtle file"""
        self.graph.serialize(destination=str(output_path), format="turtle")
        return output_path


def convert_single_file(json_path, rdf_path):
    """Convert single JSON file to RDF"""
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    converter = JSONtoRDFConverter()
    converter.convert_pattern(data)
    converter.save_to_file(rdf_path)

    return rdf_path


def convert_all_patterns():
    """Convert all JSON patterns to RDF"""
    print("Converting JSON patterns to RDF/Turtle format...\n")
    print("="*60)

    stats = {"total": 0, "success": 0, "failed": 0}

    # Process all JSON files
    for json_file in JSON_DIR.glob("*.json"):
        stats["total"] += 1

        try:
            # Output RDF file
            rdf_file = RDF_DIR / f"{json_file.stem}.ttl"

            # Convert
            convert_single_file(json_file, rdf_file)

            stats["success"] += 1
            print(f"  OK {json_file.name} -> {rdf_file.name}")

        except Exception as e:
            stats["failed"] += 1
            print(f"  FAIL {json_file.name}: {e}")

    # Summary
    print("\n" + "="*60)
    print("CONVERSION SUMMARY")
    print("="*60)
    print(f"Total files: {stats['total']}")
    print(f"Successfully converted: {stats['success']}")
    print(f"Failed: {stats['failed']}")
    print(f"\nRDF files saved to: {RDF_DIR.absolute()}")
    print("="*60)

    return stats


def merge_all_rdf():
    """Merge all RDF files into single file"""
    print("\nMerging all RDF files...")

    merged_graph = Graph()
    merged_graph.bind("agento", AGENTO)
    merged_graph.bind("dcterms", DCTERMS)
    merged_graph.bind("data", BASE)

    # Load all RDF files
    for rdf_file in RDF_DIR.glob("*.ttl"):
        if rdf_file.name == "agentic-patterns.ttl":
            continue  # Skip merged file itself

        try:
            merged_graph.parse(str(rdf_file), format="turtle")
        except Exception as e:
            print(f"  Error loading {rdf_file.name}: {e}")

    # Save merged file
    merged_file = RDF_DIR / "agentic-patterns.ttl"
    merged_graph.serialize(destination=str(merged_file), format="turtle")

    print(f"  Merged {len(list(RDF_DIR.glob('pattern_*.ttl')))} files")
    print(f"  Total triples: {len(merged_graph)}")
    print(f"  Saved to: {merged_file.name}")

    return merged_file


if __name__ == "__main__":
    # Convert all patterns
    stats = convert_all_patterns()

    # Merge into single file
    if stats["success"] > 0:
        merge_all_rdf()

    print("\nDone!")
