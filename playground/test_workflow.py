import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent) + "/app")
import logging

import nest_asyncio
from utils.event_loader import EventLoader
from workflows.email_workflow import EmailWorkflow
from schemas.nylas_webhook_schema import WebhookEvent
from schemas.nylas_email_schema import EmailObject


nest_asyncio.apply()

logging.basicConfig(level=logging.INFO)


# --------------------------------------------------------------
# Load event (update with your event uuid)
# --------------------------------------------------------------

message_event = EventLoader.load_event(
    "925d1e9c-61c5-11f0-82c6-784f439cdd7a"
)  # update with your event uuid
spam_event = EventLoader.load_event(
    "925d1e9c-61c5-11f0-82c6-784f439cdd7a"
)  # update with your event uuid
invoice_event = EventLoader.load_event(
    "925d1e9c-61c5-11f0-82c6-784f439cdd7a"
)  # update with your event uuid


# --------------------------------------------------------------
# Run workflow
# --------------------------------------------------------------

workflow = EmailWorkflow()
result = workflow.run(message_event)
print(result.model_dump_json(indent=4))
#print(result.nodes["ClassificationNode"]["result"].output.category)

# This code simply parses the event into a pydantic object
# and prints it out 
#webhook_event = WebhookEvent(**message_event)
#email = EmailObject(**webhook_event.data["object"])
#print(webhook_event.model_dump_json(indent=4))
