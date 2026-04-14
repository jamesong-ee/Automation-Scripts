"""
Final Photo Pipeline Script
Generated on: 2025-06-20T01:40:14.391386
"""

import os
import shutil
import hashlib
from pathlib import Path
from PIL import Image
from PIL.ExifTags import TAGS
from tqdm import tqdm
from datetime import datetime

INBOX_DIR = r"E:\10-19 Personal\11 Photos and Videos\11.00 Inbox"
ARCHIVE_DIR = r"E:\10-19 Personal\11 Photos and Videos\Camera Roll\photos"
DUPLICATES_DIR = r"E:\10-19 Personal\11 Photos and Videos\Camera Roll\duplicates"
SKIPPED_DIR = r"E:\10-19 Personal\11 Photos and Videos\Camera Roll\skipped"
AUDIT_DIR = r"E:\10-19 Personal\11 Photos and Videos\Camera Roll\audit"
LOGS_DIR = r"E:\10-19 Personal\11 Photos and Videos\Camera Roll\logs"

os.makedirs(DUPLICATES_DIR, exist_ok=True)
os.makedirs(SKIPPED_DIR, exist_ok=True)
os.makedirs(AUDIT_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)

log_path = os.path.join(LOGS_DIR, f"photo_processing_20250620_014410.txt")
summary = {
    "Renamed": 0,
    "Duplicates": 0,
    "Skipped": 0,
    "Audit": 0,
    "Total": 0
}

def get_exif_date(file_path):
    try:
        image = Image.open(file_path)
        exif_data = image._getexif()
        if not exif_data:
            return None
        for tag_id, value in exif_data.items():
            tag = TAGS.get(tag_id, tag_id)
            if tag == "DateTimeOriginal":
                return datetime.strptime(value, "%Y:%m:%d %H:%M:%S")
    except Exception:
        return None
    return None

def hash_file(file_path):
    h = hashlib.sha256()
    with open(file_path, 'rb') as f:
        while True:
            chunk = f.read(8192)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()

def process():
    entries = list(Path(INBOX_DIR).rglob("*"))
    files = [p for p in entries if p.is_file()]
    seen_hashes = set()

    with open(log_path, "w", encoding="utf-8") as log:
        log.write("=== Summary ===\n")

    for src in tqdm(files, desc=f"Processing {INBOX_DIR}", unit="file"):
        summary["Total"] += 1
        try:
            date = get_exif_date(src)
            if not date:
                shutil.copy2(src, Path(AUDIT_DIR) / src.name)
                summary["Audit"] += 1
                continue

            file_hash = hash_file(src)
            if file_hash in seen_hashes:
                shutil.copy2(src, Path(DUPLICATES_DIR) / src.name)
                summary["Duplicates"] += 1
                continue

            seen_hashes.add(file_hash)
            year = str(date.year)
            month = "{:02d}".format(date.month)
            dest_folder = Path(ARCHIVE_DIR) / year / month
            os.makedirs(dest_folder, exist_ok=True)

            dest_path = dest_folder / src.name
            if dest_path.exists():
                dest_path = dest_folder / f"copy_{src.name}"
            shutil.copy2(src, dest_path)
            summary["Renamed"] += 1

        except Exception:
            shutil.copy2(src, Path(SKIPPED_DIR) / src.name)
            summary["Skipped"] += 1

    with open(log_path, "r+", encoding="utf-8") as log:
        log.seek(0)
        for key in ["Renamed", "Duplicates", "Skipped", "Audit", "Total"]:
            log.write(f"{key}: {summary[key]}\n")
        log.write(f"Run started: {datetime.now().isoformat()}\n\n")

process()
