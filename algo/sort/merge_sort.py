#!/usr/bin/env python

""" Program to implement merge sort """

import sys
import lib.utils
import ex.exceptions
import algo.sort.utils

def_cmprator = lib.utils.get_def_cmprator()

DEBUG = 0

def is_sort_stable(): 
    """ algorithm's assumption about it's stability """
    return True

def merge(elemlist, start_idx, mid_idx, end_idx,\
          cmprator=def_cmprator): 
    """ Merge the intermediate sorted arrays """
    list1 = elemlist[start_idx : mid_idx + 1]
    list2 = elemlist[mid_idx+1 : end_idx + 1]

    counter1 = counter2 = counter = 0 
    max_counter1 = len(list1)
    max_counter2 = len(list2)
    max_counter = end_idx - start_idx + 1
    merged_list = [None] * max_counter

    if DEBUG:
        print "before " + str(elemlist)
        print "list1  " + str(list1)
        print "list2  " + str(list2)

    while counter < max_counter:
        if cmprator(list1[counter1], list2[counter2]) < 0:
            merged_list[counter] = list1[counter1]
            counter1 += 1
        else:
            merged_list[counter] = list2[counter2]
            counter2 += 1

        counter += 1

        if counter1 == max_counter1:
            while counter2 < max_counter2:
                merged_list[counter] = list2[counter2]
                counter2 += 1
                counter += 1
        elif counter2 == max_counter2:
            while counter1 < max_counter1:
                merged_list[counter] = list1[counter1]
                counter1 += 1
                counter += 1
    elemlist[start_idx:end_idx+1] = merged_list
    if DEBUG:
        print "after  " + str(elemlist)
        print "-------------"
    return None

def do_sort(elemlist, start_idx=0, end_idx=None, \
            cmprator=def_cmprator):
    """ Workhorse """
    if end_idx is None:
        end_idx = len(elemlist) - 1
    if (start_idx < end_idx):
        mid_idx = int((start_idx + end_idx) / 2)
        do_sort(elemlist, start_idx, mid_idx, cmprator)
        do_sort(elemlist, mid_idx + 1, end_idx, cmprator)
        merge(elemlist, start_idx, mid_idx, end_idx, cmprator)
    return None

def main(argv=None): 
    import ex.exceptions
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
