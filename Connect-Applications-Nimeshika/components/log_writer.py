import os
import time
import datetime
import sys
import logging

import components.read_config_file as config_ini


def rename_previous_log_file(current_time, new_log_name, log_file_dir):
    """ rename existing log file with same date """

    new_log = os.path.join(log_file_location, new_log_name)

    if os.path.isfile(new_log):
        old_log_file = "{}_{}".format(new_log_name, current_time)
        src_file = os.path.join(log_file_dir, new_log_name)
        dest_file = os.path.join(log_file_dir, old_log_file)
        os.rename(src_file, dest_file)


ERROR = "\033[31m"
BLUE = "\033[34m"
CYAN = "\033[36m"
WARN = "\033[33m"
INFO = "\033[32m"
RESET = "\033[0m"

read_configs = config_ini.ReadConfig()
log_file_location = read_configs.get_one_option("PATHS", "log_path")

now_date_time = datetime.datetime.now()
now_date = str(now_date_time.strftime("%Y-%m-%d"))
now_time = str(now_date_time.strftime("%H-%M-%S"))

new_log_file_name = "WirelessAPsTester_{}.log".format(now_date)
log_file = os.path.join(log_file_location, new_log_file_name)


try:
    # rename existing log file with same date
    rename_previous_log_file(now_time, new_log_file_name, log_file_location)

    # create logger
    logFormatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%m/%d/%Y %H:%M:%S')
    logger = logging.getLogger('salary_slip_generator')
    logger.setLevel(logging.DEBUG)

    # create file handler and set level to debug
    fileHandler = logging.FileHandler(log_file)
    fileHandler .setLevel(logging.DEBUG)
    fileHandler .setFormatter(logFormatter)
    # add ch to logger
    logger.addHandler(fileHandler)

except Exception as e:
    print("Can not find logs directory", e)
    exit(1)


def error(msg):
    """ ERROR Message """

    sys.stdout.write(ERROR)
    print (time.strftime('%m/%d/%Y %I:%M:%S %p') + " ERROR " + msg)
    sys.stdout.write(RESET)
    logger.error(msg)


def warn(msg):
    """ WARNING Message """

    sys.stdout.write(WARN)
    print (time.strftime('%m/%d/%Y %I:%M:%S %p') + " WARNING " + msg)
    sys.stdout.write(RESET) 
    logger.warning(msg)


def info(msg):
    """ INFORMATION """

    sys.stdout.write(INFO)
    print (time.strftime('%m/%d/%Y %I:%M:%S %p') + " INFO " + msg)
    sys.stdout.write(RESET)
    logger.info(msg)


