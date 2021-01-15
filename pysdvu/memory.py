# -*- coding: utf-8 -*-
# ================================================
# Project: sdvu
# Author: Quentin Ducasse
# Email: quentin.ducasse@ensta-bretagne.org
# Repository: https://github.com/QDucasse/pysdvu
# ================================================

# MEMORY
# ======

class Memory(object):
    def __init__(self, size):
        self.bytes_array = [0]*size

    def __len__(self):
        return len(self.bytes_array)

    def __getitem__(self, index):
        return self.bytes_array[index]

    def __setitem__(self, index, value):
        self.bytes_array[index] = value

class Register(object):
    def __init__(self, cell_size):
        self.cell_size = cell_size
        self.value = 0

    def __get__(self, obj, objtype=None):
        return self.value

    def __set__(self, obj, value):
        self.value = value

class MemoryManipulator(object):
    def __init__(self, cell_size):
        self.cell_size = cell_size
        self.memory = None

    def read_cell_at_address(self, address):
        value = 0
        for i in range(self.cell_size):
            value = (value << 8) | self.memory[address+i]
        return value

    def write_cell_at_address(self, address, cell_value):
        to_write = cell_value
        for addr in range(address + self.cell_size - 1, address-1, -1):
            self.memory[addr] = to_write & 0xFF
            to_write = to_write >> 8
