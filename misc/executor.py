from redis import Redis
from rq import get_current_job, Worker, Connection, Queue
from rq_worker_playground import test_rq

queue = Queue("someWorker", connection=Redis.from_url('redis://'))
queue.enqueue(test_rq.example, 23)
