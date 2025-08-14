import streamlit as st
from pathlib import Path
import importlib

# -------------------------------
# Streamlit App Configuration
# -------------------------------

st.set_page_config(
    page_title="Wildlife Collision Predictor",
    layout="wide",
)

st.title("Wildlife Collision Predictor")
st.write("""
Welcome!
Use the sidebar to navigate between the different sections
of the dashboard.
""")

# -------------------------------
# Load all pages from app_pages/
# -------------------------------

# Get all .py files from the app_pages folder, excluding __init__.py or __files
pages_dir = Path(__file__).parent / "app_pages"
page_files = sorted(
    p for p in pages_dir.glob("*.py") if not p.name.startswith("__")
)

# Convert filenames to clean page names
page_names = [
    p.name.split("_", 1)[1].replace(".py", "").replace("_", " ").title()
    for p in page_files
]

# Sidebar page selector
selected = st.sidebar.selectbox("Go to section", page_names)

# Load selected module
selected_file = next(
    p
    for p in page_files
    if selected.lower().replace(" ", "_") in p.name.lower()
)
module_name = f"app_pages.{selected_file.stem}"
page_module = importlib.import_module(module_name)

# Run the selected page's `run()` function
page_module.run()
