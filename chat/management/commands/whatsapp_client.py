import asyncio
import logging
from django.core.management.base import BaseCommand
from neonize.client import NewClient
from neonize.events import ConnectedEv, MessageEv

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Starts the WhatsApp client'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('WhatsApp client started successfully.'))
        asyncio.run(self.start_client())
        self.stdout.write(self.style.SUCCESS('WhatsApp client started successfully.'))

    async def start_client(self):
        client = NewClient("session_db.sqlite3")

        @client.event(ConnectedEv)
        def on_connected(client, event):
            logger.info("Connected to WhatsApp")

        @client.event(MessageEv)
        def on_message(client, message):
            chat = message.Info.MessageSource.Chat
            text = message.Message.conversation or message.Message.extendedTextMessage.text
            logger.info(f"Received message: {text} from {chat}")
            # Save message to the database
            from chat.models import Message
            Message.objects.create(
                chat_id=chat,
                sender=message.Info.MessageSource.Sender,
                content=text
            )

        await client.connect()
        await client.wait_for_login()
        await client.run_forever()
