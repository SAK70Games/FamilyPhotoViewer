import os
import shutil
import random
from datetime import datetime, timedelta
from pathlib import Path

# Optional: install these first if HEIC support is needed
# pip install pillow pillow-heif

from PIL import Image
import pillow_heif

# ===== CONFIG =====
archive_root = Path(r"D:\Pictures")
photos_folder = Path(r"D:\FamilyPhotoViewer\photos")  # Images only
output_html = Path("D:\FamilyPhotoViewer\index.html")  # HTML outside photos
num_photos_per_day = 5
days_to_look_back = 7
supported_extensions = {'.jpg', '.jpeg', '.heic', '.png'}

# ===== SETUP =====
photos_folder.mkdir(parents=True, exist_ok=True)
today = datetime.today()

# ===== HELPER FUNCTIONS =====
def is_valid_photo(file_path):
    return file_path.suffix.lower() in supported_extensions

def convert_heic_to_jpg(src_path, dest_path):
    heif_file = pillow_heif.read_heif(str(src_path))
    image = Image.frombytes(
        heif_file.mode,
        heif_file.size,
        heif_file.data,
        "raw"
    )
    image.save(dest_path, format="JPEG")

# ===== MAIN =====
candidate_photos = []

for year in range(2003, 2026):
    year_path = archive_root / str(year)
    if not year_path.exists():
        continue

    for day_folder in os.listdir(year_path):
        day_path = year_path / day_folder
        if not day_path.is_dir():
            continue

        folder_date_str = day_folder[:10]  # YYYY-MM-DD
        try:
            folder_date = datetime.strptime(folder_date_str, "%Y-%m-%d")
        except ValueError:
            continue

        # Align folder date to current year
        try:
            folder_date_this_year = folder_date.replace(year=today.year)
        except ValueError:
            # Skip invalid dates like Feb 29 on non-leap years
            continue

        delta = today - folder_date_this_year
        if timedelta(0) <= delta <= timedelta(days=days_to_look_back - 1):
            # Include this folder
            for file in day_path.iterdir():
                if file.is_file() and is_valid_photo(file):
                    candidate_photos.append(file)

print(f"Found {len(candidate_photos)} candidate photos from last {days_to_look_back} days relative to each year.")

# Randomly pick up to 5
selected_photos = random.sample(candidate_photos, min(num_photos_per_day, len(candidate_photos)))
print(f"Selected {len(selected_photos)} photos:")

# Clear photos folder
for existing_file in photos_folder.iterdir():
    if existing_file.is_file():
        existing_file.unlink()

# Copy / convert photos
for photo in selected_photos:
    dest_file = photos_folder / (photo.stem + ".jpg")
    if photo.suffix.lower() == '.heic':
        convert_heic_to_jpg(photo, dest_file)
        print(f"Converted HEIC → JPG: {photo.name}")
    else:
        shutil.copy2(photo, dest_file)
        print(f"Copied: {photo.name}")

# Generate index.html outside photos folder
with open(output_html, "w", encoding="utf-8") as f:
    f.write("<html><head><title>Family Photo Viewer</title></head><body>\n")
    f.write("<h1>Family Photo Viewer</h1>\n")
    for photo_file in photos_folder.iterdir():
        if photo_file.suffix.lower() == ".jpg":
            # Add path relative to HTML
            f.write(f'<img src="photos/{photo_file.name}" style="max-width:100%;margin-bottom:10px;"><br>\n')
    f.write("</body></html>\n")

print(f"index.html generated at: {output_html}")
