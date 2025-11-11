"""
Simple AutoGen Extractor
"""
import ast
from pathlib import Path
import base_extractor


class AutoGenExtractor(base_extractor.BaseExtractor):
    """Simple extractor for AutoGen patterns"""

    def __init__(self):
        super().__init__("autogen")

    def extract(self, file_path: Path) -> dict:
        """Extract AutoGen pattern - looks for AssistantAgent, UserProxyAgent, etc."""
        code = self._load_python(file_path)

        try:
            tree = ast.parse(code)
        except:
            return {"agents": [], "tasks": [], "tools": []}

        agents = []
        tasks = []
        tools = []

        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                func_name = self._get_func_name(node)

                if "Agent" in func_name:
                    agent = self._extract_agent(node, func_name)
                    if agent:
                        agents.append(agent)

        return {
            "agents": agents,
            "tasks": tasks,
            "tools": tools,
            "workflow": {"type": "Sequential", "steps": []}
        }

    def _get_func_name(self, node):
        """Get function name"""
        if isinstance(node.func, ast.Name):
            return node.func.id
        elif isinstance(node.func, ast.Attribute):
            return node.func.attr
        return ""

    def _extract_agent(self, node, func_name):
        """Extract agent info"""
        agent = {
            "name": func_name,
            "role": func_name,
            "description": ""
        }

        for kw in node.keywords:
            if kw.arg == "name":
                try:
                    agent["name"] = ast.literal_eval(kw.value)
                except:
                    pass
            elif kw.arg == "system_message":
                try:
                    agent["description"] = ast.literal_eval(kw.value)
                except:
                    pass

        return agent
