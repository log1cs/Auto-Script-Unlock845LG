#!/usr/bin/python3
# -*- coding: utf-8 -*-
# (c) B.Kerler 2018-2021

import logging
from edl.Library.utils import LogBase

try:
    from edl.Library.Modules.generic import generic
except ImportError as e:
    generic = None
    pass

try:
    from edl.Library.Modules.oneplus import oneplus
except ImportError as e:
    oneplus = None
    pass

try:
    from edl.Library.Modules.xiaomi import xiaomi
except ImportError as e:
    xiaomi = None
    pass

class modules(metaclass=LogBase):
    def __init__(self, fh, serial, supported_functions, loglevel, devicemodel, args):
        self.fh = fh
        self.args = args
        self.serial = serial
        self.error = self.__logger.error
        self.supported_functions = supported_functions
        self.__logger.setLevel(loglevel)
        if loglevel==logging.DEBUG:
            logfilename = "log.txt"
            fh = logging.FileHandler(logfilename)
            self.__logger.addHandler(fh)
        self.options = {}
        self.devicemodel = devicemodel
        self.generic = None
        try:
            self.generic = generic(fh=self.fh, serial=self.serial, args=self.args, loglevel=loglevel)
        except Exception as e:
            pass
        self.ops = None
        try:
            self.ops = oneplus(fh=self.fh, projid=self.devicemodel, serial=self.serial,
                               supported_functions=self.supported_functions, args=self.args,loglevel=loglevel)
        except Exception as e:
            pass
        self.xiaomi=None
        try:
            self.xiaomi = xiaomi(fh=self.fh)
        except Exception as e:
            pass

    def addpatch(self):
        if self.ops is not None:
            return self.ops.addpatch()
        return ""

    def addprogram(self):
        if self.ops is not None:
            return self.ops.addprogram()
        return ""

    def edlauth(self):
        if self.xiaomi is not None:
            return self.xiaomi.edl_auth()
        return True

    def writeprepare(self):
        if self.ops is not None:
            return self.ops.run()
        return True

    def run(self, command, args):
        args = args.split(",")
        options = {}
        for i in range(len(args)):
            if "=" in args[i]:
                option = args[i].split("=")
                if len(option) > 1:
                    options[option[0]] = option[1]
            else:
                options[args[i]] = True
        if command=="":
            print("Valid commands are:\noemunlock\n")
            return False
        if self.generic is not None and command == "oemunlock":
            if "enable" in options:
                enable = True
            elif "disable" in options:
                enable = False
            else:
                self.error("Unknown mode given. Available are: enable, disable.")
                return False
            return self.generic.oem_unlock(enable)
        return False
