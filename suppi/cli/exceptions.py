# coding: utf-8

from suppi import exceptions as exc


class CliError(exc.SuppiError):
    RETURN_CODE = 4
