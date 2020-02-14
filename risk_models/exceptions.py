# coding=utf-8

class QueryException(Exception):
    """ There is an error with the query interface """
    pass


class BuiltInFuncNotExistError(QueryException):
    """ Built-in function does not exist """
    pass


class RuleNotExistsException(QueryException):
    """ Rule does not exist/has error """
    pass


class ReportException(Exception):
    """ Escalation interface error """
    pass
