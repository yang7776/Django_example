from apscheduler.schedulers.blocking import BlockingScheduler

def job():
    print('job 3s')

if __name__=='__main__':
    sched = BlockingScheduler(timezone='Asia/Shanghai')
    sched.add_job(job, 'interval', id='3_second_job', seconds=3)
    sched.start()