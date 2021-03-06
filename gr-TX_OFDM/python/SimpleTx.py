#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2019 <+YOU OR YOUR COMPANY+>.
# 
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 

import numpy
import pickle
from gnuradio import gr


class SimpleTx(gr.sync_block):
    """
    docstring for block SimpleTx
    """
    def __init__(self, case, pickle_dir, file_name):
        gr.sync_block.__init__(self,
                               name="SimpleTx",
                               in_sig=None,
                               out_sig=[numpy.complex64])
        with open(pickle_dir + file_name) as f:
            self.tx_data = pickle.load(f)
        self.source_buffer_sz = self.tx_data.shape[1]

        self.current_ptr = 0

    def work(self, input_items, output_items):
        out = output_items[0]
        output_buffer_sz = out[:].shape[0]
        self.current_ptr = self.current_ptr % self.source_buffer_sz
        end_ptr = (self.current_ptr + output_buffer_sz) % self.source_buffer_sz

        if end_ptr < self.current_ptr:
            out[0:(self.source_buffer_sz - self.current_ptr)] = self.tx_data[0, self.current_ptr: self.source_buffer_sz]
            out[(self.source_buffer_sz - self.current_ptr):] = self.tx_data[0, 0:end_ptr]
        else:
            out[:] = self.tx_data[0, self.current_ptr % self.source_buffer_sz: end_ptr % self.source_buffer_sz]
        self.current_ptr = self.current_ptr + output_buffer_sz
        return len(output_items[0])
