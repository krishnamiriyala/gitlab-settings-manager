wheel:
	python setup.py bdist_wheel --universal

reinstall: uninstall install

install: wheel
	sudo pip3 install dist/*.whl

uninstall:
	sudo pip3 uninstall dist/*.whl

clean:
	rm -rf ./*egg-info*
