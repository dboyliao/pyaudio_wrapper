import sys, subprocess, os

if os.path.exists(".temp_install_path.txt"):
    print "Removing the package from your machine."
    try:
        subprocess.call("cat .temp_install_path.txt | xargs rm -rf", shell = True)
        subprocess.call("rm .temp_install_path.txt", shell = True)
        print 'Sucessfully uninstall pyaudio_wrapper...'
        sys.exit(0)
    except Exception as e:
        print "Something goes wrong."
        print e
else:
    print 'Package is not installed yet'