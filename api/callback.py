"""
API CALLBACK - /api/callback
Vercel Serverless Function

Chuc nang:
- Nhan callback tu thesieure.com khi the duoc xu ly xong
- Xac thuc chu ky callback
- Gui thong tin cho bot Discord de cong tien

Luong hoat dong:
1. thesieure.com goi callback (GET hoac POST) khi the xu ly xong
2. API xac thuc chu ky callback_sign
3. Gui thong tin cho bot Discord qua /api/card-callback
4. Bot Discord cong tien cho user
"""

from http.server import BaseHTTPRequestHandler
import json
import os
import hashlib
import requests
from urllib.parse import parse_qs

# ============================================
# CAU HINH TU ENVIRONMENT VARIABLES
# ============================================
BOT_API_URL = os.environ.get('BOT_API_URL', '')        # URL Ngrok cua bot Discord
BOT_API_SECRET = os.environ.get('BOT_API_SECRET', '')  # Mat khau bao mat
TSR_PARTNER_KEY = os.environ.get('TSR_PARTNER_KEY', '') # Key de verify callback

# ============================================
# HANDLER CHINH
# ============================================
class handler(BaseHTTPRequestHandler):
    
    def do_POST(self):
        """
        Xu ly POST callback tu thesieure
        
        Data callback:
        - status: 1=thanh cong, 2=sai menh gia, 3=loi
        - request_id: Ma giao dich
        - declared_value: Menh gia khai bao
        - value: Menh gia thuc
        - amount: So tien nhan duoc
        - code: Ma the
        - serial: So seri
        - telco: Nha mang
        - trans_id: Ma giao dich thesieure
        - callback_sign: Chu ky xac thuc
        """
        try:
            # Doc body request
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            
            # Parse du lieu tuy theo Content-Type
            content_type = self.headers.get('Content-Type', '')
            
            if 'application/json' in content_type:
                data = json.loads(body)
            else:
                # Parse form data
                data = {}
                parsed = parse_qs(body.decode())
                for key, value in parsed.items():
                    data[key] = value[0] if len(value) == 1 else value

            # Lay thong tin tu callback
            status = int(data.get('status', 0))
            request_id = data.get('request_id', '')
            declared_value = int(data.get('declared_value', 0))
            value = data.get('value')
            amount = int(data.get('amount', 0))
            code = data.get('code', '')
            serial = data.get('serial', '')
            telco = data.get('telco', '')
            trans_id = data.get('trans_id', '')
            callback_sign = data.get('callback_sign', '')

            # Xac thuc chu ky: md5(partner_key + code + serial)
            expected_sign = hashlib.md5((TSR_PARTNER_KEY + code + serial).encode()).hexdigest()
            if callback_sign != expected_sign:
                return self.send_response_json(400, {'error': 'Invalid signature'})

            # Gui thong tin cho bot Discord
            if BOT_API_URL:
                try:
                    bot_response = requests.post(f"{BOT_API_URL}/api/card-callback", json={
                        'secret': BOT_API_SECRET,
                        'status': status,
                        'request_id': request_id,
                        'declared_value': declared_value,
                        'value': value,
                        'amount': amount,
                        'code': code,
                        'serial': serial,
                        'telco': telco,
                        'trans_id': trans_id
                    }, timeout=10)
                except Exception as e:
                    print(f"Error calling bot API: {e}")

            return self.send_response_json(200, {'success': True})

        except Exception as e:
            return self.send_response_json(500, {'error': str(e)})

    def do_GET(self):
        """
        Xu ly GET callback tu thesieure
        Tham so nam trong URL query string
        """
        try:
            from urllib.parse import urlparse, parse_qs
            parsed = urlparse(self.path)
            params = parse_qs(parsed.query)
            
            # Chuyen params thanh dict
            data = {}
            for key, value in params.items():
                data[key] = value[0] if len(value) == 1 else value

            # Lay thong tin tu callback
            status = int(data.get('status', 0))
            request_id = data.get('request_id', '')
            declared_value = int(data.get('declared_value', 0))
            value = data.get('value')
            amount = int(data.get('amount', 0))
            code = data.get('code', '')
            serial = data.get('serial', '')
            telco = data.get('telco', '')
            trans_id = data.get('trans_id', '')
            callback_sign = data.get('callback_sign', '')

            # Xac thuc chu ky
            expected_sign = hashlib.md5((TSR_PARTNER_KEY + code + serial).encode()).hexdigest()
            if callback_sign != expected_sign:
                return self.send_response_json(400, {'error': 'Invalid signature'})

            # Gui thong tin cho bot Discord
            if BOT_API_URL:
                try:
                    requests.post(f"{BOT_API_URL}/api/card-callback", json={
                        'secret': BOT_API_SECRET,
                        'status': status,
                        'request_id': request_id,
                        'declared_value': declared_value,
                        'value': value,
                        'amount': amount,
                        'code': code,
                        'serial': serial,
                        'telco': telco,
                        'trans_id': trans_id
                    }, timeout=10)
                except Exception as e:
                    print(f"Error calling bot API: {e}")

            return self.send_response_json(200, {'success': True})

        except Exception as e:
            return self.send_response_json(500, {'error': str(e)})

    def send_response_json(self, status_code, data):
        """Helper function gui JSON response"""
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
