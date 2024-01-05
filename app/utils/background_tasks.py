from typing import Any

from app.constant.template import NotificationTemplate
from app.models.base import NotificationType
from app.services import NotificationService


async def send_notification(
        notification_service: NotificationService,
        user_id: int,
        entity: Any,
        message_template: NotificationTemplate,
        action: str,
        username: str = None,
        entities_name: str = None
):
    await notification_service.notify_entity_status(
        user_id=user_id,
        entity=entity,
        notification_type=NotificationType.PROJECT_NOTIFICATION,
        message_template=message_template,
        action=action,
        username=username,
        entities_name=entities_name
    )

