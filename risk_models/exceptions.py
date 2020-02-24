#!/usr/bin/env python3
# coding: utf-8


TQueryException = 'There is an error with the query interface'


class QueryException(Exception):
    """ {{TQueryException}} """
    pass


TBuiltInFuncNotExistError = 'Built-in_Function does not exist'


class BuiltInFuncNotExistError(QueryException):
    """ {{TBuiltInFuncNotExistError}} """
    pass


TRuleNotExistsException = 'Rule does not exist/has error'


class RuleNotExistsException(QueryException):
    """ {{TRuleNotExistsException}} """
    pass


TReportException = 'Escalation interface error'


class ReportException(Exception):
    """ {{TReportException}} """
    pass
