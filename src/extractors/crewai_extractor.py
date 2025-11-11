"""
CrewAI-Specific Extractor
Parses CrewAI agent configurations from Python files
"""
import ast
import re
from pathlib import Path
from typing import Dict, List, Any
import base_extractor


class CrewAIExtractor(base_extractor.BaseExtractor):
    """Extractor for CrewAI framework patterns"""

    def __init__(self):
        super().__init__("crewai")

    def extract(self, file_path: Path) -> Dict[str, Any]:
        """
        Extract CrewAI pattern from Python file

        Looks for:
        - Agent() instantiations with role, goal, backstory, tools, llm
        - Task() instantiations with description, expected_output, agent
        - Crew() instantiations with agents, tasks, process
        """
        code = self._load_python(file_path)

        # Parse AST
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            raise ValueError(f"Invalid Python syntax in {file_path}: {e}")

        # Extract components
        agents = []
        tasks = []
        crews = []
        tools = []
        resources = []

        # Visit all nodes
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                func_name = self._get_function_name(node)

                if func_name == "Agent":
                    agent_data = self._extract_agent(node)
                    agents.append(agent_data)
                    # Extract tools from agent
                    if agent_data.get("tools"):
                        tools.extend(agent_data.get("tools", []))

                elif func_name == "Task":
                    task_data = self._extract_task(node)
                    tasks.append(task_data)

                elif func_name == "Crew":
                    crew_data = self._extract_crew(node)
                    crews.append(crew_data)

        # Determine workflow type from crew process
        workflow_type = "Sequential"  # Default
        if crews:
            process = crews[0].get("process", "sequential")
            if process == "hierarchical":
                workflow_type = "Nested"
            elif process == "parallel":
                workflow_type = "Parallel"

        # Build workflow steps
        workflow_steps = self._build_workflow_steps(agents, tasks, workflow_type)

        # Extract resources from tools
        resources = self._extract_resources_from_tools(tools)

        return {
            "title": self._extract_title(code, file_path),
            "description": self._extract_description(code),
            "objective": self._extract_objective(crews, tasks),
            "agents": agents,
            "tasks": tasks,
            "tools": tools,
            "resources": resources,
            "workflow": {
                "type": workflow_type,
                "steps": workflow_steps
            },
            "team": crews[0] if crews else {}
        }

    def _get_function_name(self, node: ast.Call) -> str:
        """Get the function name from Call node"""
        if isinstance(node.func, ast.Name):
            return node.func.id
        elif isinstance(node.func, ast.Attribute):
            return node.func.attr
        return ""

    def _extract_agent(self, node: ast.Call) -> Dict[str, Any]:
        """Extract Agent configuration from AST node"""
        agent_data = {
            "name": "",
            "role": "",
            "goal": "",
            "backstory": "",
            "description": "",
            "tools": [],
            "llm": None,
            "memory": False,
            "verbose": False
        }

        for keyword in node.keywords:
            key = keyword.arg
            value = self._eval_node(keyword.value)

            if key == "role":
                agent_data["role"] = value
                agent_data["name"] = value  # Use role as name
            elif key == "goal":
                agent_data["goal"] = value
            elif key == "backstory":
                agent_data["backstory"] = value
                agent_data["description"] = value  # Use backstory as description
            elif key == "tools":
                agent_data["tools"] = self._extract_tools_list(keyword.value)
            elif key == "llm":
                agent_data["llm"] = self._extract_llm(keyword.value)
            elif key == "memory":
                agent_data["memory"] = value
            elif key == "verbose":
                agent_data["verbose"] = value

        return agent_data

    def _extract_task(self, node: ast.Call) -> Dict[str, Any]:
        """Extract Task configuration from AST node"""
        task_data = {
            "title": "",
            "description": "",
            "expected_output": "",
            "agent": ""
        }

        for keyword in node.keywords:
            key = keyword.arg
            value = self._eval_node(keyword.value)

            if key == "description":
                task_data["description"] = value
                task_data["title"] = value[:50] if value else "Task"  # Use first 50 chars as title
            elif key == "expected_output":
                task_data["expected_output"] = value
            elif key == "agent":
                # Try to get agent variable name
                if isinstance(keyword.value, ast.Name):
                    task_data["agent"] = keyword.value.id
                else:
                    task_data["agent"] = str(value)

        return task_data

    def _extract_crew(self, node: ast.Call) -> Dict[str, Any]:
        """Extract Crew configuration from AST node"""
        crew_data = {
            "name": "Crew",
            "agents": [],
            "tasks": [],
            "process": "sequential"
        }

        for keyword in node.keywords:
            key = keyword.arg
            value = self._eval_node(keyword.value)

            if key == "agents":
                crew_data["agents"] = self._extract_list_items(keyword.value)
            elif key == "tasks":
                crew_data["tasks"] = self._extract_list_items(keyword.value)
            elif key == "process":
                crew_data["process"] = value

        return crew_data

    def _extract_tools_list(self, node: ast.AST) -> List[Dict]:
        """Extract tools from a list node"""
        tools = []

        if isinstance(node, ast.List):
            for item in node.elts:
                tool = self._extract_tool_from_node(item)
                if tool:
                    tools.append(tool)

        return tools

    def _extract_tool_from_node(self, node: ast.AST) -> Dict[str, Any]:
        """Extract single tool information from AST node"""
        tool_data = {
            "name": "",
            "description": "",
            "type": ""
        }

        if isinstance(node, ast.Call):
            # Tool instantiation like SearchTool()
            func_name = self._get_function_name(node)
            tool_data["name"] = func_name
            tool_data["type"] = func_name

            # Extract description from docstring or parameters
            for keyword in node.keywords:
                if keyword.arg == "description":
                    tool_data["description"] = self._eval_node(keyword.value)

        elif isinstance(node, ast.Name):
            # Tool variable reference
            tool_data["name"] = node.id
            tool_data["type"] = node.id

        return tool_data if tool_data["name"] else None

    def _extract_llm(self, node: ast.AST) -> str:
        """Extract LLM model information"""
        if isinstance(node, ast.Call):
            func_name = self._get_function_name(node)
            # Look for model parameter
            for keyword in node.keywords:
                if keyword.arg in ["model", "model_name"]:
                    return self._eval_node(keyword.value)
            return func_name
        elif isinstance(node, ast.Name):
            return node.id
        return None

    def _extract_list_items(self, node: ast.AST) -> List[str]:
        """Extract variable names from a list"""
        items = []
        if isinstance(node, ast.List):
            for item in node.elts:
                if isinstance(item, ast.Name):
                    items.append(item.id)
        return items

    def _eval_node(self, node: ast.AST) -> Any:
        """Safely evaluate AST node to get value"""
        try:
            return ast.literal_eval(node)
        except (ValueError, TypeError):
            # For non-literal nodes, try to get string representation
            if isinstance(node, ast.Name):
                return node.id
            elif isinstance(node, ast.Attribute):
                return f"{self._eval_node(node.value)}.{node.attr}"
            return None

    def _extract_title(self, code: str, file_path: Path) -> str:
        """Extract pattern title from comments or filename"""
        # Look for title in comments
        title_match = re.search(r'#\s*Title:\s*(.+)', code, re.IGNORECASE)
        if title_match:
            return title_match.group(1).strip()

        # Use filename as fallback
        return file_path.stem.replace('_', ' ').title()

    def _extract_description(self, code: str) -> str:
        """Extract description from module docstring"""
        try:
            tree = ast.parse(code)
            docstring = ast.get_docstring(tree)
            if docstring:
                return docstring.strip()
        except:
            pass

        # Look for description in comments
        desc_match = re.search(r'#\s*Description:\s*(.+)', code, re.IGNORECASE)
        if desc_match:
            return desc_match.group(1).strip()

        return ""

    def _extract_objective(self, crews: List[Dict], tasks: List[Dict]) -> str:
        """Extract overall objective from crew or tasks"""
        if crews and len(tasks) > 0:
            # Combine task descriptions as objective
            descriptions = [task.get("description", "") for task in tasks[:2]]
            return " ".join(descriptions)[:200]
        return ""

    def _build_workflow_steps(self, agents: List[Dict], tasks: List[Dict], workflow_type: str) -> List[Dict]:
        """Build workflow steps linking agents and tasks"""
        steps = []

        for i, task in enumerate(tasks):
            # Find corresponding agent
            agent_ref = task.get("agent", "")
            agent_match = None

            for agent in agents:
                if agent.get("role") == agent_ref or agent.get("name") == agent_ref:
                    agent_match = agent
                    break

            step = {
                "order": i + 1,
                "task": task.get("description", ""),
                "agent": agent_match.get("role", "") if agent_match else agent_ref,
                "next_step": i + 2 if i < len(tasks) - 1 else None
            }
            steps.append(step)

        return steps

    def _extract_resources_from_tools(self, tools: List[Dict]) -> List[Dict]:
        """Extract resources accessed by tools"""
        resources = []
        resource_map = {
            "SearchTool": {"name": "Google Search Engine", "type": "search_engine"},
            "SerperDevTool": {"name": "Serper API", "type": "api"},
            "ScrapeWebsiteTool": {"name": "Web Scraper", "type": "web_service"},
            "FileReadTool": {"name": "File System", "type": "filesystem"},
            "DatabaseTool": {"name": "Database", "type": "database"}
        }

        for tool in tools:
            tool_type = tool.get("type", "")
            if tool_type in resource_map:
                resource_info = resource_map[tool_type].copy()
                resource_info["description"] = f"Resource accessed by {tool.get('name', tool_type)}"
                resources.append(resource_info)

        return resources

    def _link_agent_tasks(self, pattern: Dict) -> Dict:
        """Override to link agents with their tasks based on task.agent field"""
        # Create agent lookup by name/role
        agent_lookup = {}
        for agent in pattern["agents"]:
            agent_lookup[agent["name"]] = agent
            agent_lookup[agent["role"]] = agent

        # Link tasks to agents
        for task in pattern["tasks"]:
            agent_ref = task.get("assigned_agent", "")
            if agent_ref in agent_lookup:
                agent = agent_lookup[agent_ref]
                if task["id"] not in agent["tasks"]:
                    agent["tasks"].append(task["id"])
                task["assigned_agent"] = agent["id"]

        return pattern
