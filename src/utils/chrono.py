from datetime import datetime, timedelta
from contextlib import contextmanager
# ###############################

class Chrono:
    def __init__(self):
        self.value  = timedelta()
        self._start = None
    # ###############################

    def __repr__(self):
        return "<%s %s>" % (self.__class__.__name__, self.value)
    # ###############################

    def start(self):
        self._start = datetime.now()
        return self
    # ###############################

    def stop(self):
        assert self._start is not None
        self.value = datetime.now() - self._start
        return self
    # ###############################

    def __enter__(self):
        return self.start()
    # ###############################

    def __exit__(self, *_):
        self.stop()
    # ###############################


@contextmanager
def PrintChrono(prefix='', suffix=''):
    chrono = Chrono()
    with chrono:
        yield
    print('%s%s%s' % (prefix, chrono.value, suffix))
# ###############################
