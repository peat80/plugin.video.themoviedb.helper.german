from xbmcgui import Dialog, DialogProgressBG
from resources.lib.addon.plugin import executebuiltin, get_localized
from resources.lib.addon.logger import kodi_log, kodi_log_traceback
""" Top level module only import plugin/constants/logger """


DIALOG = Dialog()


def kodi_notification(*args, **kwargs):
    return DIALOG.notification(*args, **kwargs)


def kodi_dialog_ok(*args, **kwargs):
    return DIALOG.ok(*args, **kwargs)


def kodi_dialog_yesno(*args, **kwargs):
    return DIALOG.yesno(*args, **kwargs)


def kodi_dialog_multiselect(*args, **kwargs):
    return DIALOG.multiselect(*args, **kwargs)


def kodi_dialog_contextmenu(*args, **kwargs):
    return DIALOG.contextmenu(*args, **kwargs)


def kodi_dialog_input(*args, **kwargs):
    return DIALOG.input(*args, **kwargs)


def kodi_dialog_textviewer(*args, **kwargs):
    return DIALOG.textviewer(*args, **kwargs)


def kodi_traceback(exception, log_msg=None, notification=True, log_level=1):
    if notification:
        head = f'TheMovieDb Helper {get_localized(257)}'
        kodi_notification(head, get_localized(2104))
    kodi_log_traceback(exception, log_msg=log_msg, log_level=log_level)


class ProgressDialog(object):
    """ Wrapper class for using ProgressDialog in with statement """

    def __init__(self, title='', message='', total=100, logging=1):
        self.logging = logging
        self._create(title, message, total)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def _create(self, title='', message='', total=100):
        self._pd = DialogProgressBG()
        self._pd.create(title, message)
        self._count = 0
        self._total = total
        self._title = title
        kodi_log([self._title, ' - 00 ', message], self.logging)
        return self._pd

    def update(self, message='', count=1, total=None):
        if not self._pd:
            return
        if total:  # Reset counter if given new total
            self._count = count
            self._total = total
        self._count += count
        self._progr = (((self._count) * 100) // self._total)
        self._pd.update(self._progr, message=message) if message else self._pd.update(self._progr)
        kodi_log([self._title, ' - ', self._progr, ' ', message], self.logging)
        return self._progr

    def close(self):
        if not self._pd:
            return
        kodi_log([self._title, ' - Done!'], self.logging)
        self._pd.close()


class BusyDialog():
    def __init__(self, is_enabled=True):
        """ ContextManager for timing code blocks and outputing to log """
        if is_enabled:
            executebuiltin('ActivateWindow(busydialognocancel)')
        self.is_enabled = is_enabled

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if not self.is_enabled:
            return
        executebuiltin('Dialog.Close(busydialognocancel)')


def busy_decorator(func):
    def wrapper(*args, **kwargs):
        """ Decorator for BusyDialog around a function """
        with BusyDialog():
            response = func(*args, **kwargs)
        return response
    return wrapper