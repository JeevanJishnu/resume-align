import os
import time
import requests
import logging
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime, timedelta

# Setup Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("CV-Watcher")

# Configuration
WATCH_DIR = "input"
DONE_DIR = os.path.join("output", "done")
REVIEW_DIR = os.path.join("output", "review")
API_URL = "http://localhost:8000/process"
RATE_LIMIT_SECONDS = 5 # Reduced for demo processing speed

# Ensure directories exist
os.makedirs(DONE_DIR, exist_ok=True)
os.makedirs(REVIEW_DIR, exist_ok=True)

class CVHandler(FileSystemEventHandler):
    def __init__(self):
        self.last_processed_time = datetime.min
        self.processed_count = 0
        self.start_time = datetime.now()

    def on_created(self, event):
        if event.is_directory:
            return
        
        file_path = event.src_path
        file_ext = os.path.splitext(file_path)[1].lower()
        
        if file_ext in ['.pdf', '.png', '.jpg', '.jpeg']:
            logger.info(f"New CV detected: {os.path.basename(file_path)}")
            self.process_file(file_path)

    def process_file(self, file_path):
        # 1. Rate Limiting
        time_since_last = (datetime.now() - self.last_processed_time).total_seconds()
        if time_since_last < RATE_LIMIT_SECONDS:
            wait_time = int(RATE_LIMIT_SECONDS - time_since_last)
            logger.warning(f"Rate limit active. Waiting {wait_time}s before processing {os.path.basename(file_path)}")
            time.sleep(wait_time)

        # 2. Check if file is still being written (for large files)
        file_size = -1
        while file_size != os.path.getsize(file_path):
            file_size = os.path.getsize(file_path)
            time.sleep(1)

        try:
            logger.info(f"Uploading {os.path.basename(file_path)} to FastAPI backend...")
            with open(file_path, 'rb') as f:
                files = {'file': (os.path.basename(file_path), f, 'application/octet-stream')}
                response = requests.post(API_URL, files=files)
            
            if response.status_code == 200:
                result = response.json()
                status = result.get('status', 'review')
                confidence = result.get('confidence_score', 0)
                
                logger.info(f"Successfully processed {os.path.basename(file_path)} | Status: {status} | Confidence: {confidence:.2f}")
                
                # Move to appropriate directory
                target_dir = DONE_DIR if status == 'auto' else REVIEW_DIR
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                new_name = f"{timestamp}_{os.path.basename(file_path)}"
                shutil.move(file_path, os.path.join(target_dir, new_name))
                
                self.processed_count += 1
                self.last_processed_time = datetime.now()
                self.log_stats()
            else:
                logger.error(f"Backend error ({response.status_code}): {response.text}")
        
        except requests.exceptions.ConnectionError:
            logger.error("Could not connect to FastAPI server. Is it running on port 8000?")
        except Exception as e:
            logger.error(f"Error processing {file_path}: {str(e)}")

    def log_stats(self):
        uptime = datetime.now() - self.start_time
        hours = uptime.total_seconds() / 3600
        rate = self.processed_count / hours if hours > 0 else self.processed_count
        logger.info(f"Stats: Total Processed: {self.processed_count} | Average Rate: {rate:.2f} CVs/hour")

if __name__ == "__main__":
    event_handler = CVHandler()
    observer = Observer()
    observer.schedule(event_handler, WATCH_DIR, recursive=False)
    
    logger.info(f"Starting CV Watcher on folder: {os.path.abspath(WATCH_DIR)}")
    logger.info("Listening for PDF/PNG/JPG files...")
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Stopping watcher...")
        observer.stop()
    observer.join()
