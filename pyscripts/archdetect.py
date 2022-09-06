import sys, platform

def retTypeAndMachine():
    # Detect machine and ostype
    ostype = platform.system().lower()
    machine = platform.machine().lower()
    if machine == 'aarch64_be' \
        or machine == 'armv8b' \
        or machine == 'armv8l':
        machine = 'aarch64'
    if machine == 'i386' or machine == 'i686':
        machine = 'x86'
    if machine == "amd64":
        machine = 'x86_64'
    if ostype == 'windows':
        if not machine == 'x86_64':
            sys.stderr.write("Error : Program on windows only support 64bit machine\n")
            return None
    if ostype == 'linux':
        if not (machine == 'aarch64' or \
                machine == 'arm' or \
                machine == 'x86' or \
                machine == 'x86_64'):
            sys.stderr.write("Error : Machine not support your device [%s]\n" %machine)
            return None
    return ostype, machine

