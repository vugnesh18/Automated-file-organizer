# Practical Usage Examples

This document provides real-world examples of how to use the Automated File Organizer.

## Quick Start Examples

### 1. Organize Your Downloads Folder (Simplest)

**Scenario**: Your Downloads folder is a mess with all types of files mixed together.

```bash
python cli.py --organize type --path ~/Downloads --interactive
```

This will:
- Show you a menu to choose organization method
- Organize files by type into categories
- Display results showing how many files were organized

### 2. Organize by Date (Archives)

**Scenario**: You want to organize old project files by when they were created.

```bash
python cli.py --organize date --path ~/Documents --move
```

Structure created:
```
2024/
  01 - January/
  02 - February/
2023/
  12 - December/
  ...
```

### 3. Find Large Files

**Scenario**: Your disk is full and you want to find and organize large files.

```bash
python cli.py --organize size --path ~/
```

Structure created:
```
Small_<1MB/
Medium_1-100MB/
Large_>100MB/  <- Find these first!
```

## Advanced Examples

### 4. Move Files (Not Copy)

**Scenario**: You want to permanently move files instead of copying.

```bash
python cli.py --organize type --path ~/Downloads --move --cleanup
```

This will:
- Move files to category folders
- Remove empty directories after organization
- Clean up the original directory

### 5. Preview Before Organizing

**Scenario**: You're nervous about organizing - preview first!

```bash
python cli.py --organize type --path ~/Documents --dry-run
```

This shows what would happen without actually moving/copying files.

### 6. Use Custom Rules

**Scenario**: You have specialized file types you want to organize.

Create `my_config.json`:
```json
{
  "source_directory": ".",
  "rules": {
    "projects": [".prj", ".psd", ".ai"],
    "documents": [".pdf", ".docx"],
    "data": [".csv", ".xlsx"]
  }
}
```

Then run:
```bash
python cli.py --organize type --path ~/Work --config my_config.json
```

### 7. Organize Multiple Folders (Script)

**Scenario**: You want to organize several folders at once.

Create `organize_all.py`:
```python
from file_organizer import FileOrganizer

organizer = FileOrganizer()

folders = [
    "~/Downloads",
    "~/Documents",
    "~/Desktop"
]

for folder in folders:
    print(f"Organizing {folder}...")
    stats = organizer.organize_files(folder)
    print(f"  Organized {stats['organized_files']} files")
    organizer.cleanup_empty_folders(folder)
```

Run:
```bash
python organize_all.py
```

### 8. Interactive Mode with Cleanup

**Scenario**: You want a guided experience with cleanup at the end.

```bash
python cli.py --interactive
```

Then:
1. Choose "Organize by file type"
2. Later choose "Clean up empty folders"
3. Choose "Exit"

## Real-World Scenarios

### Scenario A: Clean Up Downloads After a Week

```bash
# Review what will happen
python cli.py --organize type --path ~/Downloads --dry-run

# Actually organize
python cli.py --organize type --path ~/Downloads

# Clean up
python cli.py --cleanup --path ~/Downloads
```

### Scenario B: Archive Old Project Files

```bash
# Create archive folder
mkdir ~/Archives

# Move files into organized date structure
python cli.py --organize date --path ~/Archives --move --cleanup
```

### Scenario C: Find Space-Hogging Files

```bash
# Organize by size to see what's taking up space
python cli.py --organize size --path ~/

# Check the Large_>100MB folder
ls ~/Large_>100MB/
```

### Scenario D: Professional File Organization

Create a custom config for your business:

```json
{
  "rules": {
    "invoices": [".pdf", ".xlsx"],
    "proposals": [".docx", ".pptx"],
    "contracts": [".pdf"],
    "reports": [".xlsx", ".csv"],
    "correspondence": [".pdf", ".docx"]
  }
}
```

```bash
python cli.py --organize type --path ~/BusinessDocs --config business_config.json
```

## Using in Python Scripts

### Example 1: Organize and Log

```python
from file_organizer import FileOrganizer

organizer = FileOrganizer("config.json")

# Organize files
stats = organizer.organize_files("~/Downloads")

# Print detailed results
print(f"Total: {stats['total_files']}")
print(f"Organized: {stats['organized_files']}")
print(f"Failed: {stats['failed_files']}")

for category, count in stats['categories'].items():
    print(f"  {category}: {count}")
```

### Example 2: Batch Processing

```python
from pathlib import Path
from file_organizer import FileOrganizer

organizer = FileOrganizer()

# Get all subdirectories in a folder
base_path = Path("~/Documents")
for folder in base_path.iterdir():
    if folder.is_dir():
        print(f"Processing {folder.name}...")
        stats = organizer.organize_files(str(folder))
        if stats['organized_files'] > 0:
            print(f"  Organized {stats['organized_files']} files")
```

### Example 3: Conditional Organization

```python
from file_organizer import FileOrganizer
from pathlib import Path

organizer = FileOrganizer()

path = Path("~/Downloads")

# Count files
file_count = len(list(path.glob("*")))

if file_count > 100:
    print("Too many files! Organizing...")
    stats = organizer.organize_files(str(path))
    organizer.cleanup_empty_folders(str(path))
else:
    print("Folder is clean")
```

## Tips & Tricks

### Tip 1: Safe Testing
Always use `--dry-run` first:
```bash
python cli.py --organize type --path ~/MyFolder --dry-run
```

### Tip 2: Different Config for Different Folders
```bash
# Work files
python cli.py --path ~/Work --config work_config.json

# Personal files
python cli.py --path ~/Personal --config personal_config.json
```

### Tip 3: Check Logs
After organizing, check logs for details:
```bash
ls -la logs/
tail -f logs/organizer_*.log
```

### Tip 4: Backup Before Moving
Always backup before using `--move`:
```bash
cp -r ~/Documents ~/Documents.backup
python cli.py --organize type --path ~/Documents --move
```

### Tip 5: Organize Desktop Regularly
Add to your weekly routine:
```bash
python cli.py --organize type --path ~/Desktop --cleanup
```

## Troubleshooting Common Issues

### "Permission Denied" Error

```bash
# Run with appropriate permissions
# On Windows, run Command Prompt as Administrator
python cli.py --organize type --path C:\Users\YourName\Downloads

# On macOS/Linux
sudo python cli.py --organize type --path /path/to/folder
```

### Files Not Organizing

Check the log file:
```bash
cat logs/organizer_*.log
```

Add the extension to config.json if it's missing.

### Want to Undo Organization

If you used `--copy` (default), original files are still there:
```bash
# Delete organized files (but keep originals)
rm -r ~/Documents/documents ~/Documents/images ~/Documents/videos
```

If you used `--move`, restore from backup:
```bash
rm -r ~/Documents/*
cp -r ~/Documents.backup/* ~/Documents/
```

## Performance Notes

- **Small folders** (< 100 files): < 1 second
- **Medium folders** (100-1000 files): 1-5 seconds
- **Large folders** (1000+ files): 5-30 seconds

For very large folders, consider organizing subfolder by subfolder.

## Next Steps

1. **Start simple**: Use `--interactive` mode first
2. **Backup**: Keep a backup before using `--move`
3. **Customize**: Create your own config.json for specific needs
4. **Automate**: Schedule regular organization with cron (Linux) or Task Scheduler (Windows)
5. **Extend**: Add new categories and rules as needed

---

Happy organizing! 📁✨
