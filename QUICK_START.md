# Quick Start Guide

Get the Automated File Organizer up and running in 2 minutes!

## Prerequisites

- **Python 3.7 or higher** ([Download](https://www.python.org/downloads/))
- That's it! No other dependencies needed.

## Installation

### Step 1: Check Python Installation

**Windows (Command Prompt):**
```bash
python --version
```

**macOS/Linux (Terminal):**
```bash
python3 --version
```

If Python is not installed, [download it here](https://www.python.org/downloads/).

### Step 2: Download/Navigate to Project

```bash
# On Windows
cd C:\Users\YourName\Desktop\Automated file organizer

# On macOS/Linux
cd ~/Desktop/"Automated file organizer"
```

### Step 3: Verify Files

You should see these files:
- `file_organizer.py`
- `cli.py`
- `config.json`
- `README.md`

## Running the Organizer

### Option 1: Easiest - Click & Run

**Windows:**
1. Double-click `run_interactive.bat`
2. Choose your organization method
3. Done!

**macOS/Linux:**
1. Open Terminal
2. Run: `bash run_interactive.sh`
3. Choose your organization method
4. Done!

### Option 2: Command Line (More Control)

**Organize Downloads by Type:**
```bash
python cli.py --organize type --path ~/Downloads
```

**Organize Desktop by Date:**
```bash
python cli.py --organize date --path ~/Desktop
```

**See what would happen (no changes):**
```bash
python cli.py --organize type --path ~/Documents --dry-run
```

### Option 3: Interactive Menu

```bash
python cli.py --interactive
```

Shows a menu to choose organization method and other options.

## First-Time Examples

### Example 1: Organize Downloads

```bash
python cli.py --organize type --path ~/Downloads
```

**Before:**
```
Downloads/
├── document.pdf
├── photo.jpg
├── video.mp4
├── archive.zip
└── report.xlsx
```

**After:**
```
Downloads/
├── documents/
│   ├── document.pdf
│   └── report.xlsx
├── images/
│   └── photo.jpg
├── videos/
│   └── video.mp4
└── archives/
    └── archive.zip
```

### Example 2: Preview Before Organizing

```bash
# See what would happen
python cli.py --organize type --path ~/Documents --dry-run

# Actually do it
python cli.py --organize type --path ~/Documents
```

### Example 3: Organize and Cleanup

```bash
python cli.py --organize type --path ~/Desktop --cleanup
```

## Customizing Categories

Edit `config.json` to customize file categories:

```json
{
  "rules": {
    "images": [".jpg", ".png", ".gif"],
    "videos": [".mp4", ".mkv"],
    "documents": [".pdf", ".docx"]
  }
}
```

Add or remove file extensions as needed, then save and run:
```bash
python cli.py --organize type --path ~/MyFolder
```

## Common Tasks

| Task | Command |
|------|---------|
| Organize Downloads | `python cli.py --organize type --path ~/Downloads` |
| Move files (not copy) | `python cli.py --organize type --path ~/Downloads --move` |
| Clean empty folders | `python cli.py --cleanup --path ~/Downloads` |
| Preview changes | `python cli.py --organize type --path ~/Downloads --dry-run` |
| Interactive menu | `python cli.py --interactive` |

## Troubleshooting

### Python not found
```bash
# Try:
python3 --version

# Or install Python from:
https://www.python.org/downloads/
```

### Permission denied (macOS/Linux)
```bash
# Make script executable
chmod +x run_interactive.sh

# Then run
./run_interactive.sh
```

### Files not organizing
1. Check that extensions are in `config.json`
2. Verify the path exists: `ls ~/Downloads` (macOS/Linux) or `dir C:\Users\...\Downloads` (Windows)
3. Check logs in the `logs/` folder

### Want to undo?
By default, files are copied (not moved), so originals remain. Delete the organized folders to undo.

## Next Steps

1. **Read**: [README.md](README.md) for full documentation
2. **Learn**: [USAGE_EXAMPLES.md](USAGE_EXAMPLES.md) for more examples
3. **Explore**: [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) for technical details
4. **Test**: Run on a small folder first to see how it works

## Getting Help

| Issue | Solution |
|-------|----------|
| Lost? | Try `python cli.py --help` |
| Want examples? | Read `USAGE_EXAMPLES.md` |
| Technical questions? | See `PROJECT_STRUCTURE.md` |
| Found a bug? | Check `logs/organizer_*.log` |

## You're All Set! 🎉

You can now organize your files efficiently. Start with:

```bash
python cli.py --interactive
```

Enjoy! 📁✨

---

**Need more help?** See [README.md](README.md)
