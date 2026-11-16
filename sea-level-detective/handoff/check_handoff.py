"""Read the hand-off workbook back and print each sheet's size plus the key results (a check, no computation)."""
from pathlib import Path
from openpyxl import load_workbook

wb = load_workbook(Path(__file__).resolve().parent / "SeaLevelDetective_data_handoff.xlsx", read_only=True)
for ws in wb.worksheets:
    print(f"{ws.title:<22} rows {ws.max_row:>6}  cols {ws.max_column:>3}")
print("\nKey_results:")
for row in wb["Key_results"].iter_rows(min_row=2, values_only=True):
    print("  ", " | ".join("" if v is None else str(v) for v in row[:4]))
print("\nSeason_predictions (header + 3 test rows):")
rows = list(wb["Season_predictions"].iter_rows(min_row=3, values_only=True))
print("  ", rows[0])
for r in rows[-4:-1]:
    print("  ", tuple(round(v, 2) if isinstance(v, float) else v for v in r))
empty = [ws.title for ws in wb.worksheets if ws.max_row < 3]
print("\nempty sheets:", empty or "none")
