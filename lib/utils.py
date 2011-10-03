#!/usr/bin/env python

import ex.exceptions

def char_generator(start = 'a', end = 'z'):
    for num in xrange(ord(start), ord(end) + 1):
        yield chr(num)

def fqdn_import(name):
    mod = __import__(name)
    components = name.split('.')
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod

def is_number(n):
    """ Check if the argument is a number """
    try:
        float(n)
        return True
    except:
        return False

def_xformer = float
def_integrity_chkr = is_number

def get_def_cmprator():
    return lambda x, y: (x-y)

def xform_elem(elem, xformer = def_xformer, \
               integrity_chkr = def_integrity_chkr):
    if (elem is None or elem == ''):
        raise ex.exceptions.EmptyArgError('Empty elem provided')

    if not integrity_chkr(elem):
        err = "Integrity check - (" + \
              str(integrity_chkr.func_doc).strip() + \
              ")" + " - failed on value '" + str(elem) + "'"
        raise ex.exceptions.BadArgError(err)

    return xformer(elem)

def xform_list(elemlist, xformer = def_xformer, \
               integrity_chkr = def_integrity_chkr):
    if (len(elemlist) == 0):
        raise ex.exceptions.EmptyArgError('Empty list provided')

    for idx in range(len(elemlist)):
        try:
            xformed = xform_elem(elemlist[idx], xformer,\
                                 integrity_chkr)
            elemlist[idx] = xformed
        except ex.exceptions.ValidationError as e:
            err = "Index [" + str(idx) + "] - " + e.message  
            raise ex.exceptions.BadArgError(err)
    return 1

def get_valid_num_conversions():
    return dict(
        dec = {
          'bin' : {
            'converter' : dec2bin,
            'formatter' : bin_fmt
          }
        },
        bin = {
          'dec' : {
            'converter' : bin2dec,
            'formatter' : dec_fmt
          }
        }
    )

def chk_pow_2(num):
    count = 0
    binstr = dec2bin(num)
    binstr_len = len(binstr)
    one_idx = -1

    while count < binstr_len:
        if binstr[count] == '1':
            if one_idx > 0:
                one_idx = -1
                break
            one_idx = binstr_len - count
        count += 1
    return one_idx

def dec_fmt(num): 
    return num

def bin2dec(binstr):
    binlist = list(binstr)
    curr_power = 0
    dec_num = 0

    for bit in binlist[::-1]:
        dec_num += int(bit) * (2 ** curr_power)
        curr_power += 1

    return dec_num

def bin_fmt(binstr, bitlen = 32):
    if bitlen < len(binstr):
        return binstr[-1 : len(binstr) - bitlen - 1 : -1]
    return binstr.zfill(bitlen)
    
    # zfill one liner replaces:
    # bitmask = "0" * bitlen
    # nonmasked = bitlen - len(binstr)
    # return bitmask[0 : nonmasked + 1] + binstr

def dec2bin(num, result = ''):
    try: 
        num = xform_elem(num, int)
    except ex.exceptions.ValidationError as e:    
        raise ex.exceptions.ValidationError(e.message)

    if (num == 0):
        if result == '':
            result = '0'
        return result[::-1]

    quot = num / 2
    rem = num % 2
    result += str(rem)

    result = dec2bin(quot, result)

    return result
