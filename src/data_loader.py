import pandas as pd
from src.config import RAW_DATA_DIR

def load_season(season: str) -> pd.DataFrame:
    """
    Load La Liga match data for one season.

    Example:
        load_season("2025_26")
    """

    file_path = RAW_DATA_DIR / f"laliga_{season}.csv"

    if not file_path.exists():
        raise FileNotFoundError(
            f"CSV file not found: {file_path}"
        )

    return pd.read_csv(file_path)

def load_all_seasons(seasons: list[str]) -> pd.DataFrame:
    """load and combine multiplke la liga season """
    dataframes = []
    
    for season in seasons:
        df = load_season(season)
        df["season"] = season  # Add a new column for the season
        dataframes.append(df)

    return pd.concat(dataframes, ignore_index=True)