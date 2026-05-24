"""
Automated File Organizer
A flexible file organization tool that categorizes and moves files based on configurable rules.
"""

import os
import shutil
from pathlib import Path
from typing import Dict, List, Optional
import json
from datetime import datetime
import logging


class FileOrganizer:
    """Main file organizer class for categorizing and moving files."""
    
    def __init__(self, config_path: str = "config.json"):
        """Initialize the file organizer with configuration."""
        self.config = self._load_config(config_path)
        self.logger = self._setup_logging()
        
    def _setup_logging(self) -> logging.Logger:
        """Set up logging configuration."""
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)
        
        # Create logs directory if it doesn't exist
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        # File handler
        fh = logging.FileHandler(log_dir / f"organizer_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
        fh.setLevel(logging.DEBUG)
        
        # Console handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        
        logger.addHandler(fh)
        logger.addHandler(ch)
        
        return logger
    
    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from JSON file."""
        if not Path(config_path).exists():
            self.logger.warning(f"Config file {config_path} not found. Using default config.")
            return self._get_default_config()
        
        with open(config_path, 'r') as f:
            return json.load(f)
    
    def _get_default_config(self) -> Dict:
        """Return default configuration."""
        return {
            "source_directory": ".",
            "organize_by": "extension",
            "create_subdirectories": True,
            "move_files": False,
            "rules": {
                "documents": [".pdf", ".doc", ".docx", ".txt", ".xlsx", ".xls", ".ppt", ".pptx"],
                "images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".ico"],
                "videos": [".mp4", ".mkv", ".avi", ".mov", ".flv", ".wmv"],
                "audio": [".mp3", ".wav", ".flac", ".aac", ".m4a", ".wma"],
                "archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
                "code": [".py", ".js", ".ts", ".cpp", ".c", ".java", ".html", ".css", ".json"],
                "executables": [".exe", ".msi", ".app"]
            }
        }
    
    def organize_files(self, source_dir: Optional[str] = None) -> Dict:
        """
        Organize files in the specified directory.
        
        Args:
            source_dir: Directory to organize (uses config if not specified)
            
        Returns:
            Dictionary with organization statistics
        """
        source_dir = Path(source_dir or self.config["source_directory"])
        
        if not source_dir.exists():
            self.logger.error(f"Source directory {source_dir} does not exist.")
            return {"status": "error", "message": "Directory not found"}
        
        self.logger.info(f"Starting file organization in {source_dir}")
        
        stats = {
            "total_files": 0,
            "organized_files": 0,
            "failed_files": 0,
            "categories": {}
        }
        
        # Get all files in the directory (non-recursive)
        files = [f for f in source_dir.iterdir() if f.is_file()]
        stats["total_files"] = len(files)
        
        for file_path in files:
            try:
                category = self._categorize_file(file_path)
                
                if category and category != "unorganized":
                    self._organize_file(file_path, source_dir, category)
                    stats["organized_files"] += 1
                    stats["categories"][category] = stats["categories"].get(category, 0) + 1
                else:
                    self.logger.debug(f"File {file_path.name} could not be categorized")
                    
            except Exception as e:
                self.logger.error(f"Error organizing file {file_path.name}: {str(e)}")
                stats["failed_files"] += 1
        
        self.logger.info(f"Organization complete. Organized {stats['organized_files']} files")
        return stats
    
    def _categorize_file(self, file_path: Path) -> str:
        """
        Categorize a file based on its extension.
        
        Args:
            file_path: Path to the file
            
        Returns:
            Category name or None
        """
        file_extension = file_path.suffix.lower()
        rules = self.config.get("rules", {})
        
        for category, extensions in rules.items():
            if file_extension in extensions:
                return category
        
        return "unorganized"
    
    def _organize_file(self, file_path: Path, source_dir: Path, category: str) -> None:
        """
        Move or copy file to the appropriate category folder.
        
        Args:
            file_path: Path to the file
            source_dir: Source directory
            category: Category name
        """
        # Create category directory
        category_dir = source_dir / category
        category_dir.mkdir(exist_ok=True)
        
        destination = category_dir / file_path.name
        
        # Handle duplicate filenames
        if destination.exists():
            base_name = file_path.stem
            extension = file_path.suffix
            counter = 1
            while destination.exists():
                destination = category_dir / f"{base_name}_{counter}{extension}"
                counter += 1
        
        # Move or copy file
        if self.config.get("move_files", False):
            shutil.move(str(file_path), str(destination))
            self.logger.debug(f"Moved {file_path.name} to {category}/")
        else:
            shutil.copy2(str(file_path), str(destination))
            self.logger.debug(f"Copied {file_path.name} to {category}/")
    
    def organize_by_date(self, source_dir: Optional[str] = None) -> Dict:
        """
        Organize files by creation date (Year/Month structure).
        
        Args:
            source_dir: Directory to organize
            
        Returns:
            Dictionary with organization statistics
        """
        source_dir = Path(source_dir or self.config["source_directory"])
        
        if not source_dir.exists():
            self.logger.error(f"Source directory {source_dir} does not exist.")
            return {"status": "error", "message": "Directory not found"}
        
        self.logger.info(f"Starting date-based organization in {source_dir}")
        
        stats = {
            "total_files": 0,
            "organized_files": 0,
            "failed_files": 0,
            "periods": {}
        }
        
        files = [f for f in source_dir.iterdir() if f.is_file()]
        stats["total_files"] = len(files)
        
        for file_path in files:
            try:
                # Get file modification time
                mod_time = datetime.fromtimestamp(file_path.stat().st_mtime)
                year = str(mod_time.year)
                month = f"{mod_time.month:02d} - {mod_time.strftime('%B')}"
                
                # Create directory structure
                date_dir = source_dir / year / month
                date_dir.mkdir(parents=True, exist_ok=True)
                
                destination = date_dir / file_path.name
                
                # Handle duplicates
                if destination.exists():
                    base_name = file_path.stem
                    extension = file_path.suffix
                    counter = 1
                    while destination.exists():
                        destination = date_dir / f"{base_name}_{counter}{extension}"
                        counter += 1
                
                # Move or copy
                if self.config.get("move_files", False):
                    shutil.move(str(file_path), str(destination))
                else:
                    shutil.copy2(str(file_path), str(destination))
                
                period = f"{year}/{month}"
                stats["periods"][period] = stats["periods"].get(period, 0) + 1
                stats["organized_files"] += 1
                
            except Exception as e:
                self.logger.error(f"Error organizing file {file_path.name}: {str(e)}")
                stats["failed_files"] += 1
        
        self.logger.info(f"Date-based organization complete. Organized {stats['organized_files']} files")
        return stats
    
    def organize_by_size(self, source_dir: Optional[str] = None) -> Dict:
        """
        Organize files by size (Small < 1MB, Medium 1-100MB, Large > 100MB).
        
        Args:
            source_dir: Directory to organize
            
        Returns:
            Dictionary with organization statistics
        """
        source_dir = Path(source_dir or self.config["source_directory"])
        
        if not source_dir.exists():
            self.logger.error(f"Source directory {source_dir} does not exist.")
            return {"status": "error", "message": "Directory not found"}
        
        self.logger.info(f"Starting size-based organization in {source_dir}")
        
        stats = {
            "total_files": 0,
            "organized_files": 0,
            "failed_files": 0,
            "sizes": {}
        }
        
        files = [f for f in source_dir.iterdir() if f.is_file()]
        stats["total_files"] = len(files)
        
        for file_path in files:
            try:
                file_size = file_path.stat().st_size
                
                # Categorize by size
                if file_size < 1024 * 1024:  # 1 MB
                    category = "Small_<1MB"
                elif file_size < 100 * 1024 * 1024:  # 100 MB
                    category = "Medium_1-100MB"
                else:
                    category = "Large_>100MB"
                
                # Create category directory
                size_dir = source_dir / category
                size_dir.mkdir(exist_ok=True)
                
                destination = size_dir / file_path.name
                
                # Handle duplicates
                if destination.exists():
                    base_name = file_path.stem
                    extension = file_path.suffix
                    counter = 1
                    while destination.exists():
                        destination = size_dir / f"{base_name}_{counter}{extension}"
                        counter += 1
                
                # Move or copy
                if self.config.get("move_files", False):
                    shutil.move(str(file_path), str(destination))
                else:
                    shutil.copy2(str(file_path), str(destination))
                
                stats["sizes"][category] = stats["sizes"].get(category, 0) + 1
                stats["organized_files"] += 1
                
            except Exception as e:
                self.logger.error(f"Error organizing file {file_path.name}: {str(e)}")
                stats["failed_files"] += 1
        
        self.logger.info(f"Size-based organization complete. Organized {stats['organized_files']} files")
        return stats
    
    def cleanup_empty_folders(self, source_dir: Optional[str] = None) -> int:
        """
        Remove empty directories from the source directory.
        
        Args:
            source_dir: Directory to clean
            
        Returns:
            Number of folders deleted
        """
        source_dir = Path(source_dir or self.config["source_directory"])
        deleted_count = 0
        
        for folder in source_dir.rglob("*"):
            if folder.is_dir() and not list(folder.iterdir()):
                try:
                    folder.rmdir()
                    self.logger.debug(f"Deleted empty folder: {folder}")
                    deleted_count += 1
                except Exception as e:
                    self.logger.error(f"Error deleting folder {folder}: {str(e)}")
        
        return deleted_count


def main():
    """Main entry point for the file organizer."""
    organizer = FileOrganizer()
    
    print("\n" + "="*50)
    print("Automated File Organizer")
    print("="*50 + "\n")
    print("Select organization method:")
    print("1. Organize by file type (extension)")
    print("2. Organize by date")
    print("3. Organize by file size")
    print("4. Exit")
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    if choice == "1":
        stats = organizer.organize_files()
    elif choice == "2":
        stats = organizer.organize_by_date()
    elif choice == "3":
        stats = organizer.organize_by_size()
    elif choice == "4":
        print("Exiting...")
        return
    else:
        print("Invalid choice")
        return
    
    # Print results
    print("\n" + "="*50)
    print("Organization Results:")
    print("="*50)
    print(f"Total files: {stats.get('total_files', 0)}")
    print(f"Organized files: {stats.get('organized_files', 0)}")
    print(f"Failed files: {stats.get('failed_files', 0)}")
    
    # Show categories/periods/sizes
    if 'categories' in stats:
        print("\nFiles by category:")
        for category, count in stats['categories'].items():
            print(f"  {category}: {count}")
    elif 'periods' in stats:
        print("\nFiles by date:")
        for period, count in stats['periods'].items():
            print(f"  {period}: {count}")
    elif 'sizes' in stats:
        print("\nFiles by size:")
        for size, count in stats['sizes'].items():
            print(f"  {size}: {count}")
    
    print("\n" + "="*50 + "\n")


if __name__ == "__main__":
    main()
