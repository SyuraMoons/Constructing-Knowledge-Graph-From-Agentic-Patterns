"""
LangGraph-Specific Extractor
Parses LangGraph state graph configurations
"""
import ast
import re
from pathlib import Path
from typing import Dict, List, Any
import base_extractor


class LangGraphExtractor(base_extractor.BaseExtractor):
    """Extractor for LangGraph framework patterns"""

    def __init__(self):
        super().__init__("langraph")

    def extract(self, file_path: Path) -> Dict[str, Any]:
        """
        Extract LangGraph pattern from Python file

        Looks for:
        - StateGraph definitions
        - Node additions (add_node)
        - Edge connections (add_edge, add_conditional_edges)
        - Agent/Tool definitions
        """
        code = self._load_python(file_path)

        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            raise ValueError(f"Invalid Python syntax in {file_path}: {e}")

        agents = []
        tasks = []
        tools = []
        workflow_steps = []
        graph_name = "LangGraph Workflow"

        # Extract components
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                func_name = self._get_function_name(node)

                # StateGraph instantiation
                if func_name == "StateGraph":
                    graph_name = self._extract_graph_name(node)

                # add_node calls
                elif func_name == "add_node":
                    node_data = self._extract_node(node)
                    if node_data:
                        agents.append(node_data)
                        tasks.append({
                            "title": node_data.get("name", "Task"),
                            "description": f"Execute {node_data.get('name', 'node')}"
                        })

                # Tool definitions
                elif "Tool" in func_name:
                    tool_data = self._extract_tool(node, func_name)
                    if tool_data:
                        tools.append(tool_data)

        # Build workflow from graph structure (simplified - sequential by default)
        workflow_steps = self._build_workflow_from_nodes(agents, tasks)

        return {
            "title": graph_name,
            "description": self._extract_description(code),
            "objective": f"Execute {graph_name} workflow",
            "agents": agents,
            "tasks": tasks,
            "tools": tools,
            "resources": self._extract_resources_from_tools(tools),
            "workflow": {
                "type": "Sequential",  # Could be enhanced to detect parallel/conditional
                "steps": workflow_steps
            },
            "team": {"name": graph_name, "process": "graph"}
        }

    def _get_function_name(self, node: ast.Call) -> str:
        """Get function name from Call node"""
        if isinstance(node.func, ast.Name):
            return node.func.id
        elif isinstance(node.func, ast.Attribute):
            return node.func.attr
        return ""

    def _extract_graph_name(self, node: ast.Call) -> str:
        """Extract graph name from StateGraph"""
        # Look for assignment like: graph = StateGraph(...)
        return "LangGraph Workflow"

    def _extract_node(self, node: ast.Call) -> Dict[str, Any]:
        """Extract node configuration"""
        node_data = {
            "name": "",
            "role": "Graph Node",
            "description": "",
            "tools": []
        }

        # First argument is usually the node name
        if node.args:
            node_name = self._eval_node(node.args[0])
            node_data["name"] = node_name
            node_data["description"] = f"Graph node: {node_name}"

        return node_data if node_data["name"] else None

    def _extract_tool(self, node: ast.Call, tool_type: str) -> Dict[str, Any]:
        """Extract tool configuration"""
        tool_data = {
            "name": tool_type,
            "type": tool_type,
            "description": ""
        }

        for keyword in node.keywords:
            if keyword.arg == "name":
                tool_data["name"] = self._eval_node(keyword.value)
            elif keyword.arg == "description":
                tool_data["description"] = self._eval_node(keyword.value)

        return tool_data

    def _eval_node(self, node: ast.AST) -> Any:
        """Safely evaluate AST node"""
        try:
            return ast.literal_eval(node)
        except:
            if isinstance(node, ast.Name):
                return node.id
            return ""

    def _extract_description(self, code: str) -> str:
        """Extract description from docstring"""
        try:
            tree = ast.parse(code)
            return ast.get_docstring(tree) or ""
        except:
            return ""

    def _build_workflow_from_nodes(self, agents: List[Dict], tasks: List[Dict]) -> List[Dict]:
        """Build workflow steps"""
        steps = []
        for i, (agent, task) in enumerate(zip(agents, tasks)):
            steps.append({
                "order": i + 1,
                "task": task.get("description", ""),
                "agent": agent.get("name", ""),
                "next_step": i + 2 if i < len(agents) - 1 else None
            })
        return steps

    def _extract_resources_from_tools(self, tools: List[Dict]) -> List[Dict]:
        """Extract resources from tools"""
        return []
