#coding=utf-8
import logging, logging.handlers
import traceback
import os.path
import sys
import threading
import time
import os
from weblog import date_rotatingfilehandler
# window and linux set different path
import platform
if platform.system() == "Windows":
    log_path = u'./static/files/weblog'
else:
    log_path = u"/home/Faye/log/weblog"

class ctrace_logger(logging.Logger):
    """
    Class: ctrace_logger
    Description: 重载logging.Logger, 主要目的是确保日志记录接口不抛出异常
    Base: logging.Logger
    Others: 
    """

    def __init__(self, name):
        logging.Logger.__init__(self, name)
        
        self.setLevel(logging.DEBUG)
        self.handler = None
        #self.console_handler = None
        self.file_path = ''
        #self.name = ''

    # def _log(self, level, msg, args, exc_info=None, extra=None):
    def _log(self, level, msg, args, exc_info=None, extra=None, stack_info=False):
        """
        Method:    _log
        Description: 重载基类的_log方法，捕获异常，确保异常不会对外抛异常，导致软件功能失败
        Parameter: 
            level: 日志的级别
            msg: 日志文本信息
            args: 参数
            exc_info: 当前的栈信息
            extra: 其他信息
        Return: 
        Others: 
        """
        try:
            if logging._srcfile:
                #IronPython doesn't track Python frames, so findCaller throws an
                #exception on some versions of IronPython. We trap it here so that
                #IronPython can use logging.
                try:
                    fn, lno, func = self.findCaller()
                except ValueError:
                    fn, lno, func = "(unknown file)", 0, "(unknown function)"
            else:
                fn, lno, func = "(unknown file)", 0, "(unknown function)"
            if exc_info:
                if not isinstance(exc_info, tuple):
                    exc_info = sys.exc_info()
            record = self.makeRecord(self.name, level, fn, lno, msg, args, exc_info, func, extra)
            self.handle(record)
        except:
            print ("LOG EXCEPTION", msg)
            traceback.print_exc(file=sys.stdout)
            
    def open(self,file_path):   
        """
        Method:    open
        Description: 打开日志文件
        Parameter: 
            file_path: 日志文件路径
        Return: 
        Others: 每个文件存放的日志为2M，可以通过max_file_count控制当前日志的总大小
        """
        self.close()

        self.file_path = file_path

        #self.name = name
        
        #self.logger = logging.getLogger(name)
#        self.handler = logging.handlers.RotatingFileHandler(
#                 file_path
#                , maxBytes=1024*1024*2
#                , backupCount=max_file_count)

        self.handler = date_rotatingfilehandler.DataRotatingFileHandler(
                 file_path
                , maxBytes=1024*1024*10)

        fmt = '[%(levelname)s] %(asctime)s %(message)s [File:%(filename)s Function:%(funcName)s Line:%(lineno)d]'
        #fmt = '%(asctime)s  %(levelname)s %(message)s'
        formatter = logging.Formatter(fmt)
        
        self.addHandler(self.handler)

        # 在文件头，写入时间，以便切换文件的时候，提取时间
        current_time = time.strftime("[%Y-%m-%d_%H-%M-%S]" , time.localtime(time.time()))
        self.info(current_time)
        
        self.handler.setFormatter(formatter)

        
    def close(self):
        if self.handler is None:
            return
            
        self.handler.flush()     
        self.handler.close()
        self.removeHandler(self.handler)
        
        self.handler = None
        #self.logger = None
        
logging.setLoggerClass(ctrace_logger)
g_logger = None
g_print_lock = None

def _print_log(level, msg, *args, **kwargs):
    global g_print_lock
    if g_print_lock is None:
        g_print_lock = threading.RLock()
        
    with g_print_lock:
        try:
            msg = msg.decode("utf-8")
        except:
            pass
            
        try:
            time_info = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
       #     logmsg = level + ' '+ time_info + ' ' + msg + '[File:%s Funtion:%s Line:%s]'
            # %sys._getframe().f_code.co_filename,sys_getframe().f_code.co_name,sys_getframe().f_lineno
            if len(args) > 0:
                msg = msg % args
            elif len(kwargs) > 0:
                msg = msg % kwargs
            print (level, time_info, msg)
    
        except:
            pass
            
def _print_debug(msg, *args, **kwargs):

    _print_log("[debug]", msg, *args, **kwargs)

def _print_info(msg, *args, **kwargs):
    _print_log("[info]", msg, *args, **kwargs)

def _print_warning(msg, *args, **kwargs):
    _print_log("[warning]", msg, *args, **kwargs)
    
def _print_error(msg, *args, **kwargs):
    _print_log("[error]",  msg, *args, **kwargs)
       
def _exception(msg, *args, **kwargs):    
    """
    Description: 当发生异常时，通过本函数输出异常日志到stdout
    """
    global g_print_lock
    if g_print_lock is None:
        g_print_lock = threading.RLock()
    with g_print_lock:
        try:
            msg = msg.decode("utf-8")
        except:
            pass
        try:
            time_info = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            print (time_info, 'exception:', msg)
            print(traceback.format_exc())
        except:
            pass
    
debug       = _print_debug
info        = _print_info
warning     = _print_warning
error       = _print_error
exception   = _exception

def open(logname):
    """
    Description: 打开日志文件
    Parameter: 
        logname: 日志文件的名称
        file_path: 文件存放的目录##删除了
    """
    global g_logger, debug, info, warning, error, exception
    close()
    g_logger = logging.getLogger(logname)
    # dir_path = os.path.join(os.environ.get('LOG_PREFIX'), os.environ.get('WORKSPACE'), os.environ.get('LOG_POSTFIX'), 'server_log')
    dir_path = log_path
    ret = os.path.isdir(dir_path)
    
    if ret != True:
        try:
            os.makedirs(dir_path)
        except:
            if os.path.isdir(dir_path):
                info("mkdir %s ok" % dir_path);   
            exception("mkdir %s failed." % dir_path)
        
    g_logger.open(file_path = os.path.join(dir_path, logname + '.log'))

    debug       = g_logger.debug
    info        = g_logger.info
    warning     = g_logger.warning
    error       = g_logger.error
    exception   = g_logger.exception

def get_logger():
    global g_logger
    return g_logger

def close():
    """
    Description: 关闭日志文件
    Others: 关闭日志文件后，后续日志将会输出到stdout
    """

    global g_logger, debug, info, warning, error, exception

    if g_logger is not None:
        g_logger.close()
        g_logger = None

    debug       = _print_debug
    info        = _print_info
    warning     = _print_warning
    error       = _print_error
    exception   = _exception