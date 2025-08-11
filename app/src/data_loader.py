import os
import pathlib
import tempfile
import requests
import pandas as pd

# Lokal standard-path (används också för caching på Heroku)
LOCAL_PATH = pathlib.Path("data/cleaned_data.csv")

# Hämta URL från Heroku config var (eller .env lokalt)
CLEAN_DATA_URL = os.getenv("CLEAN_DATA_URL", "").strip()

def _download_to(path: pathlib.Path) -> None:
    if not CLEAN_DATA_URL:
        raise RuntimeError("CLEAN_DATA_URL is not set. Configure it in Heroku Config Vars.")
    path.parent.mkdir(parents=True, exist_ok=True)
    # GitHub Releases accepterar vanlig GET (följ redirect). Streama till fil.
    with requests.get(CLEAN_DATA_URL, stream=True, timeout=60) as r:
        r.raise_for_status()
        with open(path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

def ensure_local_copy() -> pathlib.Path:
    """
    Säkerställ att vi har en lokal kopia (cache). På Heroku
    lever /app-filsystemet under dynons livstid, så detta spar
    nedladdningar tills dynon startas om.
    """
    try:
        if LOCAL_PATH.exists() and LOCAL_PATH.stat().st_size > 0:
            return LOCAL_PATH
        _download_to(LOCAL_PATH)
        return LOCAL_PATH
    except Exception:
        # Sista utvägen: skriv till ett temporärt ställe om /app är låst
        tmp_path = pathlib.Path(tempfile.gettempdir()) / "cleaned_data.csv"
        if not tmp_path.exists() or tmp_path.stat().st_size == 0:
            _download_to(tmp_path)
        return tmp_path

def load_clean_data(encoding: str = "latin1") -> pd.DataFrame:
    """
    Ladda som pandas DataFrame. Vi använder latin1 eftersom dina tidigare fel
    visade att UTF-8 inte fungerar för filen.
    """
    csv_path = ensure_local_copy()
    return pd.read_csv(csv_path, encoding=encoding)