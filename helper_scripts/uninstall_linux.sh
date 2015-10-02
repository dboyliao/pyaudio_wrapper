if [ -f ./.temp_install_path.txt ];
	then
		cat .temp_install_path.txt | xargs rm -rf;
		rm .temp_install_path.txt;
		echo 'Sucessfully uninstall pyaudio_wrapper';
		exit 0
fi
echo 'Package is not installed yet'