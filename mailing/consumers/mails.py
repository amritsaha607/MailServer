
import logging

from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from mailing.consumers.utils import get_group_name, user_to_channel_mappings
from mailing.helper import get_user_by_email

logger = logging.getLogger(__name__)


class MailConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        # Accept the connection
        await self.accept()

        # Initialize identifiers
        self.user_id = self.scope['url_route']['kwargs']['user']

        user_to_channel_mappings[self.user_id].append(self.channel_name)

    async def disconnect(self, code):

        # Fetch all email items
        mails = await self.fetch_mail_events()

        # For all mail items create group and add user to the corresponding group
        await self.remove_from_mail_group(mails)

        user_to_channel_mappings[self.user_id].remove(self.channel_name)

        return await super().disconnect(code)

    async def receive_json(self, content: dict, **kwargs):
        logger.info(f'Received json content: {content}')
        mode = content.get('mode')

        await self.execute_action(mode)

    @database_sync_to_async
    def fetch_mail_events(self):
        user = get_user_by_email(self.user_id)
        return user.get_mail_events()

    async def add_to_multiple_mail_groups(self, mails):
        async for mail in mails:
            await self.add_to_mail_group(mail)

    async def add_to_mail_group(self, mail):
        group_name = get_group_name(mail.chain_id)
        await self.channel_layer.group_add(
            group_name,
            self.channel_name,
        )
        logger.info(f'added user {self.channel_name} to group {group_name}')

    @sync_to_async
    def remove_from_mail_group(self, mails):
        for mail in mails:
            group_name = get_group_name(mail.chain_id)
            self.channel_layer.group_discard(
                group_name,
                self.channel_name,
            )
            logger.info(f'removed user {self.user_id} from group {group_name}')

    async def send_mail_event_notification(self, event):

        # Receive data from room group
        event_data = event['data']

        # Send message to WebSocket
        await self.send_json(event_data)

    async def execute_action(self, mode):
        if mode == 'boot':
            await self.execute_boot_action()

    # Action methods

    async def execute_boot_action(self):
        # Fetch all email items
        mails = await self.fetch_mail_events()

        # For all mail items create group and add user to the corresponding group
        await self.add_to_multiple_mail_groups(mails)
