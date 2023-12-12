from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import time

def action():
    print("Action function called at", datetime.now())

def schedule_daily_action(hour, minute):
    scheduler = BackgroundScheduler()
    scheduler.add_job(action, 'cron', hour=hour, minute=minute)
    scheduler.start()
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

