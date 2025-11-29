# Napthe Web - Trang nap the cho Discord Bot

## Huong dan deploy len Vercel

### Buoc 1: Tao tai khoan Vercel
1. Truy cap https://vercel.com
2. Dang ky tai khoan bang GitHub

### Buoc 2: Deploy project
1. Push thu muc `napthe-web` len GitHub repo rieng
2. Tren Vercel, click "Add New Project"
3. Import repo tu GitHub
4. Vercel se tu dong detect va deploy

### Buoc 3: Cau hinh Environment Variables
Trong Vercel Dashboard > Project > Settings > Environment Variables, them:

| Key | Value | Mo ta |
|-----|-------|-------|
| `TSR_PARTNER_ID` | ID doi tac thesieure | Lay tu thesieure.com |
| `TSR_PARTNER_KEY` | Key doi tac thesieure | Lay tu thesieure.com |
| `BOT_API_URL` | URL Ngrok cua bot | VD: https://xxx.ngrok-free.dev |
| `BOT_API_SECRET` | Mat khau bao mat | Tu dat, phai giong voi bot |

### Buoc 4: Cau hinh Discord Bot
Trong file `.env` cua bot Discord, them:

```
BOT_API_SECRET=mat_khau_giong_vercel
NAPTHE_WEB_URL=https://ten-project.vercel.app
```

### Buoc 5: Cau hinh callback thesieure
1. Dang nhap thesieure.com
2. Vao phan API/Doi tac
3. Dat Callback URL: `https://ten-project.vercel.app/api/callback`

## Cau truc thu muc

```
napthe-web/
├── index.html          # Trang chinh
├── style.css           # CSS
├── script.js           # JavaScript
├── vercel.json         # Cau hinh Vercel
├── requirements.txt    # Python dependencies
└── api/
    ├── charge.py       # API nap the
    ├── callback.py     # Nhan callback tu thesieure
    └── search-user.py  # Tim user Discord
```

## Cach hoat dong

1. User dung lenh `/napthe` trong Discord
2. Bot gui link den trang nap the kem user ID
3. User nhap thong tin the tren trang web
4. Web goi API thesieure de nap the
5. Khi the duoc xu ly, thesieure goi callback den Vercel
6. Vercel goi API bot de cong tien cho user

## Luu y

- Callback URL phai la HTTPS
- Bot API URL (Ngrok) can luon chay
- Mat khau BOT_API_SECRET phai giong nhau giua Vercel va Bot
