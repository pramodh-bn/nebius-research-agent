"""Launch the Research Courtroom full stack (FastAPI backend + React frontend).

Usage:
  python run_app.py
"""
import os
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FRONTEND = ROOT / "frontend"
TOOLS = ROOT / ".tools"


def main():
    print("=" * 60)
    print("⚖️  Starting Research Courtroom Stack")
    print("=" * 60)

    env = os.environ.copy()
    if TOOLS.exists():
        env["PATH"] = str(TOOLS) + os.pathsep + env.get("PATH", "")

    # 1. Start FastAPI backend
    print("Starting FastAPI backend on http://127.0.0.1:8000...")
    backend = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "courtroom.api:app", "--host", "0.0.0.0", "--port", "8000"],
        cwd=str(ROOT / "src"),
        env=env,
    )

    time.sleep(1.5)

    # 2. Start Vite frontend
    bun_exe = TOOLS / "bun.exe"
    runner = str(bun_exe) if bun_exe.exists() else "bun"
    print(f"Starting React frontend on http://localhost:3000 using {runner}...")
    frontend = subprocess.Popen(
        [runner, "run", "dev", "--port", "3000"],
        cwd=str(FRONTEND),
        env=env,
    )

    print("\n✅ Research Courtroom is running!")
    print("   👉 React Web UI: http://localhost:3000")
    print("   👉 API Docs:     http://127.0.0.1:8000/docs")
    print("   👉 Streamlit UI: streamlit run app.py (also still available)")
    print("\nPress Ctrl+C to stop both servers.\n")

    try:
        backend.wait()
    except KeyboardInterrupt:
        print("\nStopping servers...")
        backend.terminate()
        frontend.terminate()
        backend.wait()
        frontend.wait()
        print("Done.")


if __name__ == "__main__":
    main()
