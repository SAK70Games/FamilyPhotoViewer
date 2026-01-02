# FamilyPhotoViewer

FamilyPhotoViewer is a simple tool that picks a small set of photos from the picture archive each day and displays them on a website as a daily "look back" on the past week across all years.

## Viewing Output

- Open this web page in any browser (e.g., Safari on iPhone) to view the photos from a GitHub repository:
https://sak70games.github.io/FamilyPhotoViewer/
- Family members can make this a bookmark

## How It Runs

1. Windows Task Scheduler calls the batch file at 3AM every day: run_family_photo_viewer.bat
2. The batch file calls the Python script (family_photo_viewer.py) located in scripts/ 
3. The Python script:  
   - Selects photos from the picture archive (D:\Pictures)  
   - Puts selected photos in the photos/ folder  
   - Generates a new index.html in the main folder that drives the website  
   - Dumps logs to the logs/ folder  
4. GitHub updates are pushed automatically, so the page can be viewed from the GitHub link


