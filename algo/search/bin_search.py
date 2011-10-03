#!/usr/bin/env python

import sys
import ex.exceptions
import lib.utils
import algo.search.utils

""" 
Program to implement binary search 
with a strategy option to search first available,
leftmost or rightmost occurance
"""

DEBUG = 0
def_cmprator = lib.utils.get_def_cmprator()

def do_search(elemlist, target, \
              start_idx = 0, end_idx = None, \
              strategy = None,\
              cmprator = def_cmprator):
    if end_idx is None:
        end_idx = len(elemlist) - 1

    target_idx = -1
    if start_idx <= end_idx:
        mid_idx = (start_idx + end_idx) / 2
        if DEBUG:
            print "start_idx - " + str(start_idx) +\
                  "|start_val - " + str(elemlist[start_idx])
            print "end_idx   - " + str(end_idx) +\
                  "|end_val   - " + str(elemlist[end_idx])
            print "mid_ idx  - " + str(mid_idx) +\
                  "|mid_val   - " + str(elemlist[mid_idx])
            print
        if cmprator(elemlist[mid_idx], target) == 0:
            target_idx = mid_idx
        elif cmprator(elemlist[mid_idx], target) > 0:
            end_idx = mid_idx - 1
        else:
            start_idx = mid_idx + 1

        # If not found via mid
        if target_idx == -1:
            target_idx = do_search(elemlist, target,\
                                   start_idx, end_idx,
                                   strategy, cmprator)

        # If found either via mid or by recursive calls
        if strategy is None:
            # No strategy - return the first occurance
            return target_idx
        elif target_idx != -1:
            # Decide the direction depending on the strategy
            if strategy == 'left':
                end_idx = target_idx - 1
            else:
                start_idx = target_idx + 1
            prev_target_idx = target_idx
            target_idx = do_search(elemlist, target,\
                                   start_idx, end_idx,\
                                   strategy, cmprator)
            if target_idx == -1:
                return prev_target_idx
            else:
                return target_idx
        else:
            return target_idx
    else:
        return -1

def main(argv=None): 
    try:
        input = algo.search.utils.build_args(argv)
    except ex.exceptions.ValidationError:
        return(2)

    global DEBUG
    DEBUG = int(input['debug'])
    if DEBUG:
        print input['list']
        print

    target_idx = do_search(input['list'], input['target'],\
                           strategy = input['strategy'])

    if DEBUG:
        print "target idx " + str(target_idx)
    if target_idx == -1:
        return(1)
    else:
        return(0)

if __name__ == "__main__":
    sys.exit(main())
