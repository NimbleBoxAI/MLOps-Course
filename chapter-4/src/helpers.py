import datetime
import logging
import ntpath
import os
import shutil
from typing import Optional

from pythonjsonlogger import jsonlogger
from pytz import timezone, utc
from rich.logging import RichHandler

from cloudpathlib import CloudPath

def create_folder(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        print("Directory created: " + directory)
    else:
        print("Directory exists: " + directory)


def create_logger(
    project_name: str,
    level: str = "INFO",
    log_dir: str = "logs",
    file_name: Optional[str] = None,
    do_print: bool = True,
    simple_logging: bool = False,
    log_to_file: bool = False,
    rich_logging: bool = False,
    time_zone: Optional[str] = None,
    json_logging: bool = False,
):
    """Creates a logger of given level and saves logs to a file

    :param project_name: project name for which we are logging
    :param level: logging level
                  LEVELS available
                  DEBUG: Detailed information, typically of interest only when diagnosing problems.
                  INFO: Confirmation that things are working as expected.
                  WARNING: An indication that something unexpected happened, or indicative of some problem in the near future (e.g. 'disk space low'). The software is still working as expected.
                  ERROR: Due to a more serious problem, the software has not been able to perform some function.
                  CRITICAL: A serious error, indicating that the program itself may be unable to continue running.
    :param log_dir: directory when log files are created
    :param file_name: name of the log file
    :param do_print: whether to print the logs
    :param simple_logging: sets formatter to only message
    :param log_to_file: whether to save logs on disk
    :param rich_logging: colorful logging using rich
    :param time_zone: timezone to be used for time in logging such as Asia/Kolkata
                      https://gist.github.com/heyalexej/8bf688fd67d7199be4a1682b3eec7568
    """
    import __main__

    if file_name is None:
        try:
            file_name = ntpath.basename(__main__.__file__).split(".")[0]
        except:
            file_name = "logs"

    logger = logging.getLogger(file_name)
    logger.handlers.clear()
    logger.setLevel(getattr(logging, level))

    # These default log values get eliminated
    JSON_ELIMINATE_ARGS = [
        "exc_info",
        "exc_text",
        "msecs",
        "msg",
        "name",
        "pathname",
        "process",
        "processName",
        "relativeCreated",
        "stack_info",
        "thread",
        "threadName",
        "levelno",
        "args",
        "created",
    ]

    if time_zone:

        def time_formatter(*args):
            # TODO: Doesnt work with rich formatter
            utc_dt = utc.localize(datetime.datetime.utcnow())
            my_tz = timezone(time_zone)
            converted = utc_dt.astimezone(my_tz)
            return converted.timetuple()

        logging.Formatter.converter = time_formatter

    if rich_logging:
        stream_format = f"{project_name}:%(module)s:%(funcName)s: %(message)s"
        stream_handler = RichHandler(omit_repeated_times=False)
    else:
        stream_format = f"%(asctime)s:%(levelname)s:{project_name}:%(module)s:%(funcName)s: %(message)s"
        stream_handler = logging.StreamHandler()

    file_formatter = stream_formatter = logging.Formatter(
        stream_format, "%Y-%m-%d %H:%M:%S"
    )

    if json_logging:
        json_formatter = jsonlogger.JsonFormatter(
            reserved_attrs=JSON_ELIMINATE_ARGS, timestamp=True
        )

    if simple_logging:
        file_formatter = logging.Formatter("%(message)s")
        stream_formatter = logging.Formatter("%(message)s")

    if log_to_file:
        date = datetime.date.today()
        date = "%s-%s-%s" % (date.day, date.month, date.year)
        log_file_path = os.path.join(log_dir, "%s-%s.log" % (file_name, date))

        create_folder(log_dir)
        file_handler = logging.FileHandler(log_file_path)
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

    if do_print:
        if json_logging:
            stream_handler.setFormatter(json_formatter)
        else:
            stream_handler.setFormatter(stream_formatter)
        logger.addHandler(stream_handler)

    logger.propagate = False

    return logger


def download_s3_folder(bucket_name: str, model_name: str, local_dir: str) -> None:
    """
    Download the contents of a folder directory
    Args:
        bucket_name: the name of the s3 bucket
        s3_folder: the folder path in the s3 bucket
        local_dir: directory path in the local file system
    """
    logger = create_logger(project_name="download_model", level="INFO", json_logging=True)
    uri = f"s3://{bucket_name}/{model_name}"
    cp = CloudPath(uri)
    logger.info(f"Downloading...")
    cp.download_to(local_dir)
    logger.info("Download complete!")



def download_model_from_s3(
    model_name: str,
    download_folder: str = "./models",
    s3_bucket: str = "mlops-course/models",
) -> str:
    """Downloads model from s3 bucket based on given arguments and saves in default download folder
    Args:
        model_name (str): Name of model to be loaded
        download_folder (str)(Optional): Path where model will be downloaded
        s3_bucket (str)(Optional): S3 bucket name where the model is present. Defaults to mlops-course/models
    Return:
        str: Path where model is downloaded
    """
    logger = create_logger(project_name="download_model", level="INFO", json_logging=True)
    model_path = download_folder
    os.makedirs(model_path, exist_ok=True)

    ## If the folder already contains model files return model_path
    if os.listdir(model_path):
        logger.info(f"Model already exists at {model_path} skipping the downloading...")
        return model_path

    shutil.rmtree(model_path)

    remote_directory = f"s3://{s3_bucket}/{model_name}"

    logger.info(f"Downloading the model from: {remote_directory} to {model_path}")
    download_s3_folder(
        s3_bucket,
        model_name=model_name,
        local_dir=model_path,
    )

    return model_path