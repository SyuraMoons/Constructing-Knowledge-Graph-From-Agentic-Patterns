# Kelompok 3 Progress Report

## Assignment: Constructing Knowledge Graph from Agentic AI Patterns

### Completed Tasks ✅

#### 1. AgentO Ontology Development ✅
- **Created**: `ontology/agento.ttl` (Extended AgentO ontology v1.1.0)
- **Extensions Added**:
  - AutoGen-specific properties: `systemMessage`, `humanInputMode`, `vendorClass`
  - Enhanced provenance: `extractedFrom`, `extractionDate`, `extractorVersion`
  - Resource modeling: `Resource` class with `accessesResource` property
- **Classes**: 13 (Pattern, Agent, Task, Tool, Resource, Workflow types, etc.)
- **Object Properties**: 16 (hasTask, usesTool, hasGoal, etc.)
- **Datatype Properties**: 32 (agentName, role, description, humanInputMode, etc.)
- **Documentation**: `ontology/README.md` with full specification

#### 2. Extraction Pipeline ✅
- **Tool**: Multi-framework extractor in `src/extractors/`
- **Frameworks Supported**: 4 (CrewAI, LangGraph, AutoGen, MastraAI)
- **Patterns Extracted**: 51 patterns from 51 source files
- **Success Rate**: 100% JSON extraction
- **Output**: `data/normalized/` - 51 JSON files

#### 3. JSON → RDF Conversion ✅
- **Tool**: `scripts/json_to_rdf.py`
- **Successful Conversions**: 51/51 (100%)
- **Failed**: 0/51 (URI encoding issue fixed)
- **Total Triples**: 1,539 triples in merged file
- **Output**: `data/rdf/agentic-patterns.ttl`

#### 4. Fix URI Encoding Issues ✅
- **Problem**: Task descriptions with spaces (e.g., "Collect papers from arXiv") created invalid URIs
- **Solution**: URL-encode all identifiers using `urllib.parse.quote()`
- **Impact**: Fixed! Now 51/51 patterns successfully converted to RDF

### In Progress / Pending ⏳

#### 5. SPARQL Endpoint Setup ⏳
- **Tool**: Qlever (recommended) or Virtuoso
- **Status**: Not yet installed
- **Requirement**: Load RDF data and provide queryable endpoint

#### 6. KG Statistics & Evaluation ⏳
- **Required Metrics**:
  - Total triples, agents, tasks, tools, workflows
  - Completeness by framework
  - Missing attributes analysis
  - Error detection
- **Output Format**: Tables, charts, statistics report
- **Status**: Script not yet created

#### 7. Use Case Demonstrations ⏳
- **Required**: 3 real-world use cases
- **Suggested** (from paper):
  1. Pattern Reconstruction (SPARQL visualization)
  2. Cross-Framework Reusability (query agents by role)
  3. Implementation Auditing (trace workflows)
- **Status**: Not yet started

### Current Statistics

| Metric | Count | Status |
|--------|-------|--------|
| Input Pattern Files | 51 | ✅ Complete |
| Frameworks Covered | 4 | ✅ Complete |
| JSON Normalized Patterns | 51 | ✅ Complete |
| RDF Patterns (successful) | 51 | ✅ Complete |
| RDF Patterns (failed) | 0 | ✅ Fixed |
| Total RDF Triples | 1,539 | ✅ Complete |
| Ontology Classes | 13 | ✅ Complete |
| Ontology Properties | 48 | ✅ Complete |

### Files Created

**Ontology**:
- `ontology/agento.ttl` - AgentO ontology (extended)
- `ontology/README.md` - Ontology documentation

**Code**:
- `src/extractors/` - Pattern extractors (7 files)
- `scripts/json_to_rdf.py` - RDF converter

**Data**:
- `data/normalized/` - 51 JSON patterns
- `data/rdf/` - 51 TTL files + merged file (agentic-patterns.ttl)

**Documentation**:
- `README.md` - Project overview
- `ontology/README.md` - Ontology specification
- `src/extractors/README.md` - Extractor usage

### Next Steps (Priority Order)

1. **Setup SPARQL Endpoint** (2-3 hours)
   - Install Qlever via Docker
   - Load RDF data
   - Test queries
   - Document access

3. **Generate Statistics** (2-3 hours)
   - Create analysis script
   - Generate tables/charts
   - Write evaluation report

4. **Create Use Cases** (3-4 hours)
   - Develop 3 SPARQL-based demonstrations
   - Create notebooks/scripts
   - Document findings

### Estimated Completion

- **Current Progress**: ~60%
- **Remaining Work**: 6-10 hours
- **Target**: Full completion within 1-2 days

### GitHub Repository Structure

```
agentic-kg-extractor/
├── ontology/
│   ├── agento.ttl              ✅ Done
│   └── README.md               ✅ Done
├── src/extractors/             ✅ Done
│   ├── *.py (7 files)
│   └── README.md
├── data/
│   ├── raw/                    ✅ Done (51 files)
│   ├── normalized/             ✅ Done (51 JSON)
│   └── rdf/                    ✅ Done (51 TTL + merged)
├── scripts/
│   ├── json_to_rdf.py          ✅ Done
│   ├── statistics.py           ⏳ TODO
│   └── sparql_queries/         ⏳ TODO
├── evaluation/                 ⏳ TODO
│   ├── statistics.md
│   └── charts/
├── use-cases/                  ⏳ TODO
│   ├── use-case-1.ipynb
│   ├── use-case-2.ipynb
│   └── use-case-3.ipynb
└── README.md                   ✅ Done
```

### Known Issues

1. ~~**URI Encoding**: 27 patterns fail RDF serialization due to spaces in URIs~~ ✅ FIXED
2. **Incomplete Workflow Steps**: Some patterns have empty workflow steps
3. **Missing Tool/Resource Links**: Not all tools have associated resources

### Questions for Review

1. ~~Should we prioritize fixing all 51 RDF conversions before SPARQL endpoint?~~ ✅ All 51 patterns now converted
2. Which SPARQL endpoint is preferred: Qlever or Virtuoso?
3. Are there specific use cases beyond the 3 mentioned in the paper?

---

**Last Updated**: November 17, 2025
**Team**: Kelompok 3 - Web Semantik
