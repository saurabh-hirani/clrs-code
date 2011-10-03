#!/usr/bin/env python

class Process(object):
    _cache = {}

    @classmethod
    def cache(cls, pid, val = None):
        if val is None:
            return cls._cache[pid]
        cls._cache[pid] = val

    def __new__(cls, **kwargs):
        pid = kwargs.get('pid', 0)
        try:
            cached_proc = cls._cache[pid]
            return cached_proc
        except KeyError:
            return super(Process, cls).__new__(cls)

    def __init__(self, **kwargs):
        self._pid = kwargs.get('pid', 0)
        self._name  = kwargs.get('name', '')
        self._priority = kwargs.get('priority', 0)
        Process.cache(self.pid, self)
    
    @property
    def priority(self):
        """ Process priority """
        return self._priority

    @priority.setter
    def priority(self, new_priority):
        self._priority = new_priority
        return True

    @property
    def name(self): return self._name

    @property
    def pid(self): return self._pid

    def id(self):
        return self.pid

    def __repr__(self):
        return self.name+ "[" + str(self.pid) + "]=" +\
               str(self.priority)

