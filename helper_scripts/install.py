import sys, os, subprocess

try:
    # Try to import pyaudio
    import pyaudio
    audio = pyaudio.PyAudio()
    audio.terminate()

except ImportError: # pyaudio is not installed. Build portaudio and install pyaudio.

    if sys.platform == 'darwin': # OS X
        # Install portaudio using brew.
        subprocess.call("brew update && brew install portaudio", shell = True)
        _, versions, _ = os.walk("/usr/local/Cellar/portaudio").next()
        current_version = versions[-1]
        subprocess.call('echo [build_ext] > $HOME/.pydistutils.cfg', shell = True)
        subprocess.call('echo include_dirs=/usr/local/Cellar/portaudio/{}/include/ >> $HOME/.pydistutils.cfg'.format(current_version), shell = True)
        subprocess.call('echo library_dirs=/usr/local/Cellar/portaudio/{}/lib/ >> $HOME/.pydistutils.cfg'.format(current_version), shell = True)

        # install pyaudio
        subprocess.call('pip install --allow-external pyaudio --allow-unverified pyaudio pyaudio', shell = True)

    elif sys.platform == "linux2": # ubuntu
        # Install portaudio.
        subprocess.call('apt-get install -y portaudio19-dev', shell = True)
        # Intall pyaudio.
        subprocess.call('apt-get install -y python-pyaudio', shell = True)
    elif sys.platform == 'win32': # Windows
        print "I don't know how to run scipts on windows...."
        sys.exit(1)
