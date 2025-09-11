# Media Pipeline – Photo/Video Organizer

**Problem**  
Thousands of mixed photos/videos in one folder. Manual sorting would take days.

**What it does**  
- Reads metadata timestamps and sorts into YYYY/MM folders
- Deduplicates by SHA-256 hash (“digital fingerprint”)
- Quarantines unreadable/corrupt files so the job never crashes
- Produces an audit log (moved, duplicates, errors, totals)
- Dry-run mode to preview actions safely

**Quick start**
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python media_pipeline.py --src /path/inbox --dst /path/library --quarantine /path/quarantine --log ./sample_logs/run_$(date +%F).log --dry-run
# remove --dry-run to execute
