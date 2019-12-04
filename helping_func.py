from typing import Iterable
import logging

logger = logging.getLogger(__name__)


def logging_dec(func):
    """
    Logger for functions log values as: function_name, args, kwargs and res
    :param func:
    :return:
    """

    def wrapper(*args, **kwargs):
        res = func(*args, **kwargs)
        logger.info("-" * 40)
        logger.info(
            f'\nModule: {__name__}'
            f'\nFunction name: {func.__name__}'
            f'\nArgs:{args=}'
            f'\nKwargs:{kwargs=}'
            f'\nResult: {res=}'
        )
        logger.info("-" * 40)
        return res

    return wrapper


def merge_arrays(array):
    result = list()
    for el in array:
        if isinstance(el, Iterable) and not isinstance(el, (str, bytes)):
            result.extend(merge_arrays(el))
        else:
            result.append(el)
    return result


def logging_all_class_methods(Cls):
    class NewCls:
        def __init__(self, *args, **kwargs):
            self.oInstance = Cls(*args, **kwargs)

        def __getattribute__(self, s):

            try:
                x = super(NewCls, self).__getattribute__(s)
            except AttributeError:
                pass
            else:
                return x
            x = self.oInstance.__getattribute__(s)
            if type(x) == type(self.__init__):
                return logging_dec(x)
            else:
                return x

    return NewCls
