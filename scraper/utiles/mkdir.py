import os

def mkdir(path: str): 

	if not os.path.exists(path):
		os.makedirs(path)
		print(f"Folder created: {path}")
	else:
		print(f"Folder already exists: {path}")