"""
API TIM USER - /api/search-user
Vercel Serverless Function

Chuc nang:
- Nhan username tu frontend
- Goi API bot Discord de tim user trong server
- Tra ve danh sach user tim duoc

Luong hoat dong:
1. Frontend gui GET request voi ?username=xxx
2. API goi bot Discord /api/search-user
3. Bot Discord tim trong cac server va tra ve ket qua
4. API tra ve danh sach user cho frontend
"""

from http.server import BaseHTTPRequestHandler
import json
import os
import requests
from urllib.parse import urlparse, parse_qs

# ============================================
# CAU HINH TU ENVIRONMENT VARIABLES
# ============================================
BOT_API_URL = os.environ.get('BOT_API_URL', '')        # URL Ngrok cua bot Discord
BOT_API_SECRET = os.environ.get('BOT_API_SECRET', '')  # Mat khau bao mat

# ============================================
# HANDLER CHINH
# ============================================
class handler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        """
        Xu ly GET request tim user
        
        Query params:
        - username: Ten Discord can tim (username hoac display name)
        
        Response:
        - success: true/false
        - users: Danh sach user tim duoc [{id, username, display_name, avatar}]
        - message: Thong bao loi (neu co)
        """
        try:
            # Parse query params
            parsed = urlparse(self.path)
            params = parse_qs(parsed.query)
            
            username = params.get('username', [''])[0]
            
            # Validate
            if not username:
                return self.send_response_json(400, {
                    'success': False,
                    'message': 'Vui long nhap username'
                })

            # Kiem tra cau hinh
            if not BOT_API_URL:
                return self.send_response_json(500, {
                    'success': False,
                    'message': 'He thong chua duoc cau hinh'
                })

            # Goi API bot Discord de tim user
            response = requests.get(
                f"{BOT_API_URL}/api/search-user",
                params={'username': username, 'secret': BOT_API_SECRET},
                timeout=10
            )
            
            data = response.json()
            return self.send_response_json(200, data)

        except requests.exceptions.Timeout:
            return self.send_response_json(500, {
                'success': False,
                'message': 'Timeout khi ket noi toi bot'
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
