#!/usr/bin/env python

import sys
import lib.utils
import algo.sort.utils

def_cmprator = lib.utils.get_def_cmprator()

DEBUG = 0

def merge(elemlist, start_idx, mid_idx, end_idx,\
          cmprator = def_cmprator):
    print elemlist[start_idx : mid_idx + 1]
    print elemlist[mid_idx + 1 : end_idx + 1]
    pass

def find_inversions(elemlist, start_idx = 0, end_idx = None,\
                    cmprator = def_cmprator):
    if end_idx is None:
        end_idx = len(elemlist) - 1
    if start_idx < end_idx:
        mid_idx = int((start_idx + end_idx)/2)
        find_inversions(elemlist, start_idx, mid_idx, cmprator)
        find_inversions(elemlist, mid_idx + 1, end_idx, cmprator)
        merge(elemlist, start_idx, mid_idx, end_idx, cmprator)

def main(argv=None):
    try:
        input = algo.sort.utils.build_args(argv)
    except ex.exceptions.ValidationError:
        return(2)
    global DEBUG
    DEBUG = int(input['debug'])
    find_inversions(input['list'])
    return(0)

if __name__ == "__main__":
    sys.exit(main())
