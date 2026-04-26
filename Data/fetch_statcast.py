import urllib.request
import time
import os

OUTPUT_PATH = '/Users/Ericc.Dai/Desktop/statcast_data_2025.csv'

# Define date chunks to stay under the export limit per request.
# Adjust granularity if a single chunk still exceeds ~40k rows.
DATE_RANGES = [
    ("2025-03-20", "2025-03-31"),  # Opening / spring
    ("2025-04-01", "2025-04-04"),
    ("2025-04-05", "2025-04-08"),
    ("2025-04-09", "2025-04-15"),
    ("2025-04-16", "2025-04-30"),
    ("2025-05-01", "2025-05-15"),
    ("2025-05-16", "2025-05-31"),
    ("2025-06-01", "2025-06-15"),
    ("2025-06-16", "2025-06-30"),
    ("2025-07-01", "2025-07-15"),
    ("2025-07-16", "2025-07-31"),
    ("2025-08-01", "2025-08-15"),
    ("2025-08-16", "2025-08-31"),
    ("2025-09-01", "2025-09-15"),
    ("2025-09-16", "2025-09-30"),
    ("2025-10-01", "2025-10-31"),  # Postseason
]

header = None
total_rows = 0

with open(OUTPUT_PATH, 'w') as out:
    for i, (start, end) in enumerate(DATE_RANGES):
        url = (
            'https://baseballsavant.mlb.com/statcast_search/csv'
            '?hfGT=R%7C'
            '&hfSea=2025%7C'
            '&player_type=pitcher'
            '&group_by=name-event'
            '&min_pitches=0'
            '&min_results=0'
            '&min_pas=0'
            '&sort_col=pitches'
            '&player_event_sort=api_p_release_speed'
            '&sort_order=desc'
            '&chk_event_release_speed=on'
            '&type=details'
            f'&game_date_gt={start}'
            f'&game_date_lt={end}'
            '&all=true'
        )

        print(f'[{i+1}/{len(DATE_RANGES)}] Fetching {start} to {end} ...')
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})

        try:
            resp = urllib.request.urlopen(req, timeout=180)
            data = resp.read().decode('utf-8', errors='replace')
        except Exception as e:
            print(f'  ERROR: {e} — skipping this chunk')
            continue

        lines = data.strip().split('\n')
        if len(lines) <= 1:
            print(f'  No data for this range.')
            continue

        # First chunk: write header + data. Later chunks: skip header.
        if header is None:
            header = lines[0]
            out.write(header + '\n')

        data_lines = lines[1:]
        chunk_rows = len(data_lines)
        total_rows += chunk_rows
        for line in data_lines:
            out.write(line + '\n')

        print(f'  Got {chunk_rows} rows (running total: {total_rows})')
        if chunk_rows >= 25000:
            print(f'  ⚠ WARNING: chunk hit 25k cap — data may be truncated! Split this range further.')

        # Be polite to the server
        if i < len(DATE_RANGES) - 1:
            time.sleep(3)

print(f'\nDone! {total_rows} total rows saved to {OUTPUT_PATH}')
