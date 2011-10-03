#!/usr/bin/env python

import unittest
import random

import lib.utils
import algo.sort.stability_chkr

class HeapSort(unittest.TestCase):
    modname = 'algo.sort.heap_sort'
    mod = lib.utils.fqdn_import(modname)
    sort_range = 10

    def testAscSort(self): 
        """ test ascending sort """
        elemlist = range(self.sort_range)
        backup_elemlist = list(elemlist)

        """ test asc sort without comparator """
        random.shuffle(elemlist)
        heap = self.mod.build_heap_obj(
            list = elemlist,
            heapsize = len(elemlist)
        )
        self.mod.do_sort(heap)
        self.assertEqual(elemlist, backup_elemlist)

        """ test asc sort with comparator """
        random.shuffle(elemlist)
        cmpfunc = lambda x, y: (x - y)
        heap.cmprator = cmpfunc
        self.mod.do_sort(heap)
        self.assertEqual(elemlist, backup_elemlist)

    def testDescSort(self): 
        """ test descending sort """
        elemlist = range(self.sort_range)
        backup_elemlist = list(elemlist)
        random.shuffle(elemlist)
        heap = self.mod.build_heap_obj(
            list = elemlist,
            heapsize = len(elemlist)
        )
        cmpfunc = lambda x, y: (y - x)
        heap.cmprator = cmpfunc
        self.mod.do_sort(heap)
        self.assertNotEqual(elemlist, backup_elemlist)
        backup_elemlist.reverse()
        self.assertEqual(elemlist, backup_elemlist)

if __name__ == "__main__":
    unittest.main()
