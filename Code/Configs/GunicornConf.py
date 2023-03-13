import multiprocessing

from gevent import monkey
monkey.patch_all()


worker_class = "gevent"
workers = multiprocessing.cpu_count() * 2 + 1
threads = multiprocessing.cpu_count() * 2
preload_app = True
worker_connections = 1000
timeout = 600
