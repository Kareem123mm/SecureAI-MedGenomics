#!/usr/bin/env python3
"""
SecureAI-MedGenomics Platform Launcher
Simple, reliable startup script that works every time.
"""

import subprocess
import sys
import os
import time
import webbrowser
from pathlib import Path

def print_banner():
    print("\n" + "="*60)
    print("  🧬 SecureAI-MedGenomics Platform")
    print("  Integrated AI + Security System")
    print("="*60 + "\n")

def check_python():
    print("✓ Python version:", sys.version.split()[0])
    print("✓ Python path:", sys.executable)
    return True

def check_dependencies():
    print("\n[*] Checking dependencies...")
    required = ['fastapi', 'uvicorn', 'torch', 'sklearn', 'xgboost', 'Bio']
    missing = []
    
    for module in required:
        try:
            __import__(module)
            print(f"  ✓ {module}")
        except ImportError:
            print(f"  ✗ {module} - MISSING")
            missing.append(module)
    
    if missing:
        print("\n[!] Missing dependencies. Install with:")
        print("    pip install -r backend/requirements_integrated.txt")
        return False
    
    print("  ✓ All dependencies installed")
    return True

def kill_existing_backend():
    print("\n[*] Checking for existing backend processes...")
    try:
        if sys.platform == "win32":
            # Windows: Kill Python processes on port 8000
            subprocess.run(
                ['powershell', '-Command', 
                 'Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue | Stop-Process -Id {$_.OwningProcess} -Force -ErrorAction SilentlyContinue'],
                capture_output=True,
                timeout=5
            )
        else:
            # Linux/Mac: Kill process on port 8000
            subprocess.run(['fuser', '-k', '8000/tcp'], capture_output=True, timeout=5)
        
        print("  ✓ Cleared port 8000")
        time.sleep(2)
    except Exception as e:
        print(f"  ⚠ Could not clear port: {e}")

def start_backend():
    print("\n[*] Starting backend server...")
    
    # Change to backend directory
    backend_dir = Path(__file__).parent / "backend"
    os.chdir(backend_dir)
    
    # Use Windows Python explicitly
    python_exe = r"C:\Users\YAHOO COMPUTER\AppData\Local\Programs\Python\Python311\python.exe"
    if not os.path.exists(python_exe):
        python_exe = sys.executable
    
    # Start backend process
    if sys.platform == "win32":
        # Windows: Start in new window
        process = subprocess.Popen(
            [python_exe, "integrated_main.py"],
            creationflags=subprocess.CREATE_NEW_CONSOLE
        )
    else:
        # Linux/Mac: Start in background
        process = subprocess.Popen(
            [python_exe, "integrated_main.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
    
    print("  ✓ Backend starting (PID:", process.pid, ")")
    return process

def wait_for_backend(timeout=30):
    print("\n[*] Waiting for backend to be ready...")
    
    import socket
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex(('localhost', 8000))
            sock.close()
            
            if result == 0:
                print("  ✓ Backend is ready!")
                return True
        except:
            pass
        
        time.sleep(1)
    
    print("  ✗ Backend did not start within", timeout, "seconds")
    return False

def test_health():
    print("\n[*] Testing health endpoint...")
    
    try:
        import urllib.request
        import json
        
        with urllib.request.urlopen('http://localhost:8000/api/health', timeout=5) as response:
            data = json.loads(response.read())
            
            print("  ✓ Status:", data['status'])
            print("  ✓ Models loaded:", data['ai_engine']['models_loaded'])
            print("  ✓ Security score:", data['security_pipeline']['security_score'])
            print("  ✓ Database:", data['database'])
            return True
    except Exception as e:
        print(f"  ✗ Health check failed: {e}")
        return False

def open_browser():
    print("\n[*] Opening browser...")
    
    urls = [
        ("API Documentation", "http://localhost:8000/docs"),
        ("Health Check", "http://localhost:8000/api/health"),
    ]
    
    for name, url in urls:
        print(f"  → {name}: {url}")
    
    try:
        webbrowser.open("http://localhost:8000/docs")
        print("  ✓ Browser opened")
    except:
        print("  ⚠ Could not open browser automatically")

def print_info():
    print("\n" + "="*60)
    print("  🎉 SYSTEM IS RUNNING!")
    print("="*60)
    print("\n  Backend:    http://localhost:8000")
    print("  API Docs:   http://localhost:8000/docs")
    print("  Health:     http://localhost:8000/api/health")
    print("\n" + "="*60)
    print("\n  Press Ctrl+C to stop the server\n")

def main():
    print_banner()
    
    # Step 1: Check Python
    if not check_python():
        sys.exit(1)
    
    # Step 2: Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Step 3: Kill existing backend
    kill_existing_backend()
    
    # Step 4: Start backend
    process = start_backend()
    
    # Step 5: Wait for backend
    if not wait_for_backend():
        print("\n[!] Backend failed to start. Check the backend window for errors.")
        sys.exit(1)
    
    # Step 6: Test health
    if not test_health():
        print("\n[!] Backend started but health check failed.")
    
    # Step 7: Open browser
    open_browser()
    
    # Step 8: Print info
    print_info()
    
    # Step 9: Wait for user to stop
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n[*] Stopping server...")
        process.terminate()
        process.wait()
        print("  ✓ Server stopped")
        print("\n[*] Goodbye!\n")

if __name__ == "__main__":
    main()
