#!/usr/bin/env python

""" Program to implement insertion sort """

import sys
import lib.utils
import algo.sort.utils

DEBUG = 0
def_cmprator = lib.utils.get_def_cmprator()

def is_sort_stable(): 
    """ algorithm's assumption about it's stability """
    return True

def do_sort(elemlist, cmprator=def_cmprator):
    """ Workhorse """
    outer_count = 0
    max_range = len(elemlist) - 1
    while (outer_count < max_range):
        min_idx = outer_count
        inner_count = outer_count + 1
        while (inner_count < max_range + 1):
            if (cmprator(elemlist[inner_count],elemlist[min_idx]) < 0):
                min_idx = inner_count
            inner_count += 1
        if (min_idx != outer_count):
            if DEBUG:
                print "swapping (elemlist[" + str(outer_count) +\
                       "] = " + str(elemlist[outer_count]) +\
                       ") with (elemlist[" + str(min_idx) +\
                       "] = " + str(elemlist[min_idx]) + ")"
            tmp = elemlist[outer_count]
            elemlist[outer_count] = elemlist[min_idx]
            elemlist[min_idx] = tmp
        outer_count += 1
        if DEBUG:
            print elemlist
    return None

def main(argv=None): 
    try:
        input = algo.sort.utils.build_args(argv)
    except ex.exceptions.ValidationError:
        return(2)
    global DEBUG
    DEBUG = int(input['debug'])
    do_sort(input['list'])
    return(0)

if __name__ == "__main__":
    sys.exit(main())
