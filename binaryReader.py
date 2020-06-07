# Copyright (c) Speedbot Corporation. All rights reserved.
# Licensed under the MIT License.

'''
@Author       : Lintao Zheng
@Email        : lintaozheng1991@gmail.com
@Github       : https://github.com/zlt1991
@Date         : 2020-05-10 18:02:13
@LastEditTime : 2020-05-10 18:02:14
'''
import struct

class BinaryReaderEOFException(Exception):
    def __init__(self):
        pass

    def __str__(self):
        return 'Not enough bytes in file to satisfy read request'

class BinaryReader(object):
    def __init__(self):
        self.typeNames = {
            'int8': 'b',
            'uint8': 'B',
            'int16': 'h',
            'uint16': 'H',
            'int32': 'i',
            'uint32': 'I',
            'int64': 'q',
            'uint64': 'Q',
            'float': 'f',
            'double': 'd',
            'char': 's'}

    def read(self, value, typeName, times=1):
        typeFormat = self.typeNames[typeName.lower()]*times
        typeSize = struct.calcsize(typeFormat)
        if typeSize != len(value):
            raise BinaryReaderEOFException
        return struct.unpack(typeFormat, value)

    def close(self):
        self.file.close()
