#!/usr/bin/python3


import pwd
import os
import subprocess
import re
import shutil

def main():
    if shutil.which('batcat') is None:
        raise SystemExit("[!] batcat not found. Run 'sudo apt install bat' and then run this script again.")

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

    # bat theme cache
    command = pw_dir + '/.local/bin/bat cache --build'
    print(command)
    os.system(command)

    # tmux setting
    try:
        p = subprocess.run(['tmux', '-V'], stdout=subprocess.PIPE)
        ver_string = p.stdout.decode('utf-8').strip().split()[1]
        ver_string = re.findall(r'\d+\.\d+', ver_string)[0]
        tmux_ver = tuple(map(int, ver_string.split('.')))
        print(tmux_ver)
    except FileNotFoundError:
        print("[ ] tmux not found")
        tmux_ver = (0, 0)

    if tmux_ver >= (2, 9):
        tmuxconf = pw_dir + '/.tmux.conf'
        command = 'sed -i "s/window-status-current-bg red/window-status-current-style bg=red/g" ' + tmuxconf
        print(command)
        os.system(command)

    if tmux_ver < (3, 8):
        tmuxconf = pw_dir + '/.tmux.conf'
        command = 'sed -i -e "s/dim=50%/bg=colour236,fg=default/g" -e "s/dim=0%/bg=default,fg=default/g" ' + tmuxconf
        print(command)
        os.system(command)


if __name__ == '__main__':
    main()
