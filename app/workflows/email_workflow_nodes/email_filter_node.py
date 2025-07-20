from core.nodes.base import Node
from core.task import TaskContext
from schemas.nylas_email_schema import EmailObject, Sender
from dotenv import load_dotenv
import os
import logging

load_dotenv()


class EmailFilterNode(Node):
    def process(self, task_context: TaskContext) -> TaskContext:
        # Get email object from event
        email_object = EmailObject(**task_context.event.data["object"])

        EMAIL = os.getenv("EMAIL")

        sender: Sender = email_object.from_[0]
        if sender.email == EMAIL:
            logging.info(f"Processing email from {sender.email}")
            return task_context
        else:
            task_context.stop_workflow(
                reason=f"Email from {sender.email} is not from {EMAIL}"
            )
            logging.info(f"Skipping email from {sender.email}")
            return task_context
