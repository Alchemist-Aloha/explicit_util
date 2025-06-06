from .convert_pic_to_webp import convert_pic_to_webp_multithreaded
from .nfo_tool import generate_nfo
from .recursive_namer import process_video_files
from .recursive_unzip import recursive_unzip
from .remove_empty import remove_empty_folders
from .whisper_cpp_transcribe import transcribe_videos
from .zip_and_move import async_zip_and_move
from .group_files import group_files_by_string, move_grouped_files
import importlib.resources
import os
from pathlib import Path
import asyncio
import toml

__docformat__ = "google"
def choice1() -> None:
    """Convert images to WebP format."""
    config_path = Path(str(importlib.resources.files('ExplicitUtil').joinpath('config/convert_pic_to_webp.toml')))
    config_path.parent.mkdir(parents=True, exist_ok=True)
    default_config = {"num_threads": 6, "timeout": 10, "quality": 80}
    use_config = False
    # Load configuration from file if available
    if config_path.is_file():
        use_config = input("Use stored config for settings? (y/n): ").strip().lower() == "y"
        if use_config:
            # Load the config file
            try:
                config = toml.load(config_path)
                default_config.update({k: config.get(k, v) for k, v in default_config.items()})

            except Exception as e:
                print(f"Error loading config file: {e}")
                return
            
    if not config_path.is_file() or not use_config:
        print("Config file not found. Using manual input.")
        # Prompt for settings if not using config
        for key, default in default_config.items():
            value = input(f"Enter {key.replace('_', ' ')} (default: {default}): ").strip()
            if value:
                try:
                    default_config[key] = int(value)
                except ValueError:
                    print(f"Invalid input for {key}. Using default: {default}.")
        with open(config_path, "w") as config_file:
            toml.dump(default_config, config_file)
            print(f"Config saved to {config_path}")
    folder_path = input("Enter the folder path to convert picture files: ").strip('"')
    if not Path(folder_path).exists():
        print(f"Error: Folder '{folder_path}' does not exist.")
        return

    try:
        convert_pic_to_webp_multithreaded(
            folder_path=folder_path,
            num_threads=default_config["num_threads"],
            timeout=default_config["timeout"],
            quality=default_config["quality"],
        )
    except Exception as e:
        print(f"Error converting files: {e}")

def choice2() -> None:
    """generate nfo files"""
    media_path = input("Enter the media directory path: ")
    if not Path(media_path).exists():
        print(f"Error: Media directory '{media_path}' does not exist.")
        return
    media_type = input("Enter the media type (movie, episode, musicvideo): ")
    output_dir = input("Enter the output directory path: ")
    if not Path(output_dir).exists():
        print(f"Output directory '{output_dir}' does not exist. Makeing it now.")
        try:
            os.makedirs(output_dir)
        except Exception as e:
            print(f"Error creating output directory: {e}")
            return
    try:
        generate_nfo(media_path, media_type, output_dir)
        return
    except Exception as e:
        print(f"Error generating NFO files: {e}")
        return
    

def choice3() -> None:
    """process video files"""
    NAMER_CONFIG_DEFAULT = str(importlib.resources.files('ExplicitUtil').joinpath('config/.namer.cfg'))
    default_config = {"namer_config_path":NAMER_CONFIG_DEFAULT,"suffix": (".m4v", ".mp4"), "endswith": ""}
    # Load configuration from file if available
    config_path = Path(str(importlib.resources.files('ExplicitUtil').joinpath('config/recursive_namer.toml')))
    use_config = False
    if Path(config_path).is_file():
        use_config = input("Use stored config for settings? (y/n): ").strip().lower() == "y"
        if use_config:
            try:
                config = toml.load(config_path)
                default_config.update({k: config.get(k, v) for k, v in default_config.items()})
            except Exception as e:
                print(f"Error loading config file: {e}")
                return
    if not Path(config_path).is_file() or not use_config:
        print("Config file not found. Using manual input.")
        # Prompt for settings if not using config

        for key, default in default_config.items():
            if key == "endswith":
                print("Enter NOT case sensitive endswith string (e.g., _1080p_WEBDL):")
            if key == "suffix":
                print("Enter NOT case sensitive suffix strings split with comma (e.g., .m4v,.mp4):")
            print("Enter 'default' to use default value")
            value = input(f"Enter {key.replace('_', ' ')} (default: {default}): ").strip()
            if value == "default":
                value = default_config[key]
            if value:
                if key == "suffix" and value is str:
                    value = tuple(ext.strip() for ext in value.split(","))
                default_config[key] = value
        if not Path(default_config["namer_config_path"]).is_file():
            print(f"Error: Configuration file '{default_config['namer_config_path']}' not found.")
            return
        with open(config_path, "w") as config_file:
            toml.dump(default_config, config_file)
            print(f"Config saved to {config_path}")
    # print(NAMER_CONFIG_DEFAULT)
    folder_path = Path(
        input("Enter the folder path to video files: ").strip('"').strip("'")  # remove quotes
    )  # replace with your directory.
    if not folder_path.is_dir():
        print(f"Error: Directory '{folder_path}' not found.")
        return

    try:
        process_video_files(root_dir=folder_path, namer_config=default_config['namer_config_path'], suffix=default_config["suffix"], endswith=default_config["endswith"])
        return
    except Exception as e:
        print(f"Error processing video files: {e}")
        return

