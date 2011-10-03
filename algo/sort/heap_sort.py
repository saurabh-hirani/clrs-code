#!/usr/bin/env python

""" Program to implement heap sort """

import sys
import lib.utils

import ex.exceptions
import algo.sort.utils
from ds.heap import Heap

def_cmprator = lib.utils.get_def_cmprator()

DEBUG = 0

def is_sort_stable(): 
    """ algorithm's assumption about it's stability """
    return False

def do_sort(heap_obj):
    """ Workhorse """
    heap_obj.reset_heapsize()
    heap_obj.build_max_heap()
    if DEBUG:
        print "======================="
        print "HEAP SORT BEGIN"
    while heap_obj.heapsize > 1:
        heapsize = heap_obj.heapsize
        tmp = heap_obj.list[heapsize - 1]
        heap_obj.list[heapsize - 1] = heap_obj.list[0]
        heap_obj.list[0] = tmp
        heap_obj.dec_heapsize(1)
        heap_obj.max_heapify()
    if DEBUG:
        print "HEAP SORT END"
        print "======================="
    return heap_obj

def build_heap_obj(**kwargs):
    return Heap(**kwargs)

def main(argv=None): 
    try:
        input = algo.sort.utils.build_args(argv)
    except ex.exceptions.ValidationError:
        return(2)

    global DEBUG
    DEBUG = int(input['debug'])

    heap_obj = build_heap_obj(
        list = input['list'],
        debug = input['debug'],
        cmprator = lambda x, y : (x - y)
    )
    do_sort(heap_obj)
    return(0)

if __name__ == "__main__":
    sys.exit(main())
