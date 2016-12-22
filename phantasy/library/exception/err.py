__author__ = 'shen'

class ExceptionTemplate(Exception):
    def __call__(self, *args):
        return self.__class__(*(self.args + args))

    def __str__(self):
        return ': '.join(self.args)

class CSVFormatError(ExceptionTemplate):
    pass

class DataError(ExceptionTemplate):
    pass