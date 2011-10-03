#!/usr/bin/env python

""" Program to implement the heap datastructure """

import lib.utils

REC_INDENT_ADD_BY = 2

def log_msg(msg, indent = 0):
    """ Logging method """
    print (" " * indent) + msg

class Heap:
    def __init__(self, **kwargs):
        """ Initialize the heap """
        self._list = kwargs.get('list', [])
        self._heapsize = len(self.list)
        self._cmprator = kwargs.get('cmprator', 
                                    lib.utils.get_def_cmprator())
        self._debug = kwargs.get('debug', 0)

    @property
    def list(self):
        return self._list

    @property
    def heapsize(self):
        return self._heapsize

    @property
    def cmprator(self):
        return self._cmprator

    @cmprator.setter
    def cmprator(self, cmpfunc):
        self._cmprator = cmpfunc
        return True

    @property
    def debug(self):
        return self._debug

    def __repr__(self):
        return "heapsize - " + str(self.heapsize) + " list - " +\
                str(self.list)

    def reset_heapsize(self):
        """ Reset heapsize to original list length """
        self.heapsize = len(self.list)

    def dec_heapsize(self, i):
        """ Decrement heapsize by i """
        self.heapsize -= i
        
    def inc_heapsize(self, i):
        """ Increment heapsize by i """
        self.heapsize += i
        if self.heapsize > len(self.list):
            self.list.append(None)

    def get_left_child_idx(self, i):
        """ Get left child of node """
        if i == 0:
            return 1
        return ((i << 1) + 1)
    
    def get_right_child_idx(self, i):
        """ Get right child of node """
        if i == 0:
            return 2 
        return ((i << 1) + 2)
    
    def get_parent_idx(self, i):
        """ Get parent of node """
        if (i <= 2):
            return 0
        if (i % 2 == 0):
            return ((i >> 1) - 1)
        return (i >> 1)

    def read(self, i):
        return self.list[i]

    def write(self, i, val):
        self.list[i] = val
        return True

    def max_heapify(self, curr_idx = 0, rec_indent = 0):
        """ Perform max heapify on passed heap index """
        lc_idx = self.get_left_child_idx(curr_idx)
        rc_idx = self.get_right_child_idx(curr_idx)
        curr_elem = self.read(curr_idx)
    
        if self.debug:
            log_msg("---------------", rec_indent)
            log_msg("heapsize    - " + str(self.heapsize), 
                    rec_indent)
            log_msg("max_heapify - list[" + str(curr_idx) +\
                    "] => " + str(curr_elem), rec_indent)
    
            lc_val = rc_val = "out_of_range"
            if lc_idx <= self.heapsize - 1:
                lc_val = self.read(lc_idx)
            if rc_idx <= self.heapsize - 1:
                rc_val = self.read(rc_idx)
    
            log_msg("left child  - list[" + str(lc_idx) + "] => " +\
                    str(lc_val), rec_indent)
            log_msg("right child - list[" + str(rc_idx) + "] => " +\
                    str(rc_val), rec_indent)
            log_msg("before      - " + str(self.list), rec_indent) 
                 
        if lc_idx < self.heapsize and\
           self.cmprator(self.read(lc_idx), curr_elem) > 0:
           max_idx = lc_idx
        else:
           max_idx = curr_idx
        
        if rc_idx < self.heapsize and\
           self.cmprator(self.read(rc_idx), 
                         self.read(max_idx)) > 0:
           max_idx = rc_idx
    
        if max_idx != curr_idx:
            tmp = self.read(max_idx)
            self.write(max_idx, self.read(curr_idx))
            self.write(curr_idx, tmp)
            if self.debug:
                log_msg("after       - " + str(self.list), 
                        rec_indent)
    
            self.max_heapify(max_idx, 
                             rec_indent = 
                             rec_indent + REC_INDENT_ADD_BY)
        else:
            if self.debug:
                log_msg("after       - " + str(self.list), 
                        rec_indent)

    def build_max_heap(self):
        """ Build max heap out of the passed heap """
        if self.debug:
            print "======================="
            print "BUILDING MAX HEAP BEGIN"
        start_idx = (self.heapsize - 1)/ 2
        while start_idx >= 0:
            self.max_heapify(start_idx)
            start_idx -= 1
        if self.debug:
            print "BUILDING MAX HEAP END"
            print "======================="
