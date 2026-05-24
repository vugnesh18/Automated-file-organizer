# Project Structure & Documentation

## Directory Structure

```
Automated file organizer/
├── file_organizer.py          # Main file organizer module
├── cli.py                      # Command-line interface
├── config.json                 # Configuration file with file categories
├── test_file_organizer.py      # Unit tests
├── requirements.txt            # Python dependencies
├── README.md                   # Main documentation
├── USAGE_EXAMPLES.md          # Practical usage examples
├── PROJECT_STRUCTURE.md       # This file
├── run_interactive.bat        # Windows launcher script
├── run_interactive.sh         # Linux/macOS launcher script
└── logs/                      # Auto-created: Organization logs

```

## File Descriptions

### Core Files

#### `file_organizer.py`
The main module containing the `FileOrganizer` class with all file organization logic.

**Key Classes:**
- `FileOrganizer`: Main class for all file organization operations

**Key Methods:**
- `organize_files()`: Organize files by file extension type
- `organize_by_date()`: Organize files by creation date (Year/Month)
- `organize_by_size()`: Organize files by size categories
- `cleanup_empty_folders()`: Remove empty directories
- `_categorize_file()`: Determine file category based on extension

**Dependencies:** None (uses only Python standard library)

---

#### `cli.py`
Command-line interface for the file organizer using Python's `argparse` module.

**Key Functions:**
- `main()`: Main CLI entry point with argument parsing
- `run_interactive()`: Interactive menu system
- `print_results()`: Format and display organization results
- `create_default_config()`: Generate default configuration file

**Supported Arguments:**
- `--organize`: Choose organization method (type, date, size)
- `--path`: Directory to organize
- `--config`: Custom configuration file
- `--move`: Move files instead of copying
- `--cleanup`: Clean up empty folders
- `--dry-run`: Preview without changes
- `--interactive`: Interactive mode
- `--create-default-config`: Generate config template

---

### Configuration Files

#### `config.json`
JSON configuration file defining file categories and organization rules.

**Structure:**
```json
{
  "source_directory": ".",           // Default directory
  "organize_by": "extension",        // Default method
  "create_subdirectories": true,     // Create category folders
  "move_files": false,               // Copy (false) or move (true)
  "rules": {
    "category_name": [".ext1", ".ext2"]
  }
}
```

**How to Customize:**
1. Open `config.json` in a text editor
2. Add or modify categories under `rules`
3. Add file extensions (include the dot)
4. Save and run the organizer

---

### Testing

#### `test_file_organizer.py`
Comprehensive unit tests for the file organizer.

**Test Classes:**
- `TestFileOrganizer`: Unit tests for core functionality
- `TestFileOrganizerIntegration`: Integration tests

**Running Tests:**
```bash
# Install pytest (optional)
pip install pytest

# Run tests
pytest test_file_organizer.py -v

# Or using unittest
python -m unittest test_file_organizer.py -v
```

**Coverage:**
- ✅ File categorization
- ✅ File organization by type
- ✅ File organization by date
- ✅ File organization by size
- ✅ Duplicate filename handling
- ✅ Empty folder cleanup
- ✅ Error handling
- ✅ Configuration loading

---

### Documentation

#### `README.md`
Complete user documentation with installation, usage, and features.

**Sections:**
- Features overview
- Installation instructions
- Usage modes (interactive, CLI, Python API)
- Configuration guide
- Output structure examples
- Troubleshooting
- Future enhancements

---

#### `USAGE_EXAMPLES.md`
Practical, real-world usage examples for common scenarios.

**Examples:**
- Quick start examples
- Advanced usage patterns
- Real-world scenarios
- Python API examples
- Tips and tricks
- Troubleshooting common issues

---

#### `PROJECT_STRUCTURE.md`
This file - detailed documentation of project organization.

---

### Setup & Launch Scripts

#### `run_interactive.bat` (Windows)
Batch script to launch the interactive mode on Windows.

**Usage:**
```bash
# Double-click or run from command prompt
run_interactive.bat
```

---

#### `run_interactive.sh` (Linux/macOS)
Bash script to launch the interactive mode on Unix-like systems.

**Usage:**
```bash
# Make executable
chmod +x run_interactive.sh

# Run
./run_interactive.sh
```

---

### Dependencies

#### `requirements.txt`
Lists all Python dependencies.

**Current Status:** No external dependencies!

The file organizer uses only Python's standard library:
- `os` - Operating system operations
- `shutil` - High-level file operations
- `pathlib` - Path handling
- `json` - Configuration loading
- `datetime` - Date operations
- `logging` - Event logging

---

## Data Flow

### File Organization Flow

