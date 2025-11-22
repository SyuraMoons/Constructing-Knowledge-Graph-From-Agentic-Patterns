"""[OntologyMetadata]
{
    "framework": "AutoGen",
    "file_name": "feedback_agent.py",
    "pattern_type": "AgentCollaboratorPattern",
    "description": "Two agents (assistant and user proxy) interacting in a feedback_agent context.",

    "entities": [
        {
            "id": "assistant",
            "vendorClass": "AssistantAgent",
            "mapsTo": "agento:Agent",
            "attributes": {
                "name": "feedback_agent_assistant",
                "systemMessage": "You are a helpful AI assistant for feedback_agent"
            },
            "relations": { }
        },
        {
            "id": "user_proxy",
            "vendorClass": "UserProxyAgent",
            "mapsTo": "agento:Agent",
            "attributes": {
                "name": "user",
                "humanInputMode": "NEVER"
            },
            "relations": { }
        }
    ],

    "ontologyRelationalProperties": [
        {
            "name": "participatesIn",
            "domain": "agento:Agent",
            "range": "agento:Evaluation",
            "definition": "Indicates that an agent participates in an evaluation activity.",
            "status_in_pattern": "suggested"
        },
        {
            "name": "evaluates",
            "domain": "agento:Agent",
            "range": "agento:Artifact",
            "definition": "Agent gives feedback on an artifact.",
            "status_in_pattern": "suggested"
        },
        {
            "name": "delegatesTo",
            "domain": "agento:Agent",
            "range": "agento:Agent",
            "definition": "Indicates that one agent delegates a task to another.",
            "status_in_pattern": "not_used"
        },
        {
            "name": "hasRole",
            "domain": "agento:Agent",
            "range": "agento:Role",
            "definition": "Specifies the role of an agent in a feedback activity.",
            "status_in_pattern": "optional"
        }
    ],

    "newOntologyTerms": {
        "newClasses": [
            {
                "name": "agento:Evaluation",
                "definition": "Represents feedback activity performed by an agent.",
                "status_in_pattern": "used"
            },
            {
                "name": "agento:Artifact",
                "definition": "Represents the artifact or output being evaluated.",
                "status_in_pattern": "used"
            }
        ],
        "datatypeProperties": [
            {
                "name": "name",
                "domain": "agento:Agent",
                "range": "xsd:string",
                "justification": "Every agent in the code declares a unique name."
            },
            {
                "name": "systemMessage",
                "domain": "agento:Agent",
                "range": "xsd:string",
                "justification": "Appears as system_message in AssistantAgent."
            },
            {
                "name": "humanInputMode",
                "domain": "agento:Agent",
                "range": "xsd:string",
                "justification": "Appears in UserProxyAgent."
            }
        ],
        "optionalProperties": [
            {
                "name": "vendorClass",
                "domain": "agento:Agent",
                "range": "xsd:string",
                "justification": "Allows cross-framework mapping of class names."
            }
        ]
    }
}
[/OntologyMetadata]"""

"""AutoGen pattern: feedback_agent"""
from autogen import AssistantAgent, UserProxyAgent

# Define agents
assistant = AssistantAgent(
    name="feedback_agent_assistant",                    # Agent.name
    system_message="You are a helpful AI assistant for feedback_agent"  # Agent.systemMessage
)

user_proxy = UserProxyAgent(
    name="user",                                        # Agent.name
    human_input_mode="NEVER"                            # Agent.humanInputMode
)


