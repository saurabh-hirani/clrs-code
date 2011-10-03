#!/usr/bin/env python

""" Program to implement quick sort """

import sys
import lib.utils
import ex.exceptions
import algo.sort.utils

def_cmprator = lib.utils.get_def_cmprator()

DEBUG = 0
RANDOM_PIVOT = 1

def is_sort_stable(): 
    """ algorithm's assumption about it's stability """
    return False

def pivot_randomness():
    global RANDOM_PIVOT
    return RANDOM_PIVOT

def choose_random_pivot():
    global RANDOM_PIVOT
    RANDOM_PIVOT = 1

def partition(elemlist, start_idx, end_idx, cmprator = def_cmprator):
    if DEBUG:
        print "list           - " + str(elemlist)
        print "start_idx      - " + str(start_idx)
        print "end_idx        - " + str(end_idx)
    if pivot_randomness():
        import random
        sampling_range = range(start_idx, end_idx + 1)
        rand_pivot_idx = random.sample(sampling_range, 1)[0]
        if DEBUG:
            print "sublist        - " +\
                  str(elemlist[start_idx:end_idx+1])
            print "rand_pivot_idx - " + str(rand_pivot_idx)
        tmp = elemlist[start_idx]
        elemlist[start_idx] = elemlist[rand_pivot_idx]
        elemlist[rand_pivot_idx] = tmp

    pivot_idx = start_idx

    if DEBUG:
        print "sublist        - " + str(elemlist[start_idx:end_idx+1])
        print "curr pivot_idx - " + str(pivot_idx)

    pivot_val = elemlist[pivot_idx]
    i = pivot_idx
    j = i + 1
    while j < end_idx + 1:
        if (cmprator(pivot_val, elemlist[j]) >= 0):
            i += 1
            tmp = elemlist[i]
            elemlist[i] = elemlist[j]
            elemlist[j] = tmp
            if DEBUG:
                print "upd list       - " +\
                      str(elemlist[start_idx:end_idx+1])
        j += 1            
    tmp = elemlist[pivot_idx]
    elemlist[pivot_idx] = elemlist[i]
    elemlist[i] = tmp
    if DEBUG:
        print "new sublist    - " + str(elemlist[start_idx:end_idx+1])
        print "new pivot idx  - " + str(i)
        print "list           - " + str(elemlist)
        print "-------------------"
    return i

def do_sort(elemlist, start_idx = 0, end_idx = None,
            cmprator = def_cmprator):
    """ Workhorse """
    if end_idx is None:
        end_idx = len(elemlist) - 1
    if (start_idx < end_idx): 
        pivot = partition(elemlist, start_idx, end_idx, cmprator)
        do_sort(elemlist, start_idx, pivot - 1, cmprator)
        do_sort(elemlist, pivot + 1, end_idx, cmprator)

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
