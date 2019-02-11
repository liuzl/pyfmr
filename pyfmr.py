#!/usr/bin/env python
#-*- coding:utf-8 -*-

import json
import ctypes

fmr = ctypes.CDLL('./fmr.so')
charptr = ctypes.POINTER(ctypes.c_char)

fmr.extractx.restype = charptr

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
