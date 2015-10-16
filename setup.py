#!/usr/bin/env python

import os, sys, subprocess
from setuptools import setup, find_packages, Command
from setuptools.command.install import install
from setuptools.command.develop import develop
import easy_install
from pyaudio_wrapper import __authors__, __version__, __license__


if sys.platform == "win32":
    print "Sorry, I don't know how to install this package on windows."
    print "Though pyaudio and portaudio are cross-platform."
    print "Abort installation."

    sys.exit(1)

def read(fname):
    """
    Read the README.md as long description.
    """

    return open(os.path.join(os.path.dirname(__file__), fname), "r").read()

def find_package_path(package_name):

    try:
        cmd = "cd .. && python -c 'import {0};print {0}.__path__[0]'".format(package_name)
        status = subprocess.call(cmd, stdout = open('/dev/null'), stderr = open("/dev/null"), shell = True)
        package_path = subprocess.check_output(cmd, stderr = open("/dev/null"), shell = True).strip("\n")
        if status != 0:
            return None
        else:
            if 'egg' in package_path:
                return os.path.dirname(package_path)
            else:
                return package_path
    except subprocess.CalledProcessError:
        return None


class install_cmd(install):
    """
    python setup.py install Hack.
    """

    def run(self):
        print "[Info] Installing pyaudio_wrapper."

        try:
            # Try to import pyaudio
            import pyaudio
            audio = pyaudio.PyAudio()
            audio.terminate()

        except ImportError:
            # pyaudio is not installed. Build portaudio and install pyaudio.
            print "[Info] pyaudio is not installed...."
            print "[Info] Installing pyaudio and its dependencies...."
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

        print "[Info] Installing other required packages from requirements.txt"
        subprocess.call('pip install -r requirements.txt', shell = True)
        install.run(self)

        print '[Info] Cleaning up temp files.'
        subprocess.call('rm -rf dist', shell = True)
        subprocess.call('rm -rf pyaudio_wrapper.egg-info', shell = True)
        subprocess.call('rm -rf build', shell = True)

        print "Installation sucess."

class develop_cmd(develop):

    def run(self):
        develop.run(self)

        if self.uninstall:
            package_path = find_package_path("pyaudio_wrapper")
            if package_path is not None:
                print "[Info] Detecting import hook in easy-install.pth"
                print "[Info] Clean import hook."

                pth = os.path.join(os.path.dirname(easy_install.__file__), 'easy-install.pth')

                try:
                    pth_file = open(pth, "r")
                    lines = pth_file.readlines()
                    pth_file.close()
                    to_write = []
                    for line in lines:
                        if not 'pyaudio_wrapper' in line:
                            to_write.append(line)
                    pth_file = open(pth, "w")
                    pth_file.write(''.join(to_write))
                    pth_file.close()
                except Exception as e:
                    print e
                    print "[Error] Cannot clean the import hook."
                    sys.exit(1)


class uninstall_cmd(Command):
    """
    python setup.py uninstall Hack.
    """

    description = "Uninstalling pyaudio_wrapper package."
    user_options = [('force', 'f', 'Runing force mode.')]

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):

        force = self.force is not None

        if self.verbose:
            print '[Info] Uninstalling pyaudio_wrapper...'
            print '[Info] Looking for package directory...'
        
        package_path = find_package_path("pyaudio_wrapper")
        if package_path is not None:
            if self.verbose:
                print '[Info] Package path found: \033[1;36m{}\033[0m'.format(package_path)
                confirm = raw_input("Are you sure to remove this directory (y/[n])? ")
                confirm = 'yes' if confirm.lower() in ['yes', 'y'] else 'no'

                if not confirm == 'yes':
                    print "[Info] Abort uninstallation."
                    sys.exit(1)

                if force:
                    print "[Info] Running command: rm -rf {}".format(package_path)
                    subprocess.call('rm -rf {}'.format(package_path), shell = True)
                else:
                    print "[Info] Running command: rm -r {}".format(package_path)
                    subprocess.call('rm -r {}'.format(package_path), shell = True)
                print "[Info] Sucessfully uninstall pyaudio_wrapper."
            else:
                if force:
                    subprocess.call('rm -rf {}'.format(package_path), shell = True)
                else:
                    subprocess.call('rm -r {}'.format(package_path), shell = True)
        else:
            print "[Error] pyaudio_wrapper has not been installed yet."
            print "[Info] Abort uninstalling process"
            sys.exit(1)


setup(
    name = "pyaudio_wrapper",
    version = ".".join(__version__),
    author = ", ".join(__authors__),
    author_email = "qmalliao@gmail.com",
    description = ("A simple wrapper of PyAudio."),
    long_description = read("README.md"),
    license = __license__,
    keywords = "pyaudio wrapper",
    url = "https://github.com/dboyliao/pyaudio_wrapper",
    packages = find_packages(exclude = ['tests']),
    install_requires = ["pyaudio",
                        "numpy",
                        "scipy",
                        "matplotlib"],
    cmdclass = {'uninstall': uninstall_cmd,
                'install': install_cmd,
                'develop': develop_cmd}
)