def choice4() -> None:
    """unzip files recursively"""
    folder_path = Path(input("Enter the folder path to unzip files: ").strip('"'))
    delete_zips = input("Delete ZIP archives after unzipping? (y/n): ").strip().lower()=='y'

    if not folder_path.exists():
        print(f"Error: Folder '{folder_path}' does not exist.")
        return

    try:
        recursive_unzip(folder_path, delete_zips)
        return
    except Exception as e:
        print(f"Error unzipping files: {e}")
        return


def choice5() -> None:
    """remove empty folders"""
    target_dir = input("Please enter the target directory: ").strip("\"")
    dry_run = input("Do you want to perform a dry run? (y/n): ").strip().lower() == 'y'
    
    if not Path(target_dir).exists():
        print(f"Error: Folder '{target_dir}' does not exist.")
        return
    
    try:
        remove_empty_folders(target_dir, dry_run)
        return
    except Exception as e:
        print(f"Error removing empty folders: {e}")
        return


def choice6() -> None:
    """transcribe videos with Whisper.cpp"""
    config_path = Path(str(importlib.resources.files('ExplicitUtil').joinpath('config/whisper_cpp_transcribe.toml')))
    config_path.parent.mkdir(parents=True, exist_ok=True)
    default_config = {"whisper_root": "", "suffix": (".m4v", ".mp4"), "prompt": ""}
    use_config = False
    # Load configuration from file if available
    if config_path.is_file():
        use_config = input("Use stored config for settings? (y/n): ").strip().lower() == "y"
        if use_config:
            try:
                config = toml.load(config_path)
                default_config.update({k: config.get(k, v) for k, v in default_config.items()})           
            except Exception as e:
                print(f"Error loading config file: {e}")
                return
    if not config_path.is_file() or not use_config:
        print("Using manual input.")
        # Prompt for settings if not using config
        for key, default in default_config.items():
            if key == "whisper_root":
                print("Enter the path to the whisper.cpp root directory ():")
            if key == "prompt":
                print("Enter the prompt for Whisper transcription:")
            if key == "suffix":
                print("Enter NOT case sensitive suffix strings split with comma (e.g., .m4v,.mp4):")
            print("Enter 'default' to use default value")
            value = input(f"Enter {key.replace('_', ' ')} (default: {default}): ").strip()
            if value == "default":
                value = default_config[key]
            if value:
                if key == "suffix" and value is str:
                    value = tuple(ext.strip() for ext in value.split(","))
                default_config[key] = value
        if not Path(default_config["whisper_root"]).is_dir():
            print(f"Error: Directory '{default_config['whisper_root']}' not found.")
            return
        with open(config_path, "w") as config_file:
            toml.dump(default_config, config_file)
            print(f"Config saved to {config_path}")
    input_folder= input("Enter the folder path to video files: ").strip('"')
    transcribe_videos(input_folder, default_config["whisper_root"], prompt=default_config["prompt"], suffix=default_config["suffix"])
    return



def choice7() -> None:
    """zip and move folders"""
    source_folder = Path(input("Enter the source folder path: ").strip("\""))
    if not source_folder.is_dir():
        print(f"The folder '{source_folder}' does not exist.")
        return
    destination_folder = Path(input("Enter the destination folder path: "))
    if not destination_folder.is_dir():
        print(f"The folder '{destination_folder}' does not exist.")
        destination_folder.mkdir(parents=True, exist_ok=True)
    try:
        asyncio.run(async_zip_and_move(source_folder, destination_folder))
        return
    except Exception as e:
        print(f"Error zipping and moving folders: {e}")
        return

def choice8() -> None:
    """group files by regex matching"""
    directory = Path(input("Enter the directory path: ").strip('"'))
    print("Default regex pattern: r'(\d{4}-\d{2}-\d{2})'")
    custom_regex = input("Do you want to use a custom regex pattern? (y/n): ").strip().lower() == 'y'
    if custom_regex:
        regex_pattern = input("Enter the regex pattern to match: ").strip('"')
    else:
        regex_pattern = r"(\d{4}-\d{2}-\d{2})"
    grouped_files = group_files_by_string(directory, regex_pattern)
    for key, files in grouped_files.items():
        print(f"{key}: {files}")
    proceed = input("Do you want to move the files to their respective directories? (y/n): ").strip().lower() == 'y'
    if proceed:
        move_grouped_files(directory, grouped_files)

def main() -> None:
    while True:
        print("ExplicitUtil CLI")
        print("1. Convert images to WebP")
        print("2. Generate NFO files")
        print("3. Batch rename video files with namer")
        print("4. Unzip files recursively")
        print("5. Remove empty folders")
        print("6. Transcribe videos with Whisper.cpp")
        print("7. Zip and move folders")
        print("8. Group files by regex matching")
        print("Type 'exit' to quit the program.")

        choice = input("Choose an option (1-7): ")
        if choice.lower() == "exit":
            print("Exiting...")
            break
        try:
            choice = int(choice)
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 7.")
            continue

        if choice == 1:
            choice1()
        elif choice == 2:
            choice2()
        elif choice == 3:
            choice3()
        elif choice == 4:
            choice4()
        elif choice == 5:
            choice5()
        elif choice == 6:
            choice6()
        elif choice == 7:
            choice7()
        else:
            print("Invalid choice. Please try again.")
            continue

if __name__ == "__main__":
    main()
