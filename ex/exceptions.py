#!/usr/bin/env python

class BaseError(Exception):
    def __init__(self, msg=''):
        self.message = msg
        Exception.__init__(self,msg)

    def __repr__(self):
        return '%s - %s' % (self.__class__.__name__,self.message)

    __str__ = __repr__

class ValidationError(BaseError): pass
class NoArgError(ValidationError): pass
class EmptyArgError(ValidationError): pass
class BadArgError(ValidationError): pass

class HeapError(BaseError):
   def __init__(self, msg='', errdata = {}):
        super(HeapError, self).__init__(msg)
        if len(errdata) > 0:
            self.errdata = errdata
   def get_errdata(self):
        return self.errdata
class HeapSizeZero(HeapError): pass
class DupElemInsertion(HeapError): pass
class BadIndexAccess(HeapError): pass
class InvalidProcId(HeapError): pass

class SortStabilityError(BaseError):
    def __init__(self, msg='', errdata = {}):
        super(SortStabilityError, self).__init__(msg)
        if len(errdata) > 0:
            self.errdata = errdata
    def get_errdata(self):
        return self.errdata
