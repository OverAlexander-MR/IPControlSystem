# Inverted Pendulum Control System (Cloudflare Pages + Tunnel)

This project consists of a high-performance frontend deployed on **Cloudflare Pages** and a local **Python (FastAPI) backend** connected via **Cloudflare Tunnel**.

## Architecture
`Browser (Frontend)` -> `Cloudflare Edge` -> `Cloudflare Tunnel` -> `Local Machine (Python Backend)`

---

## 🚀 Fedora/Linux Installation

### 1. Prerequisites
Install Python and system dependencies:
```bash
sudo dnf update -y
sudo dnf install python3 python3-pip python3-virtualenv -y
```

### 2. Backend Setup
Navigate to the `backend/` directory and run the initialization script:
```bash
cd backend
chmod +x run.sh
./run.sh
```
This will:
- Create a virtual environment (`venv`).
- Install dependencies (`fastapi`, `uvicorn`, etc.).
- Start the server on `http://localhost:8000`.

### 3. Cloudflare Tunnel (cloudflared) Setup

#### Install cloudflared:
```bash
curl -L --output cloudflared.rpm https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-x86_64.rpm
sudo dnf localinstall cloudflared.rpm -y
```

#### Authenticate:
```bash
cloudflared tunnel login
```

#### Create a Tunnel:
```bash
cloudflared tunnel create pendulum-tunnel
```
*Note the Tunnel ID generated.*

#### Configure:
Edit `cloudflared/config.yml` and replace `<YOUR_TUNNEL_ID>` with your actual Tunnel ID.

#### Map Domain:
```bash
cloudflared tunnel route dns pendulum-tunnel backend.yourdomain.com
```

---

## 🛠️ Persistent Service (systemd)

To make the tunnel run automatically on startup:

1. Copy the service file:
```bash
sudo cp cloudflared/cloudflared.service /etc/systemd/system/
```

2. Reload and enable:
```bash
sudo systemctl daemon-reload
sudo systemctl enable cloudflared
sudo systemctl start cloudflared
```

Check status:
```bash
sudo systemctl status cloudflared
```

---

## 🌐 Frontend Configuration

1. Update `app.js`:
   Replace `https://backend.yourdomain.com` with your actual tunnel domain.

2. Push to GitHub:
   Cloudflare Pages will automatically deploy your changes.

---

## 📝 Usage

- When you change the **Control Type** or **COM Port** in the web interface, the frontend sends an async POST request to your local machine.
- The local backend prints the received commands to the console.
- The **Connection Status** indicator shows if the backend is reachable.

## Security Note
The backend remains strictly on your local machine. No code is uploaded to GitHub for the backend part, and the tunnel provides a secure, encrypted bridge without opening firewall ports.
