# Agentic Pattern Extractors

Simple extractors for agentic AI patterns from multiple frameworks.

## Supported Frameworks

- **CrewAI**: Python-based agent definitions
- **LangGraph**: State graph configurations
- **AutoGen**: Multi-agent conversations
- **MastraAI**: JSON/YAML workflow definitions

## Installation

```bash
# Install dependencies
pip install -r ../../extractor/requirements.txt
```

## Usage

### Extract All Patterns

```bash
cd src/extractors
python main.py
```

This will:
1. Scan all files in `data/raw/{framework}/`
2. Extract agents, tasks, tools, and workflows
3. Save normalized JSON to `data/normalized/`

### Output Format

Each extracted pattern is saved as JSON with this structure:

```json
{
  "id": "pattern_xxxxx",
  "framework": "crewai",
  "source_file": "data/raw/crewai/example.py",
  "title": "Pattern Title",
  "description": "Pattern description",
  "agents": [
    {
      "id": "agent_xxxxx",
      "name": "Researcher",
      "role": "Researcher",
      "description": "...",
      "goal": "...",
      "tools": [],
      "language_model": "gpt-4",
      "memory": false
    }
  ],
  "tasks": [
    {
      "id": "task_xxxxx",
      "title": "Task name",
      "description": "...",
      "expected_output": "..."
    }
  ],
  "tools": [],
  "resources": [],
  "workflow_pattern": {
    "type": "Sequential",
    "steps": []
  }
}
```

## Directory Structure

```
data/
  raw/
    crewai/          # Put CrewAI .py files here
    langraph/        # Put LangGraph .py files here
    autogen/         # Put AutoGen .py files here
    mastraai/        # Put MastraAI .json/.yaml files here
  normalized/        # Output: extracted JSON files

src/extractors/
  base_extractor.py       # Base class
  crewai_extractor.py     # CrewAI parser
  langraph_extractor.py   # LangGraph parser
  autogen_extractor.py    # AutoGen parser
  mastraai_extractor.py   # MastraAI parser
  main.py                 # Main pipeline
```

## Framework-Specific Notes

### CrewAI
Extracts from Python files:
- `Agent(role=..., goal=..., tools=[...])`
- `Task(description=..., agent=...)`
- `Crew(agents=[...], tasks=[...])`

### LangGraph
Extracts from Python files:
- `StateGraph()` definitions
- `.add_node()` calls
- Agent and tool definitions

### AutoGen
Extracts from Python files:
- `AssistantAgent(name=..., system_message=...)`
- `UserProxyAgent(...)`

### MastraAI
Extracts from JSON/YAML files:
- `agents` array
- `workflows` array

## Testing

```bash
cd tests
python test_extractors.py
```

## Troubleshooting

**No files found:**
- Make sure files are in correct `data/raw/{framework}/` directory
- Check file extensions (.py, .json, .yaml, .yml)

**Extraction failed:**
- Check Python syntax for .py files
- Check JSON/YAML validity for config files
- Review error messages in console output

## Example Commands

```bash
# Extract only CrewAI patterns
python -c "from crewai_extractor import CrewAIExtractor; CrewAIExtractor().process_file('../../data/raw/crewai/example1.py')"

# Count extracted patterns
ls ../../data/normalized/ | wc -l
```

## Output Statistics

After running, you'll see:
```
📊 EXTRACTION SUMMARY
==================================================
Total files processed: 50
Successfully extracted: 48
Failed: 2
Output directory: /path/to/data/normalized
==================================================
```
