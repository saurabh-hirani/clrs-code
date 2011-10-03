#!/usr/bin/env python

""" Program to implement the priority queue datastructure """

import lib.utils
import ex.exceptions
from ds.heap import Heap

class Max_Pri_Queue:
    def def_elem_key_handler(self, elem):
        return elem

    def __init__(self, **kwargs):
        """ Initialize the Queue """
        list = kwargs.get('list', [])
        cmprator = kwargs.get('cmprator', 
                              lib.utils.get_def_cmprator())
        self._debug = kwargs.get('debug', 0)
        self.elem_key_handler = kwargs.get('elem_key_handler', 
                                           self.def_elem_key_handler)
        self.id_to_idx_map = {}
        self.heap = Heap(
            list = list,
            cmprator = cmprator,
            debug = self._debug
        )
    
    @property
    def debug(self):
        return self._debug
    
    def maximum(self):
        """ Find elem whose key has max val in the queue """
        if not self.heap.heapsize > 0:
            raise ex.exceptions.HeapSizeZero("Heap empty")
        return self.heap.read(0)

    def update_id_idx_map(self, start_idx = 0):
        """ Update the internal id to heap index map """
        heapsize = self.heap.heapsize
        if not start_idx <= heapsize:
            raise ex.exceptions.BadIndexAccess(
                "Cannot go beyond heapsize idx " + str(heapsize)
            )
        curr_idx = start_idx
        while curr_idx < heapsize:
            curr_id = self.heap.read(curr_idx)
            self.id_to_idx_map[curr_id] = curr_idx 
            curr_idx += 1
        return True

    def swap_nodes(self, idx1, idx2):
        """ Swap heap nodes """
        tmp = self.heap.read(idx1)
        self.heap.write(idx1, self.heap.read(idx2))
        self.heap.write(idx2, tmp)
        id1 = self.heap.read(idx1)
        id2 = self.heap.read(idx2)
        self.id_to_idx_map[id1] = idx1
        self.id_to_idx_map[id2] = idx2
        return True

    def update_key(self, id, new_key, op = 'inc'): 
        """ Update key of element from k to new_k 
        provided k > new_k """

        # cannot increase key if heap empty
        idx = self.id_to_idx_map[id]
        heapsize = self.heap.heapsize
        if not heapsize > 0:
            raise ex.exceptions.HeapSizeZero("Heap empty")
        if not idx < heapsize:
            raise ex.exceptions.BadIndexAccess(
                "Accessing - [" + str(idx) + "] > " +\
                "heapsize idx " + str(heapsize - 1)
            )

        # check if heap property violated - if it is - fix it
        if op == 'inc':
            parent_idx = self.heap.get_parent_idx(idx)
            cmprator_out = self.heap.cmprator(
                               self.heap.read(idx), 
                               self.heap.read(parent_idx)
                           )

            while (cmprator_out > 0 and idx >= 0):
                self.swap_nodes(idx, parent_idx) 
                idx = parent_idx
                parent_idx = self.heap.get_parent_idx(idx)
                cmprator_out = self.heap.cmprator(
                                   self.heap.read(idx), 
                                   self.heap.read(parent_idx)
                               )
        else:
            self.heap.max_heapify(idx)
            self.update_id_idx_map(idx)
        return True
    
    def insert(self, id): 
        """ Insert a new element in the queue """
        if id in self.id_to_idx_map:
            raise ex.exceptions.DupElemInsertion(
                "Id " + str(id) + " already exists in queue"
            )
        self.heap.inc_heapsize(1)
        heap_new_idx = self.heap.heapsize - 1
        self.heap.write(heap_new_idx, id)
        self.update_id_idx_map(heap_new_idx)
        self.update_key(id, self.elem_key_handler(id))
        return True
    
    def extract_max(self):
        """ Remove and return elem whose key has max val in queue """
        try:
            max = self.maximum() 
        except ex.exceptions.HeapError as e:
            raise \
            ex.exceptions.HeapError("Cannot extract max - " +\
                                    e.message)

        self.swap_nodes(0, self.heap.heapsize - 1)
        self.heap.dec_heapsize(1)
        self.heap.max_heapify()
        self.update_id_idx_map()
        return max

    def get_iter(self):
        i = 0
        max = self.heap.heapsize
        while i < max:
            yield self.heap.read(i)
            i += 1

    def flush(self):
        count = 0
        while self.heap.heapsize > 0:
            self.extract_max()
            count += 1
        return count
