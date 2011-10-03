#!/usr/bin/env python

import unittest

import lib.utils
import ex.exceptions
import algo.sort.stability_chkr

class FindMissingVal(unittest.TestCase):
    modname = 'algo.misc.find_missing_int'
    mod = lib.utils.fqdn_import(modname)

    def smoke_test_find_missing_val(self): 
        """ test ascending sort """
        test_bitlen = 8;
        test_numrange = 2 ** 8;

        list_data = self.mod.prepare_list(test_numrange, test_bitlen)
        numlist_bin = list_data['numlist_bin']
        missing_elem_data = self.mod.remove_elem(numlist_bin)
        found_elem = self.mod.find_missing_elem(numlist_bin)
        found_elem = lib.utils.bin2dec(found_elem)
        self.assertEqual(found_elem, missing_elem_data['exclude_int'])


    def load_test_find_missing_val(self): 
        range_count = 0
        test_bitrange = 10;

        for range_count in range(test_bitrange):
            if range_count < 1:
                continue
            test_bitlen = range_count
            test_numrange = 2 ** range_count
            ntests = int(test_numrange / 2)
            test_count = 0
            while test_count < ntests:
                list_data = self.mod.prepare_list(test_numrange, 
                                                  test_bitlen)
                numlist_bin = list_data['numlist_bin']
                missing_elem_data = self.mod.remove_elem(numlist_bin)
                found_elem = self.mod.find_missing_elem(numlist_bin)
                found_elem = lib.utils.bin2dec(found_elem)
                self.assertEqual(found_elem, 
                                 missing_elem_data['exclude_int'])
                test_count += 1
            range_count += 1

if __name__ == "__main__":
    unittest.main()
