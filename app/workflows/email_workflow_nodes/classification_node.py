from core.nodes.agent import AgentNode
from core.task import TaskContext
from dotenv import load_dotenv
from enum import Enum
from pydantic import Field
from pydantic_ai import RunContext

from core.nodes.agent import AgentConfig, ModelProvider
from schemas.nylas_email_schema import EmailObject

load_dotenv()


class EmailCategory(str, Enum):
    SPAM = "spam"
    MESSAGE = "message"
    INVOICE = "invoice"
    OTHER = "other"


PROMPT = """
You are a helpful assistant that classifies emails into one of the following categories:
- SPAM
- MESSAGE
- INVOICE
- OTHER
"""


class ClassificationNode(AgentNode):
    class OutputType(AgentNode.OutputType):
        category: EmailCategory
        confidence: float = Field(
            ge=0, le=1, description="Confidence score for the category"
        )

    class DepsType(AgentNode.DepsType):
        from_email: str = Field(..., description="Email address of the sender")
        sender: str = Field(..., description="Name or identifier of the sender")
        subject: str = Field(..., description="Subject of the ticket")
        body: str = Field(..., description="The body of the ticket")

    def get_agent_config(self) -> AgentConfig:
        return AgentConfig(
            system_prompt=PROMPT,
            output_type=self.OutputType,
            deps_type=self.DepsType,
            model_provider=ModelProvider.OPENAI,
            model_name="gpt-4o-mini",
        )

    def process(self, task_context: TaskContext) -> TaskContext:
        email_object = EmailObject(**task_context.event.data["object"])
        deps = self.DepsType(
            from_email=email_object.from_[0].email,
            sender=email_object.from_[0].name,
            subject=email_object.subject,
            body=email_object.body,
        )

        @self.agent.system_prompt
        def add_ticket_context(
            ctx: RunContext[ClassificationNode.DepsType],
        ) -> str:
            return deps.model_dump_json(indent=2)

        result = self.agent.run_sync(
            user_prompt="Classify this email",
        )

        task_context.update_node(node_name=self.node_name, result=result)
        return task_context
