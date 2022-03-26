#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------------------
# 通过蓝奏云上传/下载指定的文件夹内容。
#

import fire
from rich import print
from rich.prompt import Prompt
from rich.console import Console
from rich.progress import (
    BarColumn,
    Progress,
    TaskID,
    TextColumn,
    TimeRemainingColumn,
    TransferSpeedColumn,
)
import signal
from concurrent.futures import as_completed, ThreadPoolExecutor
from threading import Event
import os
import sys
from lanzou.api import *

lzy = LanZouCloud()

# def failcall(code, file):
#     print('code {}  {}'.format(code, file), end='')

cookie_path = '.yunpan_cookie'


def show_progress(file_name, total_size, now_size):
    """显示进度的回调函数"""
    percent = now_size / total_size
    bar_len = 40  # 进度条长总度
    bar_str = '>' * round(bar_len * percent) + '=' * \
        round(bar_len * (1 - percent))
    print('\r{:.2f}%\t[{}] {:.1f}/{:.1f}MB | {} '.format(
        percent * 100, bar_str, now_size / 1048576, total_size / 1048576, file_name), end='')
    if total_size == now_size:
        print('')  # 下载完成换行


def handler(fid, is_file):
    """上传文件完成后处理事件"""
    if is_file:
        lzy.set_desc(fid, '', is_file=True)


def load_cookie():
    with open(cookie_path, 'r') as f:
        values = f.readlines()
        f.close
    return values


def login():
    cookie = load_cookie()
    return lzy.login_by_cookie(
        {'ylogin': cookie[0], 'phpdisk_info': cookie[1]}
    )


class CliCmd:

    def set(self):
        """
        设置cookie参数，保存在.yunpan_cookie文件里
        """
        cookie = []
        cookie.append(Prompt.ask('ylogin:', default=''))
        cookie.append('\n')
        cookie.append(Prompt.ask('phpdisk_info', default=''))
        with open(cookie_path, 'w') as f:
            f.writelines(cookie)
            f.close

    def upload(self, *paths, remote):
        '''
        upload files/paths to remote
        '''
        if login() == lzy.SUCCESS:
            lzy.ignore_limits()
            for file in paths:
                lzy.upload_file(file, -1, callback=show_progress,
                                uploaded_handler=handler)
        else:
            print("登录失败")

    def download(self, *remote, path):
        """
        download remote file to local path
        """
        if login() == lzy.SUCCESS:
            lzy.ignore_limits()
            for file in remote:
                lzy.down_dir_by_url


if __name__ == '__main__':
    '''
    cookie信息存放在.cookie文件中，如果不存在这个文件或者数据不符合要求，提示输入cookie内容，并自动保存在这个文件
    否则直接执行
    '''

    fire.Fire(CliCmd)

    # cmd = Prompt.ask('.', default='i')
    # if cmd != 'i':
    #     print('Bye', ':vampire:')
    #     sys.exit()

    # with progress:
    #     with ThreadPoolExecutor(max_workers=1) as pool:
    #         task_id = progress.add_task("import", import_filename=import_wb_file, start=False)
    #         pool.submit(import_file, task_id, import_wb_file)

    # if login() == lzy.SUCCESS:
    # download()
