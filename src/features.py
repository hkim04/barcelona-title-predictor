import pandas as pd

def create_features (matches: pd.DataFrame) -> pd.DataFrame:
    """Create features for the model."""
    df = matches.copy()

    df = df.reset_index(drop=True)
    df["match_id"] = df.index 
    # Home team perspective
    home = df[
        ["match_id", "season", "Date", "HomeTeam", "FTHG", "FTAG"]
    ].copy()

    home = home.rename(columns={
        "HomeTeam": "team",
        "FTHG": "goals_for",
        "FTAG": "goals_against"
    })

    home["is_home"] = 1

    # Away team perspective
    away = df[
        ["match_id", "season", "Date", "AwayTeam", "FTAG", "FTHG"]
    ].copy()

    away = away.rename(columns={
        "AwayTeam": "team",
        "FTAG": "goals_for",
        "FTHG": "goals_against"
    })

    away["is_home"] = 0

    # Combine home and away team records
    team_matches = pd.concat([home, away], ignore_index=True)

    # Calculate points earned in each match
    team_matches["points"] = 0

    team_matches.loc[
        team_matches["goals_for"] > team_matches["goals_against"],
        "points"
    ] = 3

    team_matches.loc[
        team_matches["goals_for"] == team_matches["goals_against"],
        "points"
    ] = 1

    # Sort each team's matches chronologically
    team_matches = team_matches.sort_values(
        ["team", "Date", "match_id"]
    )

    # Calculate points from the previous 5 matches
    team_matches["last5_points"] = (
        team_matches.groupby("team")["points"]
        .transform(
            lambda x: x.shift(1).rolling(5, min_periods=5).sum()
        )
    )

    # Separate home and away features
    home_features = team_matches[
        team_matches["is_home"] == 1
    ][["match_id", "last5_points"]].rename(
        columns={"last5_points": "home_last5_points"}
    )

    away_features = team_matches[
        team_matches["is_home"] == 0
    ][["match_id", "last5_points"]].rename(
        columns={"last5_points": "away_last5_points"}
    )

    # Attach features to original matches
    df = df.merge(home_features, on="match_id", how="left")
    df = df.merge(away_features, on="match_id", how="left")

    return df.drop(columns=["match_id"])