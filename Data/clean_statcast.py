import csv

INPUT = '/Users/Ericc.Dai/Desktop/statcast_data_2025.csv'
OUTPUT = '/Users/Ericc.Dai/Desktop/statcast_data_2025_clean.csv'

DROP_COLS = {
    'spin_dir',
    'spin_rate_deprecated',
    'break_angle_deprecated',
    'break_length_deprecated',
    'tfs_deprecated',
    'tfs_zulu_deprecated',
    'umpire',
    'game_year',
    'sv_id',
    'age_pit_legacy',
    'age_bat_legacy',
    'fielder_2',
    'fielder_3',
    'fielder_4',
    'fielder_5',
    'fielder_6',
    'fielder_7',
    'fielder_8',
    'fielder_9',
}

with open(INPUT, 'r', encoding='utf-8-sig') as fin, open(OUTPUT, 'w', newline='') as fout:
    reader = csv.DictReader(fin)
    keep = [c for c in reader.fieldnames if c.strip('"') not in DROP_COLS]
    writer = csv.DictWriter(fout, fieldnames=keep, quoting=csv.QUOTE_MINIMAL)
    writer.writeheader()

    count = 0
    for row in reader:
        writer.writerow({k: row[k] for k in keep})
        count += 1

print(f'Done — {count} rows, {len(keep)} columns (dropped {len(DROP_COLS)})')
print(f'Output: {OUTPUT}')
