#!/usr/bin/env python

import ex.exceptions
import lib.utils
import lib.dumper
import sys
from optparse import OptionParser

DEBUG = 0

def find_missing_elem(numlist_bin, curr_bit = 0, elem_bit_str = ''):
    if DEBUG:
        print "----------------"
        print(dumper.dump(numlist_bin))
        print "dataset_size      " + str(len(numlist_bin))
        print "curr_bit          " + str(curr_bit)
        print "curr_elem_bit_str " + elem_bit_str

    if (len(numlist_bin) == 1):
        working_bit = len(numlist_bin[0]) - curr_bit - 1
        missing_elem_bit = int(numlist_bin[0][working_bit]) ^ 1;
        elem_bit_str = str(missing_elem_bit) + elem_bit_str 
        return elem_bit_str

    zero_list = []
    one_list = []
    working_bit = len(numlist_bin[0]) - curr_bit - 1

    for elem in numlist_bin:
        if (elem[working_bit] == '0'):
            zero_list.append(elem)
        else:
            one_list.append(elem)

    missing_elem_bit = -1
    if (len(zero_list) > len(one_list)):
        missing_elem_bit = 1
        if DEBUG:
            print "Deleting zeros list"
        [ numlist_bin.remove(x) for x in zero_list ]
    else:
        missing_elem_bit = 0
        if DEBUG:
            print "Deleting ones list"
        [ numlist_bin.remove(x) for x in one_list ]
    
    elem_bit_str = str(missing_elem_bit) + elem_bit_str
    elem_bit_str = find_missing_elem(numlist_bin, 
                                     curr_bit + 1, 
                                     elem_bit_str)
    return elem_bit_str

def remove_elem(numlist_bin, exclude_int_bin = None):
    if exclude_int_bin == None:
        import random
        exclude_int_bin = random.choice(numlist_bin)
    numlist_bin.remove(exclude_int_bin)
    return {
        'exclude_int'     : lib.utils.bin2dec(exclude_int_bin),
        'exclude_int_bin' : exclude_int_bin,
    }

def prepare_list(numrange, bitlen):
    numlist = range(numrange)
    import random
    random.shuffle(numlist)
    lib.utils.xform_list(numlist, lib.utils.dec2bin)
    numlist_bin = [ lib.utils.bin_fmt(x, bitlen) for x in \
                    numlist ]
    return {
        'numlist'         : numlist,
        'numlist_bin'     : numlist_bin,
    }

def main():
    parser = OptionParser()
    parser.add_option("-r", "--range", dest="numrange",
                      help="input int numrange")
    parser.add_option("-d", "--debug", dest="debug",
                      default = 0,
                      help="turn debugging on/off")

    (options, args) = parser.parse_args()

    if (options.numrange is None):
        raise ex.exceptions.NoArgError("no numrange provided")

    numrange = options.numrange
    one_idx = lib.utils.chk_pow_2(numrange)
    if one_idx == -1:
        raise ex.exceptions.BadArgError("numrange should be power of 2");
    bitlen = one_idx

    global DEBUG
    DEBUG = options.debug
    
    try:
        numrange = lib.utils.xform_elem(numrange, int)
    except ex.exceptions.ValidationError as e:
        raise ex.exceptions.ValidationError(e.message)
        return(2)

    try:
        list_data = prepare_list(numrange, bitlen)
    except ex.exceptions.ValidationError as e:
        raise ex.exceptions.ValidationError(e.message)
        return(2)

    try:
        missing_elem_data = remove_elem(list_data['numlist_bin'])
    except ex.exceptions.ValidationError as e:
        raise ex.exceptions.ValidationError(e.message)
        return(2)

    print "STATUS: excluding " +\
          str(missing_elem_data['exclude_int']) +\
          " => " + missing_elem_data['exclude_int_bin']

    if DEBUG:
        print "Randomly shuffled search list: "
        print(dumper.dump(list_data['numlist_bin']))

    found_missing_elem = find_missing_elem(list_data['numlist_bin'])
    found_missing_elem = lib.utils.bin2dec(found_missing_elem)

    if missing_elem_data['exclude_int'] != found_missing_elem:
        print "FAILURE: Target " +\
              str(missing_elem_data['exclude_int']) +\
              " != Found " + str(found_missing_elem)
    else:
        print "SUCCESS: Target " +\
              str(missing_elem_data['exclude_int']) +\
              " == Found " + str(found_missing_elem)

if __name__ == "__main__":
    sys.exit(main())
