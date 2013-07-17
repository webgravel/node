#!/usr/bin/env python
import os
import shlex
import sys

sys.path.append('/gravel/pkg/gravel-common')

def main():
    os.chdir(os.path.dirname(os.path.realpath(sys.argv[0])))
    args = shlex.split(os.environ['SSH_ORIGINAL_COMMAND'])
    cmd = args[0]
    if cmd not in os.listdir('command.d'):
        sys.exit('invalid command %s' % cmd)
    os.environ['ACTION'] = cmd
    exec_args = ['sudo', 'command.d/' + cmd] + args[1:]
    os.execvp(exec_args[0], exec_args)

if __name__ == '__main__':
    main()
