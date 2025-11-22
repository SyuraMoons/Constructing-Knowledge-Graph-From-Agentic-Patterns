# Constructing Knowledge Graph From Agentic Patterns

Convert analyzed agent-pattern `.txt` files into normalized JSON structures for downstream ontology and knowledge-graph generation.

## Overview

This tool processes agentic-pattern summaries from frameworks such as AutoGen, LangGraph, CrewAI, and MastraAI.
Using your standardized text-table pattern format, the parser extracts entities, relationships, and ontology terms, then outputs normalized JSON suitable for RDF/Turtle conversion.

The project uses a clear multi-stage workflow:

* **raw_data/** – Optional original pattern files
* **analyzed_data/** – Cleaned and structured `.txt` analysis outputs
* **json_data/** – Final normalized JSON extracted from each pattern

---

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Prepare Your Input Files

Place your analyzed GDocs-table text summaries into:

```
data/analyzed_data/<framework_name>/*.txt
```

Example directory structure:

```
data/analyzed_data/
    autogen/
    crewai/
    langgraph/
    mastra/
```

### 3. Convert TXT → JSON

Run the parser:

```bash
py parser.py
```

The parser will:

* Scan all framework folders under `data/analyzed_data/`
* Extract structured fields using your section-based logic
* Generate matching folders under:

```
data/json_data/<framework_name>/*.json
```

---

## Output Example

Example generated JSON directory:

```
data/json_data/
    autogen/
        chess_game.json
    crewai/
        recruiter_team.json
```

Example normalized JSON structure:

```json
{
  "framework": "AutoGen",
  "file_name": "chess_game.py",
  "pattern_type": "AgentCollaboratorPattern",
  "entities": [...],
  "ontologyRelationalProperties": [...],
  "newOntologyTerms": {...}
}
```

---

## Project Structure

```
CONSTRUCTING-KNOWLEDGE-GRAPH/
├── data/
│   ├── raw_data/         # Original framework files
│   ├── analyzed_data/    # Cleaned .txt pattern summaries
│   └── json_data/        # JSON output from parser
├── parser.py             # TXT → JSON converter
├── requirements.txt
└── README.md
```

---

## Pipeline Summary

1. **Pattern Input** – Place analyzed `.txt` files into framework folders
2. **Pattern Parsing** – The extractor identifies entities, relations, ontology mappings
3. **Normalization** – JSON is produced in a consistent, ontology-aligned structure

---

## Requirements

See `requirements.txt` for all Python dependencies.

---

## License

MIT

---

If you want a GitHub-badge version, a Mermaid diagram, or an academic version, just tell me.
