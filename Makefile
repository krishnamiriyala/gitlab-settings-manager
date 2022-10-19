build:
	python -m build

reinstall: uninstall clean install

install: build
	sudo pip3 install dist/*.whl

uninstall:
	sudo pip3 uninstall -y dist/*.whl

lint:
	addlicense -c "Krishna Miriyala<krishnambm@gmail.com>" -l mit **/*.py
	pyflakes gitlab_settings_manager/*.py
	pycodestyle gitlab_settings_manager/*.py --ignore=E501
	pylint gitlab_settings_manager/*.py -d C0116,C0114,W0703
	yamllint -s gitlab_settings_manager/*.yml

lint_fix:
	autopep8 -i gitlab_settings_manager/*.py

clean:
	rm -rf ./dist ./*egg-info*
