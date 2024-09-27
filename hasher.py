import os, glob, hashlib
from dotenv import load_dotenv
load_dotenv()

path_to_scan = os.getenv("DIRECTORY")
print(f"Path: {path_to_scan}")

def get_file_hash(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byteblock in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byteblock)
    return sha256_hash.hexdigest()


def get_files_list(path_to_scan):
	files_list = glob.glob(f"{path_to_scan}/**/*", recursive=True)

	for file in files_list:
		if os.path.isfile(file):
			file_hash = get_file_hash(file)
			print(f"File: {file} - {file_hash}")


get_files_list(path_to_scan)
