import os
import pandas as pd
from dotenv import load_dotenv
load_dotenv()

print("🔍 CLEAN_DATA_URL:", os.getenv("CLEAN_DATA_URL"))

DEFAULT_LOCAL_PATH = "data/cleaned_data.csv"

def load_clean_data(encoding="latin1"):
    """
    Loads the dataset from URL in CLEAN_DATA_URL if provided, otherwise from local path.
    """
    clean_data_url = os.getenv("CLEAN_DATA_URL")
    
    try:
        if clean_data_url:
            df = pd.read_csv(
                clean_data_url,
                encoding=encoding,
                # on_bad_lines="skip",  # optional
                # sep=",",              # optional
            )
        else:
            df = pd.read_csv(
                DEFAULT_LOCAL_PATH,
                encoding=encoding,
                # on_bad_lines="skip",  # optional
                # sep=",",              # optional
            )
    except pd.errors.ParserError as e:
        raise RuntimeError(
            "Kunde inte läsa CSV-filen. Kontrollera att URL:en pekar på en rå "
            "nedladdning (inte en HTML-sida) och att avgränsare/encoding stämmer."
        ) from e
    except Exception as e:
        where = "CLEAN_DATA_URL" if clean_data_url else DEFAULT_LOCAL_PATH
        raise RuntimeError(f"Misslyckades att ladda data från: {where}") from e

    if df.empty:
        raise RuntimeError("CSV lästes in men är tom. Kontrollera källfilen.")

    return df