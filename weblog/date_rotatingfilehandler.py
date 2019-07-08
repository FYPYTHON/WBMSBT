#coding=utf-8
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-12-25
Description: 
Others:      
Key Class&Method List: 
             1. DataRotatingFileHandler： 日志滚动处理
History: 
1. Date:2012-12-25
   Author:ACP2013
   Modification:新建文件
"""

import time
import logging
import logging.handlers
import os, os.path
import re


class DataRotatingFileHandler(logging.handlers.RotatingFileHandler):
    """
    Class: DataRotatingFileHandler
    Description: 日志滚动处理
    Base: RotatingFileHandler
    Others: 无
    """

    def __init__(self, filename, mode='a', maxBytes=110, encoding=None, delay=0):
        """
        Method: __init__
        Description: 初始化
        Parameter: 
            filename: 日志文件名
            mode: 文件打开方式
            maxBytes: 日志最大值
            encoding: 日志编码
            delay: 
        Return: 无
        Others: 无
        """
        self.__original_maxbytes = maxBytes
        back_count = 10

        logging.handlers.RotatingFileHandler.__init__(self, filename, mode, maxBytes, back_count, encoding, delay)

    def xxxdoRollover(self): # 这个函数的重载，目前不用了
        """
        Method: doRollover
        Description: 日志滚动处理
        Parameter: 无
        Return: 无
        Others: 无
        """

        if self.stream is not None:
            self.stream.close()
            self.stream = None

        # 获取日志的开始时间
        start_time = "2000-01-01_00-00-00"
        try:
            with open(self.baseFilename) as f:
                line = f.readline()
                
            p = re.match(r"\[((\d{2,4})([-_]\d{1,2}){5})\]", line)
            if p is not None:
                start_time = p.group(1)
                
        except:
            pass
            
        current_time = time.strftime("%Y-%m-%d_%H-%M-%S" , time.localtime(time.time()))
        dfn = "%s_%s__%s.log" % (self.baseFilename[:-4],start_time, current_time)
        
        if not os.path.exists(dfn):            
            try:
                os.rename(self.baseFilename, dfn)
            except Exception:
                self.maxBytes = int(self.maxBytes * 1.5)
                self.mode = 'a'
                self.stream = self._open()
                return
        else:
            self.maxBytes = int(self.maxBytes * 1.5)
            self.mode = 'a'
            self.stream = self._open()
            return

        if self.maxBytes>self.__original_maxbytes:
            self.maxBytes = self.__original_maxbytes 
        self.mode = 'w'
        self.stream = self._open()
        self.stream.write("[%s]\n" % current_time)

# if __name__ == "__main__":
