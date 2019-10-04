import logging

from camera_ctrl.log_to_db import LogType, log_to_db


def get_log_msg(file: str):
    return '{}: has been transferred'.format(file)


def file_transferred_log(file: str, **kwargs):
    logging.info(get_log_msg(file))


def file_transferred_log_to_db(file: str, **kwargs):
    log_type = LogType.INFO
    category = 'FileTransfer'
    title = 'File transferred'
    content = get_log_msg(file)

    log_to_db(log_type=log_type, category=category, title=title, content=content)