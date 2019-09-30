# -*- coding: UTF-8 -*-
# _Author:Rea
class BaseResponse:
    def __init__(self):
        self.status = True
        self.summary = None
        self.error = None
        self.data = None

