test:
	nosetest -w . --with-coverage --cover-html --cover-html-dir=tests/reports --no-byte-compile --cover-package=pyaudio_wrapper 2>&1 | tee tests/reports/test_results.txt

develop:
	python setup.py develop
	make clean

develop-clean:
	python setup.py develop --uninstall

install:
	python setup.py install

uninstall:
	python setup.py uninstall

clean:
	rm -rf pyaudio_wrapper.egg-info
	rm -rf dist
	rm -rf build
