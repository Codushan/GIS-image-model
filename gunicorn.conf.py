# Gunicorn configuration for free tier Render
import multiprocessing

# Extended timeout for model loading
timeout = 300  # 5 minutes

# Single worker to save memory
workers = 1

# Use threading for concurrency without extra memory
worker_class = 'gthread'
threads = 2

# Preload to load model once, not per worker
preload_app = True

# Use shared memory for temporary files
worker_tmp_dir = '/dev/shm'

# Memory limits
max_requests = 100  # Restart worker after 100 requests to prevent memory leaks
max_requests_jitter = 10

# Logging
accesslog = '-'
errorlog = '-'
loglevel = 'info'