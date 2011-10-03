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

    logic = 1 

    if logic == 1:
        for outer_cnt in range(1, len(elemlist)):
            inner_cnt = outer_cnt
            key = elemlist[inner_cnt]
            while (cmprator(key, elemlist[inner_cnt - 1]) < 0) and \
                  (inner_cnt >= 1):
                elemlist[inner_cnt] = elemlist[inner_cnt - 1]
                inner_cnt -= 1
                if DEBUG: print(elemlist)
            elemlist[inner_cnt] = key
            if DEBUG: 
                print(elemlist)
                print ""
    elif logic == 2:
        for outer_cnt in range(1, len(elemlist)):
            inner_cnt = outer_cnt
            while (cmprator(elemlist[inner_cnt], elemlist[inner_cnt - 1]) < 0) \
                  and (inner_cnt >= 1):
                elemlist[inner_cnt], elemlist[inner_cnt - 1] = \
                elemlist[inner_cnt - 1], elemlist[inner_cnt]
                inner_cnt -= 1
                if DEBUG: 
                    print(elemlist)
                    print ""
    elif logic == 3:
        for outer_cnt in range(1, len(elemlist)):
            inner_cnt = outer_cnt - 1
            while (cmprator(elemlist[inner_cnt + 1], elemlist[inner_cnt]) < 0)\
                  and (inner_cnt >= 0):
                elemlist[inner_cnt + 1], elemlist[inner_cnt] = \
                elemlist[inner_cnt], elemlist[inner_cnt + 1]
                inner_cnt -= 1
                if DEBUG: 
                    print(elemlist)
                    print ""
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
