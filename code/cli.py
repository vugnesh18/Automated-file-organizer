"""
Command-line interface for the Automated File Organizer.
"""

import argparse
import sys
import json
from pathlib import Path
from file_organizer import FileOrganizer


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Automated File Organizer - Organize your files intelligently",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cli.py --organize type              # Organize by file type
  python cli.py --organize date              # Organize by date
  python cli.py --organize size              # Organize by file size
  python cli.py --path ~/Downloads --move    # Move files instead of copying
  python cli.py --cleanup                    # Remove empty folders
  python cli.py --config custom_config.json  # Use custom configuration
        """
    )
    
    parser.add_argument(
        "--organize",
        choices=["type", "date", "size"],
        help="Organization method to use"
    )
    
    parser.add_argument(
        "--path",
        type=str,
        default=".",
        help="Path to the directory to organize (default: current directory)"
    )
    
    parser.add_argument(
        "--config",
        type=str,
        default="config.json",
        help="Path to configuration file (default: config.json)"
    )
    
    parser.add_argument(
        "--move",
        action="store_true",
        help="Move files instead of copying them"
    )
    
    parser.add_argument(
        "--cleanup",
        action="store_true",
        help="Remove empty directories after organization"
    )
    
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without actually organizing files"
    )
    
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Run in interactive mode"
    )
    
    parser.add_argument(
        "--create-default-config",
        action="store_true",
        help="Create a default configuration file"
    )
    
    args = parser.parse_args()
    
    # Handle create default config
    if args.create_default_config:
        create_default_config()
        return
    
    # Create organizer instance
    try:
        organizer = FileOrganizer(args.config)
        
        # Update config if --move flag is set
        if args.move:
            organizer.config["move_files"] = True
        
        # Validate path
        path = Path(args.path)
        if not path.exists():
            print(f"Error: Directory '{args.path}' does not exist.")
            sys.exit(1)
        
        # Handle interactive mode
        if args.interactive:
            run_interactive(organizer, str(path))
        else:
            # Handle dry-run
            if args.dry_run:
                print("[DRY RUN MODE] No files will be organized.\n")
            
            # Organize files
            if args.organize == "type":
                print(f"Organizing files by type in '{args.path}'...")
                stats = organizer.organize_files(str(path))
            elif args.organize == "date":
                print(f"Organizing files by date in '{args.path}'...")
                stats = organizer.organize_by_date(str(path))
            elif args.organize == "size":
                print(f"Organizing files by size in '{args.path}'...")
                stats = organizer.organize_by_size(str(path))
            else:
                # Default to type organization
                print(f"Organizing files by type in '{args.path}'...")
                stats = organizer.organize_files(str(path))
            
            # Print results
            print_results(stats)
            
            # Handle cleanup
            if args.cleanup:
                print("\nCleaning up empty folders...")
                deleted = organizer.cleanup_empty_folders(str(path))
                print(f"Deleted {deleted} empty folder(s)")
    
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)


def run_interactive(organizer: FileOrganizer, default_path: str) -> None:
    """Run the organizer in interactive mode."""
    print("\n" + "="*60)
    print("AUTOMATED FILE ORGANIZER - INTERACTIVE MODE")
    print("="*60 + "\n")
    
    while True:
        print("Main Menu:")
        print("1. Organize files by type (extension)")
        print("2. Organize files by date")
        print("3. Organize files by file size")
        print("4. Clean up empty folders")
        print("5. View current configuration")
        print("6. Exit")
        
        choice = input("\nSelect option (1-6): ").strip()
        
        if choice == "1":
            stats = organizer.organize_files(default_path)
            print_results(stats)
        
        elif choice == "2":
            stats = organizer.organize_by_date(default_path)
            print_results(stats)
        
        elif choice == "3":
            stats = organizer.organize_by_size(default_path)
            print_results(stats)
        
        elif choice == "4":
            deleted = organizer.cleanup_empty_folders(default_path)
            print(f"\nDeleted {deleted} empty folder(s)")
        
        elif choice == "5":
            print("\nCurrent Configuration:")
            print(json.dumps(organizer.config, indent=2))
        
        elif choice == "6":
            print("\nThank you for using Automated File Organizer!")
            break
        
        else:
            print("Invalid option. Please try again.")
        
        print()


def print_results(stats: dict) -> None:
    """Print formatted results of the organization."""
    print("\n" + "="*60)
    print("ORGANIZATION RESULTS")
    print("="*60)
    
    if "status" in stats and stats["status"] == "error":
        print(f"Error: {stats.get('message', 'Unknown error')}")
        return
    
    print(f"Total files processed: {stats.get('total_files', 0)}")
    print(f"Successfully organized: {stats.get('organized_files', 0)}")
    print(f"Failed to organize: {stats.get('failed_files', 0)}")
    
    # Print categories/periods/sizes
    if 'categories' in stats and stats['categories']:
        print("\nBreakdown by category:")
        for category, count in sorted(stats['categories'].items()):
            print(f"  • {category}: {count} file(s)")
    
    elif 'periods' in stats and stats['periods']:
        print("\nBreakdown by date:")
        for period, count in sorted(stats['periods'].items()):
            print(f"  • {period}: {count} file(s)")
    
    elif 'sizes' in stats and stats['sizes']:
        print("\nBreakdown by size:")
        for size, count in sorted(stats['sizes'].items()):
            print(f"  • {size}: {count} file(s)")
    
    print("="*60 + "\n")


def create_default_config() -> None:
    """Create a default configuration file."""
    config_path = Path("config.json")
    
    if config_path.exists():
        response = input("config.json already exists. Overwrite? (y/n): ").strip().lower()
        if response != 'y':
            print("Cancelled.")
            return
    
    organizer = FileOrganizer()
    default_config = organizer._get_default_config()
    
    with open(config_path, 'w') as f:
        json.dump(default_config, f, indent=2)
    
    print(f"Created default configuration in {config_path}")


if __name__ == "__main__":
    main()
