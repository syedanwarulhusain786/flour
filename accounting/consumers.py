from channels.generic.websocket import AsyncWebsocketConsumer
import json

class PurchaseQuotationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        # Handle any incoming WebSocket messages if needed
        pass

    async def purchase_order_update(self, event):
        message = event['message']
        created_at = event['created_at']
        purchase_order_number = event['purchase_order_number']

        await self.send(text_data=json.dumps({
            'message': message,
            'created_at': created_at,
            'purchase_order_number': purchase_order_number,
        }))

    async def send_purchase_quotation_update(self, quotation_data):
            await self.send(text_data=json.dumps({
                'type': 'purchase_quotation_update',
                'data': quotation_data,
            }))

    async def broadcast_purchase_quotation_update(self, quotation_data):
        for channel_name in PurchaseQuotationConsumer.connected_clients:
            await self.channel_layer.send(
                channel_name,
                {
                    'type': 'send.purchase_quotation_update',
                    'data': quotation_data,
                }
            )

    async def receive(self, text_data):
        # Handle incoming WebSocket messages
        data = json.loads(text_data)
        message_type = data.get('type')

        if message_type == 'purchase_quotation_update':
            quotation_data = data.get('data')
            await self.send_purchase_quotation_update(quotation_data)