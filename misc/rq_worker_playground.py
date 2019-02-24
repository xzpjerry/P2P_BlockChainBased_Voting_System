# Example work/job
import time
from redis import Redis
from rq import get_current_job, Worker, Connection, Queue

class test_rq:

    @classmethod
    def example(self, seconds):
        job = get_current_job()
        print('Starting task')
        for i in range(seconds):
            job.meta['progress'] = 100.0 * i / seconds
            job.save_meta()
            print(i)
            time.sleep(1)
        job.meta['progress'] = 100
        job.save_meta()
        print('Task completed')
