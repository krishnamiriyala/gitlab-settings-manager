wheel:
	python setup.py bdist_wheel --universal

install: wheel
	sudo pip3 install dist/*.whl

uninstall: wheel
	sudo pip3 uninstall dist/*.whl

clean:
	rm -rf ./*egg-info*
