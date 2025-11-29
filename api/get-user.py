"""
API LAY THONG TIN USER - /api/get-user
Vercel Serverless Function

Chuc nang:
- Nhan UID tu frontend
- Goi API bot Discord de lay thong tin user
- Tra ve thong tin user (username, avatar, display_name)
"""

from http.server import BaseHTTPRequestHandler
import json
import os
import requests
from urllib.parse import urlparse, parse_qs
import logging

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [NAPTHE-GETUSER] %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

BOT_API_URL = os.environ.get('BOT_API_URL', '')
BOT_API_SECRET = os.environ.get('BOT_API_SECRET', '')

class handler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        """
        Xu ly GET request lay thong tin user
        
        Query params:
        - uid: Discord User ID
        
        Response:
        - success: true/false
        - user: {id, username, display_name, avatar}
        - message: Thong bao loi (neu co)
        """
        try:
            parsed = urlparse(self.path)
            params = parse_qs(parsed.query)
            
            uid = params.get('uid', [''])[0]
            
            if not uid:
                logger.warning("Empty UID request")
                return self.send_response_json(400, {
                    'success': False,
                    'message': 'UID required'
                })
            
            logger.info(f"Get user request: uid={uid}")

            if not BOT_API_URL:
                return self.send_response_json(500, {
                    'success': False,
                    'message': 'He thong chua duoc cau hinh'
                })

            logger.info(f"Querying bot API for uid: {uid}")
            response = requests.get(
                f"{BOT_API_URL}/api/get-user",
                params={'uid': uid, 'secret': BOT_API_SECRET},
                timeout=10
            )
            
            logger.info(f"Bot API response status: {response.status_code}")
            
            try:
                data = response.json()
                if data.get('success'):
                    logger.info(f"Found user: {data.get('user', {}).get('username')}")
                else:
                    logger.info(f"User not found for uid: {uid}")
            except ValueError as e:
                logger.error(f"Bot API returned non-JSON: {response.status_code} - {response.text[:200]}")
                return self.send_response_json(500, {
                    'success': False,
                    'message': f'Bot API error: {response.status_code}'
                })
            
            return self.send_response_json(200, data)

        except requests.exceptions.Timeout:
            return self.send_response_json(500, {
                'success': False,
                'message': 'Timeout khi ket noi toi bot'
            })
        except requests.exceptions.ConnectionError:
            return self.send_response_json(500, {
                'success': False,
                'message': 'Khong the ket noi toi bot'
            })
        except Exception as e:
            return self.send_response_json(500, {
                'success': False,
                'message': f'Loi: {str(e)}'
            })

    def do_OPTIONS(self):
        """Xu ly CORS preflight request"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def send_response_json(self, status_code, data):
        """Helper function gui JSON response"""
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
