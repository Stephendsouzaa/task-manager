import os
import argparse
import mutagen
from mutagen.mp3 import MP3
from mutagen.id3 import ID3NoHeaderError

def list_music_files(directory):
    """List all music files in the given directory and its subdirectories."""
    music_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(('.mp3', '.wav', '.flac', '.aac')):
                music_files.append(os.path.join(root, file))
    return music_files

def show_metadata(file):
    """Show metadata for a given music file."""
    try:
        audio = MP3(file)
        metadata = {
            "File": file,
            "Song": audio.get('TIT2', 'Unknown'),
            "Artist": audio.get('TPE1', 'Unknown'),
            "Album": audio.get('TALB', 'Unknown'),
        }
        return metadata
    except (ID3NoHeaderError, Exception) as e:
        print(f"Error reading metadata for {file}: {e}")
        return None

def group_by(music_files, key):
    """Group music files by artist, album, or both."""
    grouped = {}
    for file in music_files:
        try:
            audio = MP3(file)
            artist = audio.get('TPE1', 'Unknown')
            album = audio.get('TALB', 'Unknown')
            if key == 'ARTIST':
                grouped.setdefault(artist, []).append(file)
            elif key == 'ALBUM':
                grouped.setdefault(album, []).append(file)
            elif key == 'ARTIST_ALBUM':
                grouped.setdefault(artist, {}).setdefault(album, []).append(file)
        except Exception as e:
            print(f"Error grouping {file}: {e}")
    return grouped

def print_grouped_files(grouped_files):
    """Print grouped files in a structured format."""
    for key, files in grouped_files.items():
        if isinstance(files, dict):
            print(f"{key}")
            print_grouped_files(files)
        else:
            print(f"├── {key}")
            for file in files:
                print(f"│   └── {os.path.basename(file)}")

def reorganize_files_dry_run(music_files, key):
    """Dry run for reorganizing files based on the given key."""
    changes = []
    for file in music_files:
        try:
            audio = MP3(file)
            artist = audio.get('TPE1', 'Unknown')
            album = audio.get('TALB', 'Unknown')
            if key == 'ARTIST':
                new_path = os.path.join(os.path.dirname(file), artist, os.path.basename(file))
                changes.append(f"{file} ---> {new_path}")
            elif key == 'ALBUM':
                new_path = os.path.join(os.path.dirname(file), album, os.path.basename(file))
                changes.append(f"{file} ---> {new_path}")
            elif key == 'ARTIST_ALBUM':
                new_path = os.path.join(os.path.dirname(file), artist, album, os.path.basename(file))
                changes.append(f"{file} ---> {new_path}")
        except Exception as e:
            print(f"Error processing {file}: {e}")
    return changes

def reorganize_files(music_files, key):
    """Reorganize files based on the given key."""
    for file in music_files:
        try:
            audio = MP3(file)
            artist = audio.get('TPE1', 'Unknown')
            album = audio.get('TALB', 'Unknown')
            if key == 'ARTIST':
                new_dir = os.path.join(os.path.dirname(file), artist)
            elif key == 'ALBUM':
                new_dir = os.path.join(os.path.dirname(file), album)
            elif key == 'ARTIST_ALBUM':
                new_dir = os.path.join(os.path.dirname(file), artist, album)

            os.makedirs(new_dir, exist_ok=True)
            new_path = os.path.join(new_dir, os.path.basename(file))
            os.rename(file, new_path)
            print(f"Moved {file} ---> {new_path}")
        except Exception as e:
            print(f"Error moving {file}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Music Library Manager")
    parser.add_argument('--input', type=str, required=True, help="Path to the music folder")
    parser.add_argument('--list-files', action='store_true', help="List all music files")
    parser.add_argument('--show-metadata', action='store_true', help="Show metadata of music files")
    parser.add_argument('--group-by', type=str, choices=['ARTIST', 'ALBUM', 'ARTIST_ALBUM'], help="Group music files")
    parser.add_argument('--reorganize-by', type=str, choices=['ARTIST', 'ALBUM', 'ARTIST_ALBUM'], help="Reorganize files")
    parser.add_argument('--dry-run', action='store_true', help="Show what would be reorganized without moving files")

    args = parser.parse_args()

    music_files = list_music_files(args.input)

    if args.list_files:
        for file in music_files:
            print(os.path.basename(file))

    if args.show_metadata:
        for file in music_files:
            metadata = show_metadata(file)
            if metadata:
                print(f"____________________")
                for key, value in metadata.items():
                    print(f"{key}: {value}")
                print(f"____________________")

    if args.group_by:
        grouped_files = group_by(music_files, args.group_by)
        print_grouped_files(grouped_files)

    if args.reorganize_by:
        if args.dry_run:
            changes = reorganize_files_dry_run(music_files, args.reorganize_by)
            print("The following changes will be made to your library:")
            for change in changes:
                print(change)
        else:
            reorganize_files(music_files, args.reorganize_by)

if __name__ == "__main__":
    main()
