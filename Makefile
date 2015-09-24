test:
	nosetest -w . --with-coverage --cover-html --cover-html-dir=tests/reports --no-byte-compile --cover-package=pyaudio_wrapper 2>&1 | tee tests/reports/test_results.txt

develop:
	python setup.py develop
	make clean

develop-clean:
	python setup.py develop --uninstall

install:
	python setup.py install --record .temp_install_path.txt
	make clean

uninstall:
	/bin/bash helper_scripts/uninstall.sh

clean:
	rm -rf dist
	rm -rf pyaudio_wrapper.egg-info
	rm -rf build
