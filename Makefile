test:
	nosetest -w . --with-coverage --cover-html --cover-html-dir=tests/reports --no-byte-compile --cover-package=pyaudio_wrapper 2>&1 | tee tests/reports/test_results.txt

develop:
	python setup.py develop
	make clean

develop-clean:
	python setup.py develop --uninstall
	make clean

install:
	python helper_scripts/install.py
	pip install -r requirements.txt
	python setup.py install --record .temp_install_path.txt
	make clean

uninstall:
	python helper_scripts/uninstall.py

clean:
	rm -rf dist
	rm -rf pyaudio_wrapper.egg-info
	rm -rf build
