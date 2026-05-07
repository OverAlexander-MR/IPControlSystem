# Inverted Pendulum Control System (Cloudflare Pages + Tunnel)

This project consists of a high-performance frontend deployed on **Cloudflare Pages** and a local **Python (FastAPI) backend** connected via **Cloudflare Tunnel**.

## 📁 Project Structure
- `frontend/`: Static files (HTML/JS/CSS). Deploy this to Cloudflare Pages.
- `backend/`: FastAPI server. Runs locally on your machine.
- `cloudflared/`: Configuration for the secure tunnel.

---

## 🚀 Local Setup (Testing)

### 1. Backend
```bash
cd backend
source ../.env/bin/activate
python server.py
```

### 2. Frontend
```bash
cd frontend
python3 -m http.server 3000
```
Visit `http://localhost:3000`.

---

## 🌐 Production Setup

### 1. Cloudflare Pages
1. Push the project to GitHub.
2. In Cloudflare Pages, set the **Build output directory** to `frontend`.

### 2. Cloudflare Tunnel
1. Install `cloudflared` (Arch: `sudo pacman -S cloudflared`).
2. Authenticate: `cloudflared tunnel login`.
3. Create: `cloudflared tunnel create pendulum-tunnel`.
4. Configure `cloudflared/config.yml` with your Tunnel ID.
5. Route: `cloudflared tunnel route dns pendulum-tunnel api.ipcontrolsystem.pages.dev`.
6. Start: `sudo systemctl enable --now cloudflared` (using the provided service file).

---

## 📖 Full Documentation
See [INSTRUCTIONS.txt](INSTRUCTIONS.txt) for detailed technical info and troubleshooting.
