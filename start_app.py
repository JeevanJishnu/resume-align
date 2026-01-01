
import subprocess
import time
import socket
import os
import sys
import webbrowser

def get_local_ip():
    try:
        # Connect to a public DNS server to determine the best local IP (doesn't actually send data)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

def main():
    print("="*60)
    print("      [+] ResumeAlign: AI CV Reformatter - LAN LAUNCHER")
    print("="*60)
    
    # 1. Start Backend
    print("\n[1/3] Starting Backend API...")
    # We use python executable to ensure we use the same env
    backend_cmd = [sys.executable, "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
    backend = subprocess.Popen(backend_cmd, cwd=os.getcwd())
    
    # Wait a moment for backend
    time.sleep(2)
    
    # 2. Start Frontend
    print("[2/3] Starting Frontend (Streamlit)...")
    frontend_cmd = [sys.executable, "-m", "streamlit", "run", "dashboard.py", "--server.address", "0.0.0.0", "--server.port", "8501"]
    frontend = subprocess.Popen(frontend_cmd, cwd=os.getcwd(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # 3. Get IP and Print
    ip = get_local_ip()
    url = f"http://{ip}:8501"
    
    print("\n" + "="*60)
    print(f"   [OK] SYSTEM ONLINE")
    print("="*60)
    print(f"\n   >>> SHARE THIS LINK WITH HR TEAM:  {url}")
    print(f"      (Local Access: http://localhost:8501)")
    print("\n" + "="*60)
    
    try:
        webbrowser.open("http://localhost:8501")
        print("\nPress Ctrl+C to stop the server...")
        backend.wait()
    except KeyboardInterrupt:
        print("\n\n🛑 Shutting down...")
        frontend.terminate()
        backend.terminate()
        print("Goodbye!")

if __name__ == "__main__":
    main()
