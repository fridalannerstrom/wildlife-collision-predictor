import os
import pathlib
import requests

DEFAULT_LOCAL = "data/cleaned_data.csv" 

def ensure_local_clean_data(local_path: str = DEFAULT_LOCAL) -> str:
    """
    Returnerar sökvägen till en lokal CSV med cleaned data.
    Om filen saknas laddas den ner från CLEAN_DATA_URL (env var).
    """
    p = pathlib.Path(local_path)
    if p.exists():
        return str(p)

    url = os.getenv("CLEAN_DATA_URL")
    if not url:
        raise FileNotFoundError(
            f"{local_path} saknas och CLEAN_DATA_URL är inte satt."
        )

    p.parent.mkdir(parents=True, exist_ok=True)

    # Streama ned filen (kan vara .csv eller .csv.gz)
    r = requests.get(url, stream=True, timeout=120)
    r.raise_for_status()
    tmp = p.with_suffix(p.suffix + ".download")
    with open(tmp, "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
    tmp.replace(p)  # atomiskt byte av filnamn
    return str(p)