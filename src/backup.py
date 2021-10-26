import time
import pickle
from src.data_store import data_store


INTERVAL = 10 # Backup interval in seconds

def interval_backup():
	store = data_store.get()
	print("Starting object:")
	print(store)
	while True:
		print("=== Backing up data ===")
		store = data_store.get()
		file = open("data.p", "wb")
		pickle.dump(store, file)
		file.close()
		time.sleep(INTERVAL)
