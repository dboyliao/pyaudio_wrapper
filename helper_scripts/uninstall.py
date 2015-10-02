import sys, subprocess

if sys.platform == 'darwin': # OS X
    subprocess.call("/bin/bash ./helper_scripts/uninstall_linux.sh", shell = True)
elif sys.platform == 'linux2': # linux
    subprocess.run("/bin/bash ./helper_scripts/uninstall_linux.sh", shell = True)
else: # Windows
    print "I don't know how to run scipts on windows...."