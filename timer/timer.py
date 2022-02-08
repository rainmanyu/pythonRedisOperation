import time
from timeloop import Timeloop
from datetime import timedelta
import jsonUtil
import config.constants

tl = Timeloop()


# @tl.job(interval=timedelta(seconds=2))
# def sample_job_every_2s():
#     print("2s job current time : {}".format(time.ctime()))
#
#
# @tl.job(interval=timedelta(seconds=5))
# def sample_job_every_5s():
#     print("5s job current time : {}".format(time.ctime()))


@tl.job(interval=timedelta(minutes=config.constants.c_job_interval_minutes))
def job_work():
    jsonUtil.update_versions()
