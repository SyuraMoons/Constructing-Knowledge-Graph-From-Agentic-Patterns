# AgentO: Agentic AI Ontology

## Overview

AgentO is an OWL ontology for representing agentic AI patterns, multi-agent systems, and workflows from popular frameworks (CrewAI, LangGraph, AutoGen, MastraAI).

**Namespace**: `http://www.w3id.org/agentic-ai/onto#`
**Prefix**: `agento:`
**Version**: 1.1.0 (Extended with AutoGen properties)

## Core Classes

| Class | Description | Example |
|-------|-------------|---------|
| `Pattern` | Complete agentic AI pattern from framework | CrewAI research team pattern |
| `Agent` | Autonomous entity capable of reasoning/acting | Researcher agent, Assistant agent |
| `Task` | Specific objective for an agent | "Collect papers from arXiv" |
| `Tool` | External capability or API | Search tool, Scraper tool |
| `Resource` | Data source or service | Google Search, Database |
| `WorkflowPattern` | Execution pattern type | Sequential, Parallel, Nested |
| `WorkflowStep` | Individual workflow step | Step 1: Research, Step 2: Write |
| `Team` | Collection of collaborating agents | Research team, Development team |
| `LLMModel` | Language model configuration | GPT-4, Claude |
| `Goal` | Objective to achieve | "Summarize research papers" |

## Object Properties (Relationships)

### Pattern-Level
- `hasAgentMember`: Pattern → Agent
- `hasWorkflowPattern`: Pattern → WorkflowPattern

### Agent-Level
- `hasTask`: Agent → Task
- `usesTool`: Agent → Tool
- `hasGoal`: Agent → Goal
- `usesLanguageModel`: Agent → LLMModel
- `delegatesTo`: Agent → Agent
- `collaboratesWith`: Agent → Agent
- `belongsToTeam`: Agent → Team

### Workflow-Level
- `hasWorkflowStep`: WorkflowPattern → WorkflowStep
- `nextStep`: WorkflowStep → WorkflowStep
- `performedBy`: WorkflowStep → Agent
- `hasAssociatedTask`: WorkflowStep → Task

### Tool/Resource
- `accessesResource`: Tool → Resource
- `assignedTo`: Task → Agent

## Datatype Properties (Attributes)

### Pattern Attributes
- `patternId`: Unique identifier (xsd:string)
- `framework`: Source framework name (xsd:string)
- `sourceFile`: Original file path (xsd:string)
- `objective`: Overall goal (xsd:string)
- `extractedFrom`: Provenance info (xsd:string)
- `extractionDate`: When extracted (xsd:dateTime)
- `extractorVersion`: Tool version (xsd:string)

### Agent Attributes
- `agentId`: Unique identifier (xsd:string)
- `agentName`: Agent name (xsd:string)
- `role`: Agent role (xsd:string)
- `description`: Agent description (xsd:string)
- `goalDescription`: Goal text (xsd:string)
- `backstory`: Background context (xsd:string)
- `hasMemory`: Memory capability (xsd:boolean)
- `vendorClass`: Framework-specific class (xsd:string)

### AutoGen-Specific Properties ⭐ NEW
- `systemMessage`: System prompt for agent (xsd:string)
- `humanInputMode`: Interaction mode - NEVER/ALWAYS/TERMINATE (xsd:string)

### Task Attributes
- `taskId`: Unique identifier (xsd:string)
- `taskTitle`: Task name (xsd:string)
- `description`: Task description (xsd:string)
- `expectedOutput`: Expected result (xsd:string)

### Tool Attributes
- `toolId`: Unique identifier (xsd:string)
- `toolName`: Tool name (xsd:string)
- `toolType`: Tool category (xsd:string)
- `description`: Tool description (xsd:string)

### Workflow Attributes
- `workflowType`: Sequential/Parallel/Nested (xsd:string)
- `stepOrder`: Execution order (xsd:integer)
- `processType`: Team coordination (xsd:string)

### Resource Attributes
- `resourceId`: Unique identifier (xsd:string)
- `resourceName`: Resource name (xsd:string)
- `resourceType`: database/api/search_engine/etc (xsd:string)
- `description`: Resource description (xsd:string)

## Extensions from Base AgentO

This version extends the original K-CAP paper ontology with:

### 1. AutoGen Framework Support
- **`systemMessage`**: Captures system prompts for `AssistantAgent`
- **`humanInputMode`**: Captures interaction modes for `UserProxyAgent`
- **`vendorClass`**: Stores framework-specific class names

### 2. Enhanced Provenance
- `extractedFrom`, `extractionDate`, `extractorVersion` for traceability

### 3. Resource Modeling
- Explicit `Resource` class for databases, APIs, search engines
- `accessesResource` property linking tools to resources

## Usage Example

```turtle
@prefix agento: <http://www.w3id.org/agentic-ai/onto#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

# Pattern
:pattern_chess_game a agento:Pattern ;
    agento:patternId "pattern_1b5dc140" ;
    agento:framework "autogen" ;
    agento:sourceFile "data/raw/autogen/chess_game.py" ;
    agento:hasAgentMember :agent_assistant, :agent_user .

# Assistant Agent
:agent_assistant a agento:Agent ;
    agento:agentId "agent_9107627a" ;
    agento:agentName "chess_game_assistant" ;
    agento:role "AssistantAgent" ;
    agento:vendorClass "AssistantAgent" ;
    agento:systemMessage "You are a helpful AI assistant for chess_game" ;
    agento:description "You are a helpful AI assistant for chess_game" .

# User Proxy Agent
:agent_user a agento:Agent ;
    agento:agentId "agent_f3cb2033" ;
    agento:agentName "user" ;
    agento:role "UserProxyAgent" ;
    agento:vendorClass "UserProxyAgent" ;
    agento:humanInputMode "NEVER" .
```

## Alignment with Standards

- **PROV-O**: `agento:Agent` is subclass of `prov:Agent`
- **Dublin Core**: Uses `dcterms:` for metadata
- **OWL 2**: Full OWL 2 DL compatibility
- **RDF/RDFS**: Standard RDF Schema patterns

## Statistics

- **Classes**: 13
- **Object Properties**: 16
- **Datatype Properties**: 32
- **Total Axioms**: 61+

## Files

- `agento.ttl` - Main ontology file (Turtle format)
- `README.md` - This documentation

## References

- K-CAP 2025 Paper: "Semantic Foundations for Modeling Agentic AI Systems"
- GitHub: https://github.com/agentic-patterns/agentic-ai-onto
- Namespace URI: http://www.w3id.org/agentic-ai/onto
