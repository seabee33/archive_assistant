import os, glob, hashlib, json
from dotenv import load_dotenv
load_dotenv()

path_to_scan = os.getenv("DIRECTORY")
scanfile_path = "scan_file.json"
print(f"Path: {path_to_scan}")

def get_file_hash(file_path):
	sha256_hash = hashlib.sha256()
	with open(file_path, "rb") as f:
		for byteblock in iter(lambda: f.read(4096), b""):
			sha256_hash.update(byteblock)
	return sha256_hash.hexdigest()

def check_if_scanfile_exists(file_path):
	if os.path.exists(file_path):
		if os.path.getsize(file_path) > 0:
			print("Scan file exists and has data")
			return 1
		else:
			print("Scan file exists but has no data")
			return 2
	else:
		print("Scan file not found")
		return 3


def get_files_list(path_to_scan, custom_folder_name):
	# Get all items in a directory
	files_object = glob.glob(f"{path_to_scan}/**/*", recursive=True)

	# Make a list of only the files
	files_and_hashes = {
		item: get_file_hash(item)
		for item in files_object if os.path.isfile(item)
	}

	return files_and_hashes

def compare_scans(previous_scan, current_scan):
	changes = []
	for file, file_hash in current_scan.items():
		if file in previous_scan:
			if file_hash != previous_scan[file]:
				changes.append(f"WARN: Different hash for {file}")
				changes.append(f"Previous hash: {previous_scan[file]}")
				changes.append(f"New Hash: {file_hash}")
		else:
			changes.append(f"New File: {file}")
	
	for file in previous_scan:
		if file not in current_scan:
			changes.append(f"Deleted file: {file}")
	
	return changes


def main():
	scanfile_status = check_if_scanfile_exists(scanfile_path)
	current_scan = get_files_list(path_to_scan, "test_folder")

	if scanfile_status == 1:
		with open(scanfile_path, "r") as f:
			stored_data = json.load(f)
		
		if path_to_scan in stored_data:
			previous_scan = stored_data[path_to_scan]["files_and_hashes"]
			changes = compare_scans(previous_scan, current_scan)
			
			if changes:
				print("Changes detected\n")
				for change in changes:
					print(f"{change}")
			else:
				print("All ok, No changes detected")
		else:
			print(f"New directory scanned: {path_to_scan}")
			stored_data[path_to_scan] = {
				"custom_name_given_by_user": os.path.basename(path_to_scan),
				"files_and_hashes": current_scan
			}
	elif scanfile_status in [2, 3]:
		print("Creating new scanfile")
		stored_data = {}
		stored_data[path_to_scan] = {
			"custom_name_given_by_user": os.path.basename(path_to_scan),
			"files_and_hashes": current_scan
		}
	
	if path_to_scan in stored_data:
		for file, file_hash in current_scan.items():
			if file not in stored_data[path_to_scan]["files_and_hashes"]:
				stored_data[path_to_scan]["files_and_hashes"][file] = file_hash
	
	with open(scanfile_path, "w") as f:
		json.dump(stored_data, f, indent=4)
	
	print("Finished")


main()
