"""
Unit tests for the File Organizer application.

Note: To run these tests, install pytest:
    pip install pytest

Then run:
    pytest test_file_organizer.py -v
"""

import unittest
import tempfile
import shutil
from pathlib import Path
import json
from file_organizer import FileOrganizer


class TestFileOrganizer(unittest.TestCase):
    """Test suite for FileOrganizer class."""
    
    def setUp(self):
        """Create a temporary directory for testing."""
        self.test_dir = tempfile.mkdtemp()
        self.config_path = Path(self.test_dir) / "test_config.json"
        
        # Create a default config in the test directory
        default_config = {
            "source_directory": self.test_dir,
            "organize_by": "extension",
            "create_subdirectories": True,
            "move_files": False,
            "rules": {
                "documents": [".pdf", ".txt", ".docx"],
                "images": [".jpg", ".png"],
                "videos": [".mp4"],
                "archives": [".zip"]
            }
        }
        
        with open(self.config_path, 'w') as f:
            json.dump(default_config, f)
        
        self.organizer = FileOrganizer(str(self.config_path))
    
    def tearDown(self):
        """Remove the temporary directory after tests."""
        if Path(self.test_dir).exists():
            shutil.rmtree(self.test_dir)
    
    def create_test_files(self):
        """Create test files with various extensions."""
        test_files = {
            "document1.txt": "sample text",
            "document2.pdf": "pdf content",
            "image1.jpg": "image data",
            "image2.png": "png data",
            "video1.mp4": "video data",
            "archive1.zip": "zip data"
        }
        
        for filename, content in test_files.items():
            filepath = Path(self.test_dir) / filename
            filepath.write_text(content)
        
        return len(test_files)
    
    def test_categorize_file(self):
        """Test file categorization by extension."""
        test_cases = [
            ("document.txt", "documents"),
            ("image.jpg", "images"),
            ("video.mp4", "videos"),
            ("archive.zip", "archives"),
            ("unknown.xyz", None),
        ]
        
        for filename, expected_category in test_cases:
            file_path = Path(self.test_dir) / filename
            file_path.touch()
            
            category = self.organizer._categorize_file(file_path)
            
            if expected_category:
                self.assertEqual(category, expected_category,
                               f"Failed to categorize {filename}")
            
            file_path.unlink()
    
    def test_organize_files_by_type(self):
        """Test organizing files by type."""
        num_files = self.create_test_files()
        
        stats = self.organizer.organize_files(self.test_dir)
        
        self.assertEqual(stats['total_files'], num_files)
        self.assertGreater(stats['organized_files'], 0)
        
        # Check that category folders were created
        self.assertTrue((Path(self.test_dir) / "documents").exists())
        self.assertTrue((Path(self.test_dir) / "images").exists())
    
    def test_organize_files_by_date(self):
        """Test organizing files by date."""
        self.create_test_files()
        
        stats = self.organizer.organize_by_date(self.test_dir)
        
        self.assertGreater(stats['organized_files'], 0)
        self.assertIn('periods', stats)
    
    def test_organize_files_by_size(self):
        """Test organizing files by size."""
        self.create_test_files()
        
        stats = self.organizer.organize_by_size(self.test_dir)
        
        self.assertGreater(stats['organized_files'], 0)
        self.assertIn('sizes', stats)
    
    def test_cleanup_empty_folders(self):
        """Test cleanup of empty directories."""
        # Create some empty directories
        empty_dir1 = Path(self.test_dir) / "empty1"
        empty_dir2 = Path(self.test_dir) / "empty2"
        empty_dir1.mkdir()
        empty_dir2.mkdir()
        
        deleted = self.organizer.cleanup_empty_folders(self.test_dir)
        
        self.assertGreaterEqual(deleted, 2)
        self.assertFalse(empty_dir1.exists())
        self.assertFalse(empty_dir2.exists())
    
    def test_duplicate_filename_handling(self):
        """Test handling of duplicate filenames."""
        # Create two files with the same name in source
        file1 = Path(self.test_dir) / "duplicate.txt"
        file1.write_text("first")
        
        # Organize first file
        self.organizer.organize_files(self.test_dir)
        
        # Create another file with same name
        file1.write_text("second")
        
        # Organize again - should handle duplicate
        stats = self.organizer.organize_files(self.test_dir)
        
        # Check that files were organized
        docs_dir = Path(self.test_dir) / "documents"
        if docs_dir.exists():
            files = list(docs_dir.glob("duplicate*"))
            self.assertGreaterEqual(len(files), 1)
    
    def test_invalid_directory(self):
        """Test handling of invalid directory path."""
        invalid_dir = "/invalid/path/that/does/not/exist"
        stats = self.organizer.organize_files(invalid_dir)
        
        self.assertEqual(stats['status'], 'error')
    
    def test_config_loading(self):
        """Test configuration loading."""
        config = self.organizer.config
        
        self.assertIn('rules', config)
        self.assertIn('documents', config['rules'])
        self.assertIn('images', config['rules'])
    
    def test_default_config(self):
        """Test default configuration generation."""
        default_config = self.organizer._get_default_config()
        
        self.assertIn('source_directory', default_config)
        self.assertIn('rules', default_config)
        self.assertIn('documents', default_config['rules'])
        self.assertIn('images', default_config['rules'])
        self.assertIn('videos', default_config['rules'])


class TestFileOrganizerIntegration(unittest.TestCase):
    """Integration tests for file organization."""
    
    def setUp(self):
        """Set up test environment."""
        self.test_dir = tempfile.mkdtemp()
        self.organizer = FileOrganizer()
        self.organizer.config['source_directory'] = self.test_dir
    
    def tearDown(self):
        """Clean up test environment."""
        if Path(self.test_dir).exists():
            shutil.rmtree(self.test_dir)
    
    def test_full_organization_workflow(self):
        """Test complete organization workflow."""
        # Create various test files
        files = {
            "report.pdf": "PDF content",
            "photo.jpg": "JPEG content",
            "notes.txt": "Text content",
            "movie.mp4": "Video content"
        }
        
        for filename, content in files.items():
            (Path(self.test_dir) / filename).write_text(content)
        
        # Organize by type
        stats = self.organizer.organize_files(self.test_dir)
        
        # Verify organization
        self.assertEqual(stats['total_files'], len(files))
        self.assertGreater(stats['organized_files'], 0)
        
        # Cleanup
        deleted = self.organizer.cleanup_empty_folders(self.test_dir)
        self.assertGreaterEqual(deleted, 0)


if __name__ == '__main__':
    unittest.main()
