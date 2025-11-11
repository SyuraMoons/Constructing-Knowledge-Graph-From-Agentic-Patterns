"""
Simple MastraAI Extractor
"""
import json
from pathlib import Path
import base_extractor


class MastraAIExtractor(base_extractor.BaseExtractor):
    """Simple extractor for MastraAI patterns (JSON/YAML configs)"""

    def __init__(self):
        super().__init__("mastraai")

    def extract(self, file_path: Path) -> dict:
        """Extract MastraAI pattern from JSON/YAML"""

        if file_path.suffix == '.json':
            data = self._load_json(file_path)
        elif file_path.suffix in ['.yaml', '.yml']:
            data = self._load_yaml(file_path)
        else:
            return {"agents": [], "tasks": [], "tools": []}

        agents = []
        tasks = []
        tools = []

        # Extract agents
        if "agents" in data:
            for a in data["agents"]:
                agents.append({
                    "name": a.get("name", "Agent"),
                    "role": a.get("role", ""),
                    "description": a.get("instructions", a.get("description", ""))
                })

        # Extract workflows as tasks
        if "workflows" in data:
            for w in data["workflows"]:
                tasks.append({
                    "title": w.get("name", "Workflow"),
                    "description": w.get("description", "")
                })

        return {
            "agents": agents,
            "tasks": tasks,
            "tools": tools,
            "workflow": {"type": "Sequential", "steps": []}
        }
