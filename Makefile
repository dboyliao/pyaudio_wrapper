test:
	nosetest -w . --with-coverage --cover-html --cover-html-dir=tests/reports --no-byte-compile --cover-package=pyaudio_wrapper 2>&1 | tee tests/reports/test_results.txt`

install:
	python setup.py install --record .temp_install_path.txt
	make clean

uninstall:
	cat .temp_install_path.txt | xargs rm -rf && rm .temp_install_path.txt && echo 'Sucessfully uninstall pyaudio_wrapper'

clean:
	rm -rf dist
	rm -rf pyaudio_wrapper.egg-info
	rm -rf build
