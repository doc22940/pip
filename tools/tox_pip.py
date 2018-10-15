import os
import shutil
import subprocess
import sys
from glob import glob

VIRTUAL_ENV = os.environ['VIRTUAL_ENV']
TOX_PIP_DIR = os.path.join(VIRTUAL_ENV, 'pip')


def pip(args):
    # First things first, get a recent (stable) version of pip.
    if not os.path.exists(TOX_PIP_DIR):
        subprocess.check_call([sys.executable, '-m', 'pip',
                               '--disable-pip-version-check',
                               'install', '-t', TOX_PIP_DIR,
                               'pip'])
        shutil.rmtree(glob(os.path.join(TOX_PIP_DIR, 'pip-*.dist-info'))[0])
    # And use that version.
    pypath = os.environ.get('PYTHONPATH')
    pypath = pypath.split(os.pathsep) if pypath is not None else []
    pypath.insert(0, TOX_PIP_DIR)
    os.environ['PYTHONPATH'] = os.pathsep.join(pypath)
    subprocess.check_call([sys.executable, '-m', 'pip'] + args)


if __name__ == '__main__':
    pip(sys.argv[1:])
