test:
	nosetest -w . --with-coverage --cover-html --cover-html-dir=tests/reports --no-byte-compile --cover-package=pyaudio_wrapper 2>&1 | tee tests/reports/test_results.txt

develop:
	python setup.py develop
	make clean

develop-clean:
	python setup.py develop --uninstall
	make clean

install:
	python setup.py install

uninstall:
	python setup.py uninstall

