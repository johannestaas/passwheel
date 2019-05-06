from subprocess import Popen, PIPE, check_output


def which(binary):
    return bool(check_output(['which', binary]).strip())


def copy(s):
    if isinstance(s, str):
        s = s.encode('utf8')
    if not which('xclip'):
        print('xclip not installed, cant modify clipboard')
        return None
    Popen(['xclip', '-selection', 'clipboard'], stdin=PIPE).communicate(s)
    return True
