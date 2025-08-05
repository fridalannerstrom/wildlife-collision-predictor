import streamlit as st
from pathlib import Path
import importlib

# Multipage app loader
st.set_page_config(page_title="Wildlife Collision Predictor", layout="wide")
st.title("🚗🦌 Wildlife Collision Predictor")
st.write("Welcome! Use the sidebar to navigate between sections.")

# Hämta alla .py-filer i app_pages/
pages_dir = Path(__file__).parent / "app_pages"
page_files = sorted(p for p in pages_dir.glob("*.py") if not p.name.startswith("__"))

# Lista alla sidor
page_names = [p.name.split("_", 1)[1].replace(".py", "").replace("_", " ") for p in page_files]
selected = st.sidebar.selectbox("📂 Go to", page_names)

# Ladda rätt sida
selected_file = next(p for p in page_files if selected.lower().replace(" ", "_") in p.name.lower())
module_name = f"app_pages.{selected_file.stem}"
page_module = importlib.import_module(module_name)
page_module.run()