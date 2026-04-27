from __future__ import annotations

import csv
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent
INPUT = DATA_DIR / "statcast_data_2025.csv"
OUTPUT = DATA_DIR / "statcast_data_2025_clean.csv"
PREVIEW_OUTPUT = DATA_DIR / "statcast_data_2025_clean_preview.csv"
PREVIEW_ROWS = 1000

# Middle-ground schema:
# - preserves every column used by the notebook
# - keeps a small set of still-relevant context columns
# - retains the scoreboard fields the user asked to keep
KEEP_COLUMNS = {
    "pitch_type",
    "game_date",
    "release_speed",
    "player_name",
    "batter",
    "pitcher",
    "events",
    "description",
    "zone",
    "game_type",
    "stand",
    "p_throws",
    "home_team",
    "away_team",
    "bb_type",
    "balls",
    "strikes",
    "pfx_x",
    "pfx_z",
    "plate_x",
    "plate_z",
    "on_3b",
    "on_2b",
    "on_1b",
    "outs_when_up",
    "inning",
    "inning_topbot",
    "hc_x",
    "hc_y",
    "hit_distance_sc",
    "launch_speed",
    "launch_angle",
    "effective_speed",
    "release_spin_rate",
    "release_extension",
    "game_pk",
    "estimated_woba_using_speedangle",
    "woba_value",
    "woba_denom",
    "at_bat_number",
    "pitch_number",
    "home_score",
    "away_score",
    "bat_score",
    "fld_score",
    "post_away_score",
    "post_home_score",
    "post_bat_score",
    "post_fld_score",
    "spin_axis",
    "delta_home_win_exp",
    "delta_run_exp",
    "bat_speed",
    "swing_length",
    "home_score_diff",
    "bat_score_diff",
    "home_win_exp",
}


def main() -> None:
    with INPUT.open("r", encoding="utf-8-sig", newline="") as fin:
        reader = csv.DictReader(fin)
        if reader.fieldnames is None:
            raise ValueError(f"No header row found in {INPUT}")

        missing = sorted(KEEP_COLUMNS - set(reader.fieldnames))
        if missing:
            raise ValueError(f"Missing requested columns: {missing}")

        keep = [col for col in reader.fieldnames if col in KEEP_COLUMNS]
        dropped = [col for col in reader.fieldnames if col not in KEEP_COLUMNS]

        row_count = 0
        with OUTPUT.open("w", encoding="utf-8", newline="") as fout, PREVIEW_OUTPUT.open(
            "w", encoding="utf-8", newline=""
        ) as preview_out:
            writer = csv.DictWriter(fout, fieldnames=keep, quoting=csv.QUOTE_MINIMAL)
            preview_writer = csv.DictWriter(
                preview_out, fieldnames=keep, quoting=csv.QUOTE_MINIMAL
            )
            writer.writeheader()
            preview_writer.writeheader()

            for row_count, row in enumerate(reader, start=1):
                trimmed = {col: row[col] for col in keep}
                writer.writerow(trimmed)
                if row_count <= PREVIEW_ROWS:
                    preview_writer.writerow(trimmed)

    print(f"Input : {INPUT}")
    print(f"Output: {OUTPUT}")
    print(f"Preview: {PREVIEW_OUTPUT}")
    print(f"Rows written: {row_count:,}")
    print(f"Columns kept: {len(keep)}")
    print(f"Columns dropped: {len(dropped)}")


if __name__ == "__main__":
    main()
