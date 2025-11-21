# Data Sources

This document lists the original sources for the 51 agentic pattern files used in this knowledge graph extraction project.

## Overview

All pattern files in `data/raw/` are based on official examples and tutorials from the respective framework repositories. These examples have been adapted and simplified for educational purposes as part of the Web Semantik assignment (Kelompok 3).

---

## CrewAI Examples (14 files)

**Official Repository**: [crewAIInc/crewAI-examples](https://github.com/crewAIInc/crewAI-examples)
**Main Repository**: [crewAIInc/crewAI](https://github.com/crewAIInc/crewAI)
**License**: MIT License
**Documentation**: https://docs.crewai.com/

### Pattern Files

| File | Based On | Description |
|------|----------|-------------|
| `content_writer.py` | Content Creator Flow | Multi-crew content generation system |
| `customer_support.py` | Email Auto Responder Flow | Automated email monitoring and response |
| `data_analyst.py` | Stock Analysis | Financial data analysis crew |
| `finance_team.py` | Stock Analysis | Financial analysis with SEC data |
| `hr_assistant.py` | Recruitment / Job Posting | HR automation and candidate evaluation |
| `legal_advisor.py` | Custom pattern | Legal consultation crew |
| `marketing_team.py` | Marketing Strategy / Instagram Post | Marketing campaign development |
| `product_manager.py` | Custom pattern | Product management crew |
| `project_manager.py` | Prep for a Meeting | Meeting preparation and project planning |
| `qa_tester.py` | Markdown Validator | Quality assurance and testing crew |
| `researcher_team.py` | Industry Agents | Research and information gathering |
| `sales_team.py` | Lead Score Flow | Lead qualification and sales automation |
| `software_dev.py` | Game Builder Crew | Software development crew |
| `example1.py` | Starter Template | Basic CrewAI template |

**Notes**:
- Examples based on CrewAI v0.152.0 patterns
- Adapted from Flows and Crews examples in the official repository
- Simplified for educational and extraction purposes

---

## LangGraph Examples (13 files)

**Official Repository**: [langchain-ai/langgraph](https://github.com/langchain-ai/langgraph)
**Tutorial Repository**: [langchain-ai/langgraph-101](https://github.com/langchain-ai/langgraph-101)
**License**: MIT License
**Documentation**: https://langchain-ai.github.io/langgraph/

### Pattern Files

| File | Based On | Description |
|------|----------|-------------|
| `supervisor.py` | [Multi-Agent Supervisor Tutorial](https://github.com/langchain-ai/langgraph/blob/main/docs/docs/tutorials/multi_agent/agent_supervisor.md) | Central supervisor coordinating specialized agents |
| `multi_agent.py` | Multi-Agent Concepts | Multi-agent collaboration patterns |
| `researcher.py` | Agent Supervisor Tutorial | Research specialist agent |
| `executor.py` | State Graph examples | Task execution agent |
| `planner.py` | Planning patterns | Task planning and breakdown |
| `writer.py` | Content generation patterns | Content writing agent |
| `synthesizer.py` | Information synthesis patterns | Data synthesis and aggregation |
| `reviewer.py` | Review/validation patterns | Content review and quality check |
| `router.py` | Routing patterns | Request routing and delegation |
| `analyzer.py` | Analysis patterns | Data analysis agent |
| `aggregator.py` | Aggregation patterns | Information aggregation |
| `classifier.py` | Classification patterns | Input classification |
| `simple_graph.py` | Getting Started examples | Basic StateGraph implementation |

**Notes**:
- Based on LangGraph v1.0.0+ concepts
- Patterns derived from official tutorials and documentation
- Simplified StateGraph implementations for extraction

**Key References**:
- Supervisor pattern: `docs/tutorials/multi_agent/agent_supervisor.md`
- Multi-agent concepts: `docs/concepts/multi_agent.md`
- Python supervisor template: [langgraph-supervisor-py](https://github.com/langchain-ai/langgraph-supervisor-py)

---

## AutoGen Examples (12 files)

**Official Repository**: [microsoft/autogen](https://github.com/microsoft/autogen)
**Current Version**: AutoGen 0.2 (maintained with bug fixes)
**License**: MIT License
**Documentation**: https://microsoft.github.io/autogen/

### Pattern Files

| File | Based On | Description |
|------|----------|-------------|
| `chess_game.py` | [agentchat_nested_chats_chess.ipynb](https://github.com/microsoft/autogen/blob/0.2/notebook/agentchat_nested_chats_chess.ipynb) | Nested chats for conversational chess |
| `two_agent_chat.py` | [agentchat_two_users.ipynb](https://github.com/microsoft/autogen/blob/0.2/notebook/agentchat_two_users.ipynb) | Two-agent collaborative task solving |
| `group_chat.py` | Group Chat examples | Multi-agent group conversation |
| `function_calling.py` | Tool use examples | Function/tool calling patterns |
| `planning_agent.py` | Planning examples | Task planning and breakdown |
| `teaching_agent.py` | Teaching examples | Educational agent interactions |
| `feedback_agent.py` | Feedback patterns | Iterative feedback loops |
| `code_execution.py` | Code execution examples | Automated code generation and execution |
| `web_search.py` | Tool integration examples | Web search integration |
| `stream_chat.py` | Streaming examples | Streaming conversation patterns |
| `human_feedback.py` | Human-in-the-loop examples | Human feedback integration |
| `retrieve_chat.py` | RAG examples | Retrieval augmented generation |

**Notes**:
- Based on AutoGen 0.2 notebook examples
- Simplified AssistantAgent and UserProxyAgent patterns
- `humanInputMode` set to "NEVER" for autonomous operation
- Examples from `notebook/` directory in main repository

**Key Features Demonstrated**:
- AssistantAgent with system_message configuration
- UserProxyAgent for task coordination
- Group chat with multiple agents
- Tool/function calling capabilities
- Human-in-the-loop workflows

---

## MastraAI Examples (12 files)

**Official Repository**: [mastra-ai/mastra](https://github.com/mastra-ai/mastra)
**Framework Type**: TypeScript AI agent framework
**License**: MIT License
**Documentation**: https://mastra.ai/

### Pattern Files

**JSON Files** (9):

| File | Description |
|------|-------------|
| `code_review.json` | Automated code review agent |
| `research_workflow.json` | Research and information gathering |
| `data_analysis.json` | Data analysis and insights |
| `content_creation.json` | Content generation agent |
| `social_media.json` | Social media management |
| `translation_service.json` | Translation and localization |
| `document_processor.json` | Document processing and extraction |
| `hr_assistant.json` | HR automation workflows |
| `simple_agent.json` | Basic agent template |

**YAML Files** (3):

| File | Description |
|------|-------------|
| `customer_support.yaml` | Customer support automation |
| `meeting_assistant.yaml` | Meeting coordination and notes |
| `email_automation.yaml` | Email workflow automation |

**Notes**:
- Adapted from Mastra TypeScript framework patterns
- Converted to JSON/YAML for configuration-based extraction
- Uses GPT-4 model references as default
- Simplified for demonstration purposes

**Framework Features**:
- Support for multiple LLMs (GPT-4, Claude, Gemini, Llama)
- RAG (Retrieval Augmented Generation) capabilities
- Observability and monitoring
- Built-in integrations

---

## Attribution and Usage

### Educational Use
These files have been collected and adapted for educational purposes as part of the **Web Semantik - Kelompok 3** university assignment on "Constructing Knowledge Graph from Agentic AI Patterns."

### Modifications
Original examples have been:
- Simplified to focus on core agent/task/tool patterns
- Normalized to consistent file formats
- Adapted for AST-based extraction
- Stripped of implementation details to focus on structure

### Licenses
All source frameworks use **MIT License**, which permits:
- ✅ Commercial use
- ✅ Modification
- ✅ Distribution
- ✅ Private use

**Requirements**:
- Include original license and copyright notice
- No warranty provided

### Original Licenses

**CrewAI**: Copyright (c) 2024 CrewAI Inc. - MIT License
**LangGraph**: Copyright (c) 2024 LangChain Inc. - MIT License
**AutoGen**: Copyright (c) Microsoft Corporation - MIT License
**Mastra**: Copyright (c) 2024 Mastra AI - MIT License

---

## How to Verify Sources

To verify the original sources for any pattern:

1. **Check the framework's official repository**:
   ```bash
   # CrewAI
   git clone https://github.com/crewAIInc/crewAI-examples

   # LangGraph
   git clone https://github.com/langchain-ai/langgraph

   # AutoGen
   git clone https://github.com/microsoft/autogen

   # Mastra
   git clone https://github.com/mastra-ai/mastra
   ```

2. **Browse examples online**:
   - CrewAI: https://github.com/crewAIInc/crewAI-examples
   - LangGraph: https://langchain-ai.github.io/langgraph/examples/
   - AutoGen: https://microsoft.github.io/autogen/0.2/docs/Examples/
   - Mastra: https://github.com/mastra-ai/mastra

3. **Read official documentation**:
   - CrewAI: https://docs.crewai.com/
   - LangGraph: https://langchain-ai.github.io/langgraph/
   - AutoGen: https://microsoft.github.io/autogen/
   - Mastra: https://mastra.ai/

---

## Updates and Maintenance

**Last Updated**: November 19, 2025
**Frameworks Versions**:
- CrewAI: v0.152.0
- LangGraph: v1.0.0+
- AutoGen: v0.2 (maintained)
- Mastra: Latest (TypeScript framework)

**Maintained By**: Web Semantik - Kelompok 3
**Contact**: [Your contact information]

---

## Additional Resources

### Related Projects
- AgentO Ontology: `ontology/agento.ttl`
- Extraction Pipeline: `src/extractors/`
- RDF Conversion: `scripts/json_to_rdf.py`

### Academic Context
This data collection is part of a knowledge graph construction project analyzing agentic AI design patterns across multiple frameworks for semantic web research.

### Citation
If you use this dataset or extraction pipeline, please cite:
```
Web Semantik Kelompok 3 (2025). Agentic Knowledge Graph Extractor.
Based on official examples from CrewAI, LangGraph, AutoGen, and MastraAI frameworks.
https://github.com/[your-repo]
```
