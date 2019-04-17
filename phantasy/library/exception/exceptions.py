#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class TimeoutError(Exception):
    def __init__(self, *args, **kws):
        super(self.__class__, self).__init__(*args, **kws)


class PutFinishedException(Exception):
    def __init__(self, *args, **kws):
        super(self.__class__, self).__init__(*args, **kws)

