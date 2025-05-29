import os
import streamlit.web.bootstrap

port = int(os.environ.get("PORT", 8501))

streamlit.web.bootstrap.run(
    "app.py",
    "",
    [],
    {"server.port": port, "server.enableCORS": False},
)
