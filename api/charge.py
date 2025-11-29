"""
API NAP THE - /api/charge
Vercel Serverless Function

Chuc nang:
- Nhan thong tin the tu frontend
- Goi API thesieure.com de nap the
- Luu thong tin the vao bot Discord (pending)
- Tra ve ket qua cho frontend

Luong hoat dong:
1. Frontend gui POST request voi: user_id, telco, amount, serial, code, voucher
2. API tao chu ky MD5 va gui len thesieure.com
3. Gui thong tin the cho bot Discord de theo doi
4. Tra ve ket qua cho frontend
"""

from http.server import BaseHTTPRequestHandler
import json
import os
import hashlib
import time
import random
import requests

# ============================================
# CAU HINH TU ENVIRONMENT VARIABLES
# ============================================
# Lay tu Vercel Environment Variables
TSR_PARTNER_ID = os.environ.get('TSR_PARTNER_ID')      # ID doi tac thesieure
TSR_PARTNER_KEY = os.environ.get('TSR_PARTNER_KEY')    # Key doi tac thesieure
TSR_API_URL = "https://thesieure.com/chargingws/v2"    # API endpoint thesieure
BOT_API_URL = os.environ.get('BOT_API_URL', '')        # URL Ngrok cua bot Discord
BOT_API_SECRET = os.environ.get('BOT_API_SECRET', '')  # Mat khau bao mat

# ============================================
# HANDLER CHINH
# ============================================
class handler(BaseHTTPRequestHandler):
    
    def do_POST(self):
        """
        Xu ly POST request nap the
        
        Body JSON can:
        - user_id: Discord user ID
        - telco: Nha mang (VIETTEL, MOBIFONE, ...)
        - amount: Menh gia the
        - serial: So seri the
        - code: Ma the cao
        - voucher: Ma voucher (optional)
        """
        try:
            # Doc body request
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            data = json.loads(body)

            # Lay thong tin tu request
            user_id = data.get('user_id')
            telco = data.get('telco')
            amount = data.get('amount')
            serial = data.get('serial')
            code = data.get('code')
            voucher = data.get('voucher')

            # Validate du lieu bat buoc
            if not all([user_id, telco, amount, serial, code]):
                return self.send_response_json(400, {
                    'success': False,
                    'message': 'Thieu thong tin bat buoc'
                })

            # Kiem tra cau hinh
            if not TSR_PARTNER_ID or not TSR_PARTNER_KEY:
                return self.send_response_json(500, {
                    'success': False,
                    'message': 'He thong chua duoc cau hinh'
                })

            # Tao request_id duy nhat
            request_id = f"{user_id}_{int(time.time())}_{random.randint(1000, 9999)}"
            
            # Tao chu ky MD5: md5(partner_key + code + serial)
            sign = hashlib.md5((TSR_PARTNER_KEY + code + serial).encode()).hexdigest()

            # Du lieu gui len thesieure
            tsr_data = {
                "telco": telco,
                "code": code,
                "serial": serial,
                "amount": amount,
                "request_id": request_id,
                "partner_id": TSR_PARTNER_ID,
                "sign": sign,
                "command": "charging"
            }

            # Goi API thesieure
            response = requests.post(TSR_API_URL, data=tsr_data, timeout=30)
            result = response.json()

            status = result.get('status')
            trans_id = result.get('trans_id', '')

            # Gui thong tin the cho bot Discord de theo doi
            if BOT_API_URL:
                try:
                    requests.post(f"{BOT_API_URL}/api/pending-card", json={
                        'secret': BOT_API_SECRET,
                        'request_id': request_id,
                        'user_id': user_id,
                        'telco': telco,
                        'declared_value': amount,
                        'code': code,
                        'serial': serial,
                        'trans_id': trans_id,
                        'voucher': voucher
                    }, timeout=10)
                except:
                    pass  # Khong can xu ly loi

            # Tra ve ket qua dua tren status
            # Status 99: Dang xu ly
            if status == 99:
                return self.send_response_json(200, {
                    'success': True,
                    'status': 99,
                    'message': 'The dang duoc xu ly',
                    'request_id': request_id,
                    'trans_id': trans_id
                })
            # Status 1: Thanh cong dung menh gia
            elif status == 1:
                received_amount = result.get('amount', int(amount * 0.7))
                return self.send_response_json(200, {
                    'success': True,
                    'status': 1,
                    'message': 'Nap the thanh cong',
                    'request_id': request_id,
                    'amount': received_amount
                })
            # Status 2: Thanh cong sai menh gia
            elif status == 2:
                received_amount = result.get('amount', 0)
                return self.send_response_json(200, {
                    'success': True,
                    'status': 2,
                    'message': f'The dung nhung sai menh gia. Nhan: {received_amount}',
                    'request_id': request_id,
                    'amount': received_amount
                })
            # Status 3: The loi
            elif status == 3:
                return self.send_response_json(200, {
                    'success': False,
                    'status': 3,
                    'message': 'The loi hoac da su dung'
                })
            # Status 4: Bao tri
            elif status == 4:
                return self.send_response_json(200, {
                    'success': False,
                    'status': 4,
                    'message': 'He thong dang bao tri'
                })
            # Status khac
            else:
                return self.send_response_json(200, {
                    'success': False,
                    'status': status,
                    'message': result.get('message', 'Co loi xay ra')
                })

        except requests.exceptions.Timeout:
            return self.send_response_json(500, {
                'success': False,
                'message': 'Ket noi toi he thong nap the bi timeout'
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
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def send_response_json(self, status_code, data):
        """Helper function gui JSON response"""
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
