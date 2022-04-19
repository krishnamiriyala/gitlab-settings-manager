wheel:
	rm dist/*.whl
	python setup.py bdist_wheel --universal

reinstall: uninstall clean install

install: wheel
	sudo pip3 install dist/*.whl

uninstall:
	sudo pip3 uninstall dist/*.whl

lint:
	pyflakes gitlab_settings_manager/*.py
	pycodestyle gitlab_settings_manager/*.py
	pylint gitlab_settings_manager/*.py

clean:
	rm -rf ./build ./*egg-info*
