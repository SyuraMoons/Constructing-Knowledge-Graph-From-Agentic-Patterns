# Agentic Pattern Extractor

Automated extraction and normalization of agentic AI design patterns from multiple frameworks.

## Overview

Extracts agent definitions, tasks, tools, and workflows from CrewAI, LangGraph, AutoGen, and MastraAI frameworks into standardized JSON format.

## Installation

```bash
pip install -r requirements.txt
```

## Quick Start

```bash
# Run the extractor
cd src/extractors
python main.py

# Check output
ls ../../data/normalized/
```

## Project Structure

```
agentic-kg-extractor/
├── src/extractors/          # Extractor modules
│   ├── main.py              # Main pipeline
│   ├── base_extractor.py    # Base class
│   ├── crewai_extractor.py  # CrewAI parser
│   ├── langraph_extractor.py
│   ├── autogen_extractor.py
│   ├── mastraai_extractor.py
│   └── README.md            # Detailed docs
├── data/
│   ├── raw/                 # Input: 51 pattern files
│   └── normalized/          # Output: 102 JSON files
├── tests/
│   └── test_extractors.py
└── scripts/
    └── agentic_pattern.schema.json
```

## Usage

### Extract Patterns

```bash
cd src/extractors
python main.py
```

### Add New Patterns

1. Add files to `data/raw/{framework}/`
   - `.py` files for CrewAI, LangGraph, AutoGen
   - `.json/.yaml` files for MastraAI
2. Run `python src/extractors/main.py`
3. Find output in `data/normalized/`

### Run Tests

```bash
cd tests
python test_extractors.py
```

## Output Format

```json
{
  "id": "pattern_xxxxx",
  "framework": "crewai",
  "agents": [{
    "id": "agent_xxx",
    "name": "Researcher",
    "role": "Research Specialist",
    "description": "...",
    "tools": [...]
  }],
  "tasks": [...],
  "workflow_pattern": {...},
  "provenance": {...}
}
```

## Current Stats

- ✅ 51 input pattern files
- ✅ 102 normalized JSON outputs
- ✅ 4 frameworks supported
- ✅ 100% extraction success

## Documentation

See `src/extractors/README.md` for detailed documentation.
