test:
	nosetest -w . --with-coverage --cover-html --cover-html-dir=tests/reports --no-byte-compile --cover-package=pyaudio_wrapper 2>&1 | tee tests/reports/test_results.txt

test-py3:
	nosetests-3.4 -w . --with-coverage --cover-html --cover-html-dir=tests/reports --no-byte-compile --cover-package=pyaudio_wrapper 2>&1 | tee tests/reports/test_results.txt

# Python2
develop:
	python2 setup.py develop
	make clean

develop-clean:
	python2 setup.py develop --uninstall

install:
	python2 setup.py install

uninstall:
	python2 setup.py uninstall

# Python3
develop-py3:
	python3 setup.py develop
	make clean

develop-clean-py3:
	python3 setup.py develop --uninstall

install-py3:
	python3 setup.py install

uninstall-py3:
	python3 setup.py uninstall

clean:
	rm -rf pyaudio_wrapper.egg-info
	rm -rf dist
	rm -rf build
