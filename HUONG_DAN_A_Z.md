# HUONG DAN DEPLOY NAPTHE WEB - TU A DEN Z

## MUC LUC
1. [Gioi thieu](#1-gioi-thieu)
2. [Yeu cau](#2-yeu-cau)
3. [Tao tai khoan Vercel](#3-tao-tai-khoan-vercel)
4. [Tao GitHub Repository](#4-tao-github-repository)
5. [Upload code len GitHub](#5-upload-code-len-github)
6. [Deploy len Vercel](#6-deploy-len-vercel)
7. [Cau hinh Environment Variables](#7-cau-hinh-environment-variables)
8. [Cau hinh Discord Bot](#8-cau-hinh-discord-bot)
9. [Cau hinh thesieure.com](#9-cau-hinh-thesieure-com)
10. [Test thu](#10-test-thu)
11. [Xu ly loi thuong gap](#11-xu-ly-loi-thuong-gap)

---

## 1. GIOI THIEU

### He thong gom 3 phan:
```
+------------------+     +------------------+     +------------------+
|  Discord Bot     |     |  Vercel Website  |     |  thesieure.com   |
|  (Replit/VPS)    |<--->|  (napthe-web)    |<--->|  (API nap the)   |
+------------------+     +------------------+     +------------------+
```

### Luong hoat dong:
1. User dung `/napthe` trong Discord
2. Bot gui link website kem user ID
3. User vao web, nhap thong tin the
4. Website goi API thesieure.com
5. thesieure xu ly the va goi callback
6. Website gui ket qua cho bot
7. Bot cong tien cho user

---

## 2. YEU CAU

### Tai khoan can co:
- [x] Tai khoan GitHub (mien phi)
- [x] Tai khoan Vercel (mien phi)
- [x] Tai khoan thesieure.com (co san)

### Thong tin can chuan bi:
- [x] TSR_PARTNER_ID (lay tu thesieure.com)
- [x] TSR_PARTNER_KEY (lay tu thesieure.com)
- [x] URL Ngrok cua bot Discord

---

## 3. TAO TAI KHOAN VERCEL

### Buoc 3.1: Truy cap Vercel
1. Mo trinh duyet, vao: https://vercel.com
2. Click nut "Sign Up" o goc phai tren

### Buoc 3.2: Dang ky bang GitHub
1. Chon "Continue with GitHub"
2. Dang nhap tai khoan GitHub cua ban
3. Cho phep Vercel truy cap GitHub

### Buoc 3.3: Hoan thanh dang ky
1. Chon "Hobby" (mien phi)
2. Nhap ten cua ban
3. Click "Continue"

---

## 4. TAO GITHUB REPOSITORY

### Buoc 4.1: Tao repo moi
1. Vao https://github.com/new
2. Dien thong tin:
   - Repository name: `napthe-web`
   - Description: `Website nap the cho Discord bot`
   - Chon "Private" (de bao mat)
3. Click "Create repository"

### Buoc 4.2: Luu lai URL repo
- URL se co dang: `https://github.com/USERNAME/napthe-web`
- Luu lai de dung o buoc sau

---

## 5. UPLOAD CODE LEN GITHUB

### Cach 1: Su dung GitHub Desktop (De nhat)

#### Buoc 5.1: Tai GitHub Desktop
1. Vao https://desktop.github.com
2. Tai va cai dat

#### Buoc 5.2: Clone repo
1. Mo GitHub Desktop
2. File > Clone Repository
3. Dan URL repo vua tao
4. Chon thu muc luu tren may

#### Buoc 5.3: Copy file vao
1. Mo thu muc vua clone
2. Copy tat ca file trong `napthe-web` vao:
   - index.html
   - style.css
   - script.js
   - vercel.json
   - requirements.txt
   - thu muc api/ (ca 3 file .py)

#### Buoc 5.4: Push len GitHub
1. Quay lai GitHub Desktop
2. O cot trai, thay danh sach file moi
3. Nhap "Summary": `Initial commit`
4. Click "Commit to main"
5. Click "Push origin"

### Cach 2: Su dung Git command line

```bash
# Clone repo
git clone https://github.com/USERNAME/napthe-web.git
cd napthe-web

# Copy file (tu thu muc napthe-web trong Replit)
# ... copy cac file ...

# Push len GitHub
git add .
git commit -m "Initial commit"
git push origin main
```

---

## 6. DEPLOY LEN VERCEL

### Buoc 6.1: Vao Vercel Dashboard
1. Truy cap https://vercel.com/dashboard
2. Dang nhap neu chua

### Buoc 6.2: Tao project moi
1. Click "Add New..." > "Project"
2. Tim repo `napthe-web` trong danh sach
3. Click "Import"

### Buoc 6.3: Cau hinh project
1. Project Name: giu nguyen hoac doi ten
2. Framework Preset: chon "Other"
3. Root Directory: de trong
4. **CHUA CLICK DEPLOY**

### Buoc 6.4: Them Environment Variables
1. Mo phan "Environment Variables"
2. Them tung bien (xem buoc 7)
3. Sau khi them xong, click "Deploy"

### Buoc 6.5: Cho deploy xong
1. Vercel se build va deploy
2. Mat khoang 1-2 phut
3. Khi xong, ban se thay URL: `https://ten-project.vercel.app`

---

## 7. CAU HINH ENVIRONMENT VARIABLES

### Tren Vercel:
Vao Project > Settings > Environment Variables

| Key | Value | Mo ta |
|-----|-------|-------|
| `TSR_PARTNER_ID` | `1234567890` | ID doi tac tu thesieure.com |
| `TSR_PARTNER_KEY` | `abcdef123456` | Key doi tac tu thesieure.com |
| `BOT_API_URL` | `https://xxx.ngrok-free.dev` | URL Ngrok cua bot Discord |
| `BOT_API_SECRET` | `matkhaubaomat123` | Mat khau tu dat (bat ky) |

### Luu y:
- Moi bien can them cho ca 3 moi truong: Production, Preview, Development
- Hoac chon "All" khi them

---

## 8. CAU HINH DISCORD BOT

### Buoc 8.1: Mo file .env cua bot
Tim file `.env` trong thu muc bot Discord

### Buoc 8.2: Them cac bien moi
```env
# Them vao cuoi file .env
BOT_API_SECRET=matkhaubaomat123
NAPTHE_WEB_URL=https://ten-project.vercel.app
```

### Luu y:
- `BOT_API_SECRET` phai GIONG voi tren Vercel
- `NAPTHE_WEB_URL` la URL website tren Vercel (khong co dau / o cuoi)

### Buoc 8.3: Restart bot
- Luu file va restart bot de nhan cau hinh moi

---

## 9. CAU HINH THESIEURE.COM

### Buoc 9.1: Dang nhap thesieure.com
1. Vao https://thesieure.com
2. Dang nhap tai khoan doi tac

### Buoc 9.2: Vao phan API
1. Tim menu "API" hoac "Doi tac"
2. Vao phan cau hinh callback

### Buoc 9.3: Dat Callback URL
1. Nhap URL callback moi:
   ```
   https://ten-project.vercel.app/api/callback
   ```
2. Luu lai

### Luu y:
- URL phai la HTTPS
- Thay `ten-project` bang ten project Vercel cua ban

---

## 10. TEST THU

### Buoc 10.1: Test lenh /napthe
1. Vao Discord server co bot
2. Dung lenh `/napthe`
3. Bot se gui link website

### Buoc 10.2: Truy cap website
1. Click vao link
2. Kiem tra User ID hien thi dung

### Buoc 10.3: Test form nhap username
1. Click "Doi" de doi user
2. Nhap username Discord
3. Kiem tra ket qua tim kiem

### Buoc 10.4: Test nap the (voi the that)
1. Chon nha mang va menh gia
2. Nhap seri va ma the
3. Click "Nap The"
4. Kiem tra ket qua

---

## 11. XU LY LOI THUONG GAP

### Loi 1: "He thong chua duoc cau hinh"
**Nguyen nhan:** Thieu Environment Variables tren Vercel
**Cach sua:** Kiem tra lai cac bien TSR_PARTNER_ID, TSR_PARTNER_KEY

### Loi 2: "Timeout khi ket noi toi bot"
**Nguyen nhan:** Bot Discord chua chay hoac Ngrok bi tat
**Cach sua:** 
- Kiem tra bot dang chay
- Kiem tra Ngrok dang hoat dong
- Cap nhat BOT_API_URL moi neu Ngrok doi URL

### Loi 3: "Khong tim thay user nao"
**Nguyen nhan:** Username sai hoac user khong trong server
**Cach sua:**
- Kiem tra username chinh xac
- Dam bao user dang o trong server co bot

### Loi 4: The nap xong nhung khong cong tien
**Nguyen nhan:** Callback URL sai
**Cach sua:**
- Kiem tra Callback URL tren thesieure.com
- Dam bao URL dung: `https://ten-project.vercel.app/api/callback`

### Loi 5: Loi CORS
**Nguyen nhan:** Cau hinh Vercel sai
**Cach sua:** Kiem tra file vercel.json co dung khong

---

## CAU TRUC FILE

```
napthe-web/
├── index.html          # Trang chinh (giao dien nguoi dung)
├── style.css           # CSS (giao dien dep)
├── script.js           # JavaScript (xu ly logic)
├── vercel.json         # Cau hinh Vercel (routes)
├── requirements.txt    # Python dependencies
├── README.md           # Huong dan ngan
├── HUONG_DAN_A_Z.md    # Huong dan chi tiet (file nay)
└── api/                # Thu muc API
    ├── charge.py       # API nap the
    ├── callback.py     # Nhan callback tu thesieure
    └── search-user.py  # Tim user Discord
```

---

## LIEN HE HO TRO

- **thesieure.com:** Zalo 0823.22.99.88
- **Vercel:** https://vercel.com/docs
- **GitHub:** https://docs.github.com

---

## CHANGELOG

- **v1.0** - Phien ban dau tien
  - Website nap the co ban
  - Tim user theo username
  - Luu user ID vao localStorage
  - Lich su nap the local
