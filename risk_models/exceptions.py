#!/usr/bin/env python3
# coding: utf-8
from django.utils.translation import gettext_lazy as _

TQueryException=_('There is an error with the query interface')
class QueryException(Exception):
    """ {{TQueryException}} """
    pass

TBuiltInFuncNotExistError=_('Built-in function does not exist')
class BuiltInFuncNotExistError(QueryException):
    """ {{TBuiltInFuncNotExistError}} """
    pass

TRuleNotExistsException=_('Rule does not exist/has error')
class RuleNotExistsException(QueryException):
    """ {{TRuleNotExistsException}} """
    pass

TReportException=_('Escalation interface error')
class ReportException(Exception):
    """ {{TReportException}} """
    pass
