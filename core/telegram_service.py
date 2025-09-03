"""
Telegram Bot integration for demo bot generation
"""
import asyncio
import requests
from django.conf import settings
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)


class TelegramBotService:
    """
    Service for interacting with Telegram Bot API
    """
    
    def __init__(self, bot_token: Optional[str] = None):
        self.bot_token = bot_token or getattr(settings, 'TELEGRAM_BOT_TOKEN', None)
        self.base_url = f"https://api.telegram.org/bot{self.bot_token}"
    
    def is_configured(self) -> bool:
        """Check if bot token is configured"""
        return bool(self.bot_token)
    
    def get_bot_info(self) -> Dict:
        """Get bot information"""
        try:
            response = requests.get(f"{self.base_url}/getMe", timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Failed to get bot info: {e}")
            return {"ok": False, "error": str(e)}
    
    def create_demo_bot(self, template_id: int, user_telegram: str) -> Dict:
        """
        Create a demo bot based on template
        This is a simplified implementation for demo purposes
        """
        try:
            if not self.is_configured():
                return {
                    "success": False,
                    "error": "Telegram bot not configured"
                }
            
            # In a real implementation, this would:
            # 1. Generate bot code based on template
            # 2. Deploy to a sandbox environment
            # 3. Create a temporary bot instance
            # 4. Return access details
            
            # For demo purposes, return mock data
            demo_bot_data = {
                "success": True,
                "bot_username": f"demo_bot_{template_id}_{user_telegram}",
                "demo_url": f"https://t.me/demo_bot_{template_id}_{user_telegram}",
                "expires_at": "2024-12-31T23:59:59Z",
                "commands": [
                    "/start - Start the bot",
                    "/help - Get help",
                    "/demo - See demo features"
                ],
                "features": [
                    "Interactive menu",
                    "Sample responses",
                    "Basic commands"
                ]
            }
            
            logger.info(f"Demo bot created for template {template_id}, user {user_telegram}")
            return demo_bot_data
            
        except Exception as e:
            logger.error(f"Failed to create demo bot: {e}")
            return {
                "success": False,
                "error": f"Failed to create demo bot: {str(e)}"
            }
    
    def delete_demo_bot(self, bot_username: str) -> bool:
        """
        Delete a demo bot
        """
        try:
            # In a real implementation, this would clean up the demo bot
            logger.info(f"Demo bot {bot_username} deleted")
            return True
        except Exception as e:
            logger.error(f"Failed to delete demo bot {bot_username}: {e}")
            return False


class TelegramPaymentService:
    """
    Service for Telegram Payments API integration
    """
    
    def __init__(self, bot_token: Optional[str] = None, provider_token: Optional[str] = None):
        self.bot_token = bot_token or getattr(settings, 'TELEGRAM_BOT_TOKEN', None)
        self.provider_token = provider_token or getattr(settings, 'TELEGRAM_PROVIDER_TOKEN', None)
        self.base_url = f"https://api.telegram.org/bot{self.bot_token}"
    
    def is_configured(self) -> bool:
        """Check if payment tokens are configured"""
        return bool(self.bot_token and self.provider_token)
    
    def create_invoice(self, 
                      chat_id: str,
                      title: str,
                      description: str,
                      payload: str,
                      currency: str,
                      prices: list) -> Dict:
        """
        Create a Telegram payment invoice
        """
        try:
            if not self.is_configured():
                return {
                    "success": False,
                    "error": "Telegram payments not configured"
                }
            
            invoice_data = {
                "chat_id": chat_id,
                "title": title,
                "description": description,
                "payload": payload,
                "provider_token": self.provider_token,
                "currency": currency,
                "prices": prices
            }
            
            response = requests.post(
                f"{self.base_url}/sendInvoice",
                json=invoice_data,
                timeout=10
            )
            response.raise_for_status()
            
            result = response.json()
            if result.get("ok"):
                return {
                    "success": True,
                    "message_id": result["result"]["message_id"]
                }
            else:
                return {
                    "success": False,
                    "error": result.get("description", "Unknown error")
                }
                
        except Exception as e:
            logger.error(f"Failed to create invoice: {e}")
            return {
                "success": False,
                "error": f"Failed to create invoice: {str(e)}"
            }


# Initialize services
telegram_bot_service = TelegramBotService()
telegram_payment_service = TelegramPaymentService()