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
    elemlist_len = len(elemlist)

    # bound optimization for hitting the bound at which
    # rest of the previous elements are already sorted
    new_bound = 0
    for outer_count in range(elemlist_len):
        inner_count = elemlist_len - 1
        bound = new_bound
        swapped = 0
        if DEBUG:
            print "from " + str(inner_count)
            print "to   " + str(bound)
            print "list " + str(elemlist)
            print "---------"
        while inner_count > bound:
            if cmprator(elemlist[inner_count], \
                        elemlist[inner_count - 1]) < 0:
                tmp = elemlist[inner_count]
                elemlist[inner_count] = elemlist[inner_count - 1]
                elemlist[inner_count - 1] = tmp
                # is swapped optimization
                swapped = 1
                new_bound = inner_count - 1
            inner_count -= 1
        if (swapped == 0):
            return None
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
