#!/usr/bin/env python

import ex
from ds.pri_q import Max_Pri_Queue
from ds.process import Process

class Scheduler(object):
    def is_valid_proc_pid(self, pid):
        try:
            Process.cache(pid)
        except KeyError:
            raise ex.exceptions.InvalidProcId(\
                "Process with pid " + str(pid) + " not added to " +\
                "scheduler"
            )
        return True

    def proc_priority(self, entity, new_priority = None):
        try:
            pid = entity.pid
        except AttributeError:
            pid = entity
        if self.is_valid_proc_pid(pid):
            if new_priority is None:
                return Process.cache(pid).priority
            # decide the priority op - inc or dec?
            proc = Process.cache(pid)
            old_priority = proc.priority
            op = 'dec'
            if new_priority > old_priority:
                op = 'inc'
            proc.priority = new_priority
            self.runq.update_key(pid, new_priority, op)
            if self.debug:
                self.dump_runq()
        return True

    def cmp_proc_priority(self, id1, id2):
        if self.is_valid_proc_pid(id1) and \
           self.is_valid_proc_pid(id2):
            return Process.cache(id1).priority - \
                   Process.cache(id2).priority

    def __init__(self, **kwargs):
        self._name = kwargs.get('name', 'scheduler')
        self._debug = kwargs.get('debug', 0)
        self._runq = Max_Pri_Queue(
            cmprator = self.cmp_proc_priority,
            elem_key_handler = self.proc_priority
        )

    @property
    def debug(self):
        return self._debug
        
    @property
    def runq(self):
        return self._runq

    def dump_runq(self):
        q_iter = self.runq.get_iter()
        proc_list = []
        while (1):
            try:
                pid = q_iter.next()
                proc = Process.cache(pid)
                proc_list.append(str(proc))
            except StopIteration:
                break
        if len(proc_list) > 0:
            proc_list.append("\n")
        return ' '.join(proc_list)

    def __repr__(self):
        return self.dump_runq()

    def insert_procs(self, procs):
        for proc in procs:
            self.runq.insert(proc.pid)
            if self.debug:
                print self
        return True

    def read_qualifier_proc(self):
        if self.debug:
            print self
        return Process.cache(self.runq.maximum())

    def extract_qualifier_proc(self):
        max_proc = Process.cache(self.runq.extract_max())
        if self.debug:
            print self
        return max_proc
