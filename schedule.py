from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import time
from tweet import tweet_post

content_list = []
scheduler = BackgroundScheduler()
job = None

def action():
    print("Action function called at", datetime.now())
    if content_list:
        content = content_list.pop(0)
        tweet_post(content)
        print(content)
    else:
        print("list is empty.")
    

def schedule_daily_action(hour, minute):
    global job
    job = scheduler.add_job(action, 'cron', hour=hour, minute=minute)
    scheduler.start()
    print(f"Action scheduled for every day at {hour}:{minute}")

def reset_time(time):
    hour, minute = time.split(':')
    global job
    if job is None:
        schedule_daily_action(int(hour),int(minute))
    else:
        scheduler.reschedule_job(job.id, trigger='cron', hour=int(hour), minute=int(minute))
        print(f"Action scheduled for every day at {hour}:{minute}")



# 调度 action 函数在每天的 12:20 执行
# schedule_daily_action(12, 23)

# # 为了保持程序运行，防止退出
# try:
#     # This is here to simulate application activity (which keeps the main thread alive).
#     while True:
#         time.sleep(2)
# except (KeyboardInterrupt, SystemExit):
#     # Not strictly necessary if daemonic mode is enabled but should be done if possible
#     # scheduler.shutdown()
#     print("done")

