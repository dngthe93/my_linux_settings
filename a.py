#!/usr/bin/python3


import pwd
import os
import argparse
import subprocess

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--uid', type=int, help='uid of the user. default: current uid')
    args = parser.parse_args()

    uid = args.uid
    if uid is None:
        uid = os.getuid()


    pw = pwd.getpwuid(uid)
    pw_dir = pw.pw_dir

    dirname = './root/home'
    filenames = os.listdir(dirname)
    for filename in filenames:
        fullname = os.path.join(dirname, filename)
        if os.path.isdir(fullname):
            command = 'cp -r %s %s/' % (fullname, pw_dir)
        else:
            command = 'cp %s %s/' % (fullname, pw_dir)

        print(command)
        os.system(command)


    # tmux setting
    try:
        p = subprocess.run(['tmux', '-V'], stdout=subprocess.PIPE)
        tmux_ver = float(p.stdout.decode('utf-8').strip().split()[1])
        print(tmux_ver)
    except FileNotFoundError:
        print("[ ] tmux not found")
        tmux_ver = 0.0

    if tmux_ver >= 2.9:
        tmuxconf = pw_dir + '/.tmux.conf'
        command = 'sed -i "s/window-status-current-bg red/window-status-current-style bg=red/g" ' + tmuxconf
        print(command)
        os.system(command)

    


if __name__ == '__main__':
    main()
