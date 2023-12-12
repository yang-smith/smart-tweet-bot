from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import time
from tweet import tweet_post


scheduler = BackgroundScheduler()
job = None
content_file = 'contents.txt'  # 定义内容存储的文件名

def load_contents():
    with open(content_file, 'r') as file:
        return file.read().splitlines()

def append_content(new_content):
    with open(content_file, 'a') as file:
        file.write(new_content + '\n')

def action():
    print("Action function called at", datetime.now())
    contents = load_contents()
    if contents:
        content = contents.pop(0)
        tweet_post(content)
        print(content)
        with open(content_file, 'w') as file:
            file.writelines('\n'.join(contents) + '\n')
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

