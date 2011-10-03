#!/usr/bin/env python

import sys
import random
import os

import lib.utils
import ex.exceptions

import pprint
pp = pprint.PrettyPrinter()

# options overridden by cmdline
DEBUG = 0
def_numrange = 10
def_vals = {
    'elemlist' : [],
    'numrange' : def_numrange
}
call_vals = dict(def_vals)

# dump output options
progname = sys.argv[0] or 'stability_chkr.py'
def_dump_parent_dir = progname.split('.')[0] + "-dump"
def_pre_filename = 'pre'
def_post_filename = 'post'
runcount = 0

def create_dump_env():
    if os.path.exists(def_dump_parent_dir):
        import shutil
        shutil.rmtree(def_dump_parent_dir)
    os.makedirs(def_dump_parent_dir)

def dump_output(fmt_orig_list, fmt_pre_list, fmt_post_list):
    global runcount
    dump_dir = os.path.join(def_dump_parent_dir, str(runcount))
    if not os.path.exists(dump_dir):
        os.makedirs(dump_dir)

    pre_file = os.path.join(dump_dir, def_pre_filename)
    pre_f = open(pre_file, 'w')
    pre_f.write(fmt_orig_list + '\n')
    pre_f.write(fmt_pre_list + '\n')
    pre_f.close()

    post_file = os.path.join(dump_dir, def_post_filename)
    post_f = open(post_file, 'w')
    post_f.write(fmt_orig_list + '\n')
    post_f.write(fmt_post_list + '\n')
    post_f.close()

    return dump_dir

def build_key_dict(elemlist=[]):
    """ 
    build a dictionary which allows for key repetition
    by appending new values instead of over-writing old ones
    """
    rep_key_dict = {}
    if len(elemlist) == 0:
        return(rep_key_dict)

    for elem in elemlist:
        if elem[0] in rep_key_dict:
            rep_key_dict[elem[0]].append(elem[1])
        else:
            rep_key_dict[elem[0]] = [elem[1]]
    return(rep_key_dict)


def test_input_stability(sorting_func, assumed_stability, **kwargs):
    """ 
    For the given element list and sorting function, return
    whether the sorting function is stable on the given list.
    If no list provided, does random sampling on a range
    => may return true on one dataset and false on another. 
    Best used for checking if the sort is stable on the given input
    """
    # Get the input 
    call_vals.update(kwargs)
    elemlist = call_vals['elemlist']
    user_supplied_input = True

    # Generate sample data set in numrange
    if len(elemlist) == 0:
        user_supplied_input = False
        elemlist = range(kwargs['numrange'])
        random.shuffle(elemlist)

    backup_elemlist = list(elemlist)# for sending back to user if req

    if DEBUG:
        print "------original list---------"
        print elemlist

    # Create elemlist [value, unique_key] for the sample data set 
    elemlist = [[elemlist[idx],idx] for idx in range(len(elemlist))]

    # Decide which are the indices of elemlist whose "value" 
    # will be changed to previous element's "value" - the 
    # data set necessary for stability checking

    if not user_supplied_input:
        sampling_range = range(1, len(elemlist) - 1)
        idx_vals_to_chg = random.sample(sampling_range, \
                                        len(sampling_range) / 2)

        for idx in idx_vals_to_chg:\
        elemlist[idx][0] = elemlist[idx-1][0]

        backup_elemlist = [elemlist[x][0] for\
                           x in range(len(elemlist))]

    backup_elemlist_with_rep = list(elemlist)

    if DEBUG:
        print "-----------list with repetition--------"
        print elemlist
    
    # Build a dictionary out of the current element list using 
    # first element as key and second element as value. 
    pre_dict = build_key_dict(elemlist)

    # Pre-sort: remember the sequence of appearance of the 
    # elements which have same "value" but different key
    #pre_rep_elemlist = \
    pre_rep_elemlist = [ {x : pre_dict[x]}\
                          for x in backup_elemlist]

    if DEBUG:
        print "----------before---------"
        print pre_rep_elemlist
    
    # sort it
    sorting_func(elemlist, lambda x,y : x[0] - y[0])
    
    # Post-sort: extract the sequence of appearance of the 
    # elements which have same "value" but different key
    post_dict = build_key_dict(elemlist)
    post_rep_elemlist = [ {x : post_dict[x]} \
                          for x in backup_elemlist]

    if DEBUG:
        print "----------after---------"
        print post_rep_elemlist

    # If the order of appearance of elements which had 
    # same "value" but different key before user's sort == order of 
    # appearance after user's sort => stable else unstable
    verified_stability = (pre_rep_elemlist == post_rep_elemlist)

    global runcount
    runcount += 1
    if (assumed_stability is not verified_stability):
        fail_idxs = []
        for idx in range(len(pre_rep_elemlist)):
            if pre_rep_elemlist[idx] != post_rep_elemlist[idx]:
                fail_idxs.append(idx)

        # dump pre and post list in files for user to 
        # diff
        dump_dir = dump_output(str(backup_elemlist), \
                               pp.pformat(pre_rep_elemlist),\
                               pp.pformat(post_rep_elemlist))

        errobj = ex.exceptions.SortStabilityError(
            'Stability assumption failed', 
            [ 
              { 'assumed_stability' : assumed_stability },
              { 'verified_stability': verified_stability },
              { 'orig_list'         : backup_elemlist },
              { 'list_with_rep'     : backup_elemlist_with_rep },
              { 'pre_rep_elemlist'  : pre_rep_elemlist },
              { 'post_rep_elemlist' : post_rep_elemlist },
              { 'pre_diff_post_idxs': fail_idxs },
              { 'dumped_in'         : dump_dir },
            ]            
        )
        raise errobj

