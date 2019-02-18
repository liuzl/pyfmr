#!/usr/bin/env python
#-*- coding:utf-8 -*-
''' A python wrapper for FMR'''

import platform
import pkg_resources
import json
import ctypes

sysname = platform.system()

if sysname == 'Darwin':
    lib_name = "fmr-darwin-10.6-amd64.dylib"
elif sysname == 'Windows':
    lib_name = "fmr-windows-4.0-amd64.dll"
else:
    lib_name = "fmr-linux-amd64.so"

lib_path = pkg_resources.resource_filename('pyfmr', 'lib/{}'.format(lib_name))

fmr = ctypes.CDLL(lib_path)
charptr = ctypes.POINTER(ctypes.c_char)

fmr.extractx.restype = charptr
fmr.get_last_error.restype = charptr
fmr.parse.restype = charptr
fmr.frames.restype = charptr

def c(s): return ctypes.create_string_buffer(s.encode('utf-8'))

class Parser:
    '''python wrapper of fmr'''

    def __init__(self, grammar_file):
        self.error_message = ""
        self.grammar_file = grammar_file
        self.grammar_index = fmr.init_grammar(c(grammar_file))
        if self.grammar_index < 0:
            ret = fmr.get_last_error()
            value = ctypes.cast(ret, ctypes.c_char_p).value
            fmr.gofree(ret)
            self.error_message = value.decode('utf-8')

    def extractx(self, text, start):
        if self.grammar_index < 0:
            return None
        ret = fmr.extractx(self.grammar_index, c(text), c(start))
        value = ctypes.cast(ret, ctypes.c_char_p).value
        fmr.gofree(ret)
        return value.decode('utf-8')
    
    def extract(self, text, start):
        ret = self.extractx(text, start)
        if ret is None: return None
        return json.loads(ret)

    def parse(self, text, start):
        if self.grammar_index < 0:
            return None
        ret = fmr.parse(self.grammar_index, c(text), c(start))
        value = ctypes.cast(ret, ctypes.c_char_p).value
        fmr.gofree(ret)
        return value.decode('utf-8')

    def frames(self, text):
        if self.grammar_index < 0:
            return None
        ret = fmr.frames(self.grammar_index, c(text))
        value = ctypes.cast(ret, ctypes.c_char_p).value
        fmr.gofree(ret)
        return value.decode('utf-8')

