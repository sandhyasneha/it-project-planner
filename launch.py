import os
import subprocess

port = os.environ.get("PORT", "8501")

subprocess.run([
    "streamlit", "run", "streamlit_ui.py",
    "--server.port", str(port),
    "--server.enableCORS", "false",
    "--server.enableXsrfProtection", "false"
])