def main():
    global DEBUG
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-l", "--list", dest="list",
                      help="Sample input to test stability")
    parser.add_option("-n", "--ntimes", dest="ntimes",
                      default = 1,
                      help="No. of times to sample for random input")
    parser.add_option("-r", "--numrange", dest="numrange",
                      default = def_numrange,
                      help="Range from which random sample is chosen")
    parser.add_option("-m", "--module", dest="module",
                      help="Sort module to use")
    parser.add_option("-d", "--debug", dest="debug",
                      default=DEBUG, help="Turn debugging on/off")
    (options, args) = parser.parse_args()

    # Check mandatory params
    if not (options.module):
        sys.stderr.write("No value provided for module -m")
        parser.print_help()
        return(2)

    # Import the module and get the sort function
    try:
        mod = lib.utils.fqdn_import(options.module)
    except ImportError:
        sys.stderr.write("Failed to load module '"+\
                         options.module + "'\n")
        parser.print_help()
        return(2)

    # Does this module have the sort function ?
    if not hasattr(mod, 'do_sort'):
        sys.stderr.write("Module does not have attribute do_sort\n")
        parser.print_help()
        return(2)

    # Does this module know about it's stability ?
    if not hasattr(mod, 'is_sort_stable'):
        sys.stderr.write("Module does not have attribute "+\
                         "is_sort_stable\n")
        parser.print_help()
        return(2)

    assumed_stability = mod.is_sort_stable()
    sortfunc = mod.do_sort

    # Check optional params
    ntimes = lib.utils.xform_elem(options.ntimes, xformer=int)
    numrange = lib.utils.xform_elem(options.numrange, xformer=int)
    elemlist = []
    if (options.list):
        import re
        elemlist = lib.utils.xform_list(
                   re.split(r'\W+', options.list))    
        del re
    else:
        print "Using random sampling from 0 to " +\
               str(numrange - 1)
    DEBUG = options.debug

    varargs = {
        'elemlist' : elemlist,
        'numrange' : numrange,
    }

    create_dump_env() # create the dir struct to dump o/p if req

    for count in range(ntimes):
        print "-------------------"
        try:
            test_input_stability(sortfunc, assumed_stability,
                                 **varargs)
            print "count " + str(count) + " - Assumption valid"
        except ex.exceptions.SortStabilityError as e:
            print "count " + str(count) + " - Assumption failed"
            pp.pprint(e.get_errdata())

if __name__ == "__main__":
    sys.exit(main())
