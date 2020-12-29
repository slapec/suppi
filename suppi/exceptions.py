# coding: utf-8


class SuppiError(Exception):
    RETURN_CODE = 2


class SettingsModuleError(SuppiError):
    RETURN_CODE = 3
