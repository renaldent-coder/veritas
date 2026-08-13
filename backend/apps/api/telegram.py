import requests
import logging
from django.conf import settings

logger = logging.getLogger(__name__)


def send_telegram_alert(case):
    """
    Send a rich alert to the internal Telegram group when a new case is submitted.
    """
    try:
        token = settings.TELEGRAM_BOT_TOKEN
        chat_id = settings.TELEGRAM_CHAT_ID
        
        # Build the message
        message = f"""
🚨 *NEW CASE ALERT* 🚨

📋 *Case:* #{case.case_number}
👤 *Client:* {case.client.get_full_name()}
💰 *Loss Amount:* ${case.loss_amount:,.2f} {case.currency}
📂 *Scam Type:* {case.get_scam_category_display()}
📅 *Submitted:* {case.submitted_at.strftime('%Y-%m-%d %H:%M UTC')}
🔍 *Status:* {case.get_status_display()}

📝 *Narrative Preview:*
{case.narrative[:200]}...

---
👨‍💼 *Assigned Agent:* None assigned yet
📱 *Client Telegram:* {case.client.telegram_handle or 'Not provided'}

🔗 *View in Admin:* {settings.ADMIN_BASE_URL}/admin/cases/case/{case.id}/change/
"""
        
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        payload = {
            'chat_id': chat_id,
            'text': message,
            'parse_mode': 'Markdown',
            'disable_web_page_preview': True,
        }
        
        response = requests.post(url, json=payload, timeout=10)
        
        if response.status_code == 200:
            logger.info(f"Telegram alert sent for case #{case.case_number}")
        else:
            logger.error(f"Failed to send Telegram alert: {response.text}")
            
    except Exception as e:
        logger.error(f"Telegram alert error: {str(e)}")