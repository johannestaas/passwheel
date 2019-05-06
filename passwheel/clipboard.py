from subprocess import Popen, PIPE

from .util import has_binary, warning, get_os


def copy(s):
    if isinstance(s, str):
        s = s.encode('utf8')
    if get_os() == 'linux':
        if not has_binary('xclip'):
            warning('xclip not installed, cant modify clipboard')
            return False
        Popen(['xclip', '-selection', 'clipboard'], stdin=PIPE).communicate(s)
        return True
    else:
        warning('passwheel only supports linux for modifying the clipboard')
    return False
