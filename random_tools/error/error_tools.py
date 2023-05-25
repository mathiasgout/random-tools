import logging
import time
from functools import wraps
import asyncio


def exception(logger: logging.Logger) -> None:
    """Decorator to write exception in the logger

    Args:
        logger (logging.Logger): logger
    """

    def decorator(func):
        @wraps(func)
        def f_exception(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                issue = f"Exception in '{func.__module__}.{func.__name__}': '{e.__class__.__name__}' ({e})"
                logger.error(issue)
                raise

        return f_exception

    return decorator


def exception_async(logger: logging.Logger) -> None:
    """Async decorator to write exception in the logger

    Args:
        logger (logging.Logger): logger
    """

    def decorator(func):
        @wraps(func)
        async def f_exception(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                issue = f"Exception in '{func.__module__}.{func.__name__}': '{e.__class__.__name__}' ({e})"
                logger.error(issue)
                raise

        return f_exception

    return decorator


def retry(
    ExceptionToCheck: Exception,
    tries: int = 4,
    delay: int = 3,
    backoff: int = 2,
    logger: logging.Logger = None,
) -> None:
    """Retry calling the decorated function using an exponential backoff.
    http://www.saltycrane.com/blog/2009/11/trying-out-retry-decorator-python/
    original from: http://wiki.python.org/moin/PythonDecoratorLibrary#Retry

    Args:
        ExceptionToCheck (Exception): the exception to check. may be a tuple of exceptions to check
        tries (int, optional): number of times to try (not retry) before giving up. Defaults to 4.
        delay (int, optional): initial delay between retries in seconds. Defaults to 3.
        backoff (int, optional): backoff multiplier e.g. value of 2 will double the delay. Defaults to 2.
        logger (logging.Logger, optional): logging.Logger instance. Defaults to None.
    """

    def deco_retry(f):
        @wraps(f)
        def f_retry(*args, **kwargs):
            mtries, mdelay = tries, delay
            while mtries > 1:
                try:
                    return f(*args, **kwargs)
                except ExceptionToCheck as e:
                    msg = (
                        f"Retrying in {mdelay} seconds: '{e.__class__.__name__}' ({e})"
                    )
                    if logger:
                        logger.warning(msg)
                    else:
                        print(msg)
                    time.sleep(mdelay)
                    mtries -= 1
                    mdelay *= backoff
            return f(*args, **kwargs)

        return f_retry

    return deco_retry


def retry_async(
    ExceptionToCheck: Exception,
    tries: int = 4,
    delay: int = 3,
    backoff: int = 2,
    logger: logging.Logger = None,
) -> None:
    """Asynchronous retry calling the decorated function using an exponential backoff.
    http://www.saltycrane.com/blog/2009/11/trying-out-retry-decorator-python/
    original from: http://wiki.python.org/moin/PythonDecoratorLibrary#Retry

    Args:
        ExceptionToCheck (Exception): the exception to check. may be a tuple of exceptions to check
        tries (int, optional): number of times to try (not retry) before giving up. Defaults to 4.
        delay (int, optional): initial delay between retries in seconds. Defaults to 3.
        backoff (int, optional): backoff multiplier e.g. value of 2 will double the delay. Defaults to 2.
        logger (logging.Logger, optional): logging.Logger instance. Defaults to None.
    """

    def deco_retry(f):
        @wraps(f)
        async def f_retry(*args, **kwargs):
            mtries, mdelay = tries, delay
            while mtries > 1:
                try:
                    return await f(*args, **kwargs)
                except ExceptionToCheck as e:
                    msg = (
                        f"Retrying in {mdelay} seconds: '{e.__class__.__name__}' ({e})"
                    )
                    if logger:
                        logger.warning(msg)
                    else:
                        print(msg)
                    await asyncio.sleep(mdelay)
                    mtries -= 1
                    mdelay *= backoff
            return await f(*args, **kwargs)

        return f_retry

    return deco_retry
