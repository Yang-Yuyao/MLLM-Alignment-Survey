"""Print current snapshot counts using only the Python standard library."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
m = json.loads((ROOT / 'catalog/manifest.json').read_text())
print(f"Snapshot: {m['snapshot_date']} ({m['manuscript_commit'][:7]})")
print(f"Current body-cited records: {m['current_paper_count']}")
print(f"Timeline records: {m['timeline_paper_count']}")
print(f"Supplement references: {m['supplement_reference_count']}")
print('Domain memberships overlap:')
for domain, counts in m['domain_counts'].items():
    print(f"  {domain}: {counts['total']} catalog / {counts['cited_in_chapter']} chapter / {counts['timeline']} timeline")
print(f"Historical/inactive records: {m['archived_entry_count']}")
print(f"History snapshots inspected: {m['history_snapshots']}")
