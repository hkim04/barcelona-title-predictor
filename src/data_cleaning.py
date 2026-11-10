import pandas as pd

REQUIRED_COLUMNS = ["season", "Date", "HomeTeam", "AwayTeam", "FTHG", "FTAG", "FTR"]

def clean_matches(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and validate historical La Liga match data."""
    # 1. Check that all required columns exist
    missing_columns = set(REQUIRED_COLUMNS) - set(df.columns)

    if missing_columns:
        raise ValueError(f"Missing columns: {missing_columns}")

    # 2. Select the columns we need
    cleaned = df[REQUIRED_COLUMNS].copy()

    # 3. Convert dates from strings to datetime
    cleaned["Date"] = pd.to_datetime(
        cleaned["Date"],
        dayfirst=True,
        errors="coerce"
    )

    # 4. Check for missing values
    if cleaned.isna().any().any():
        raise ValueError("Missing values found in required columns")

    # 5. Check for duplicate matches
    duplicate_columns = [
        "season", "Date", "HomeTeam", "AwayTeam"
    ]

    if cleaned.duplicated(subset=duplicate_columns).any():
        raise ValueError("Duplicate matches found")

    # 6. Validate match results
    expected_results = pd.Series("D", index=cleaned.index)

    expected_results.loc[
        cleaned["FTHG"] > cleaned["FTAG"]
    ] = "H"

    expected_results.loc[
        cleaned["FTHG"] < cleaned["FTAG"]
    ] = "A"

    if not cleaned["FTR"].eq(expected_results).all():
        raise ValueError("Match results do not match the scores")

    # 7. Sort matches chronologically
    cleaned = cleaned.sort_values(
        ["Date", "HomeTeam", "AwayTeam"]
    ).reset_index(drop=True)

    return cleaned