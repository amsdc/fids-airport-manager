import os
import sys
import tkinter as tk
import shlex


def unsafe_restart():
    sys.stdout.flush()
    theargs = ('python',) + tuple(shlex.quote(s) for s in sys.argv)
    # print(theargs)
    os.execv(sys.executable, ['python', os.path.split(sys.argv[0])[1]])
    
restart = unsafe_restart