```
User Input (CLI/Script)
    ↓
CLI Parser (cli.py)
    ↓
FileOrganizer Instance (file_organizer.py)
    ↓
Load Configuration (config.json)
    ↓
Scan Directory
    ↓
For each file:
  - Categorize file
  - Create category folder
  - Handle duplicates
  - Move or copy file
  - Log operation
    ↓
Generate Statistics
    ↓
Display Results & Logs
    ↓
Cleanup Empty Folders (optional)
```

---

## Usage Modes

### 1. Interactive Mode
Best for: Casual users, exploratory use

```bash
python cli.py --interactive
```

**Flow:**
- Display menu
- Wait for user choice
- Execute organization
- Show results
- Return to menu

---

### 2. Command-Line Mode
Best for: Scripting, automation

```bash
python cli.py --organize type --path ~/Downloads --move --cleanup
```

**Advantages:**
- Scriptable
- Automatable
- Suitable for cron/scheduled tasks
- Chainable with other commands

---

### 3. Python API Mode
Best for: Integration with other Python projects

```python
from file_organizer import FileOrganizer

organizer = FileOrganizer("config.json")
stats = organizer.organize_files("~/Downloads")
```

---

## Customization Guide

### Adding New File Categories

1. **Edit `config.json`:**
```json
{
  "rules": {
    "my_new_category": [".ext1", ".ext2", ".ext3"]
  }
}
```

2. **Run organizer:**
```bash
python cli.py --organize type --path ~/MyFolder
```

---

### Creating Custom Configuration

1. **Create `my_config.json`:**
```json
{
  "source_directory": ".",
  "rules": {
    "project_files": [".prj", ".psd"],
    "source_code": [".py", ".js", ".ts"]
  }
}
```

2. **Use it:**
```bash
python cli.py --organize type --config my_config.json
```

---

### Extending the FileOrganizer Class

```python
from file_organizer import FileOrganizer

class MyOrganizer(FileOrganizer):
    def organize_by_name_pattern(self):
        """Custom organization method"""
        # Your implementation here
        pass

organizer = MyOrganizer()
organizer.organize_by_name_pattern()
```

---

## Logging

### Log Location
```
logs/organizer_YYYYMMDD_HHMMSS.log
```

### Log Levels
- **DEBUG**: Detailed information about file operations
- **INFO**: Summary of operations
- **WARNING**: Non-critical issues
- **ERROR**: File operation errors

### Sample Log Entry
```
2024-01-15 10:30:45,123 - file_organizer - DEBUG - Copied image.jpg to images/
```

---

## Performance Characteristics

### File Processing Speed
| Folder Size | Time |
|------------|------|
| < 100 files | < 1 second |
| 100-1000 files | 1-5 seconds |
| 1000-10000 files | 5-30 seconds |
| > 10000 files | 30+ seconds |

### Memory Usage
- **Minimal**: Processes files sequentially
- **Independent of folder size**: No full directory scan in memory
- **Typical usage**: < 50MB RAM

---

## Common Patterns

### Pattern 1: Organization with Backup
```bash
# Backup first
cp -r ~/Documents ~/Documents.backup

# Then organize
python cli.py --organize type --path ~/Documents --move
```

### Pattern 2: Test Before Execution
```bash
# Preview
python cli.py --organize date --path ~/Downloads --dry-run

# Actually run
python cli.py --organize date --path ~/Downloads
```

### Pattern 3: Multi-Folder Automation
```python
from pathlib import Path
from file_organizer import FileOrganizer

organizer = FileOrganizer()

for folder in Path("~/Projects").iterdir():
    if folder.is_dir():
        print(f"Organizing {folder.name}...")
        organizer.organize_files(str(folder))
```

---

## Troubleshooting

### Debug Mode
Enable debug logging:
```python
import logging
logging.getLogger().setLevel(logging.DEBUG)
```

### Check Logs
```bash
# View latest log
tail -f logs/organizer_*.log

# Search for errors
grep ERROR logs/organizer_*.log
```

### Verify Configuration
```bash
python -c "import json; print(json.dumps(json.load(open('config.json')), indent=2))"
```

---

## Future Enhancements

- [ ] GUI Interface (Tkinter/PyQt)
- [ ] Watch mode (auto-organize on file changes)
- [ ] Undo functionality
- [ ] Advanced filtering
- [ ] Regular expression support
- [ ] Cloud storage integration
- [ ] Scheduling support (APScheduler)
- [ ] File conflict resolution UI
- [ ] Performance optimization for large folders
- [ ] Cross-platform path handling improvements

---

## Contributing Guidelines

1. **Bug Reports**: Include error logs and reproduction steps
2. **Feature Requests**: Describe use case and expected behavior
3. **Code Changes**: Ensure tests pass and follow Python style guide
4. **Documentation**: Update README and USAGE_EXAMPLES as needed

---

## License & Support

**License**: MIT License
**Python Version**: 3.7+
**Platform**: Windows, macOS, Linux
**Support**: See README.md troubleshooting section

---

Last Updated: January 2024
Version: 1.0.0
