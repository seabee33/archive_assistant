import os, glob, hashlib
from dotenv import load_dotenv
load_dotenv()

path = os.getenv("DIRECTORY")
print(f"Path: ")

def get_file_hash(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byteblock in _iter(lambda: f.read(4096), b""):
            sha256_hash.update(byteblock)
    return sha256_hash.hexdigest()


def get_
files_list = glob.glob(f"{path}/**/*", recursive=True)

for file in files_list:
	print(file)


