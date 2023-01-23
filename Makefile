build: lint
	TZ=UTC git --no-pager show --quiet --abbrev=12 --date='format-local:%Y%m%d%H%M%S' --format="%cd-%h" > VERSION
	python -m build

reinstall: uninstall clean install

install: clean build
	sudo pip3 install dist/*.whl

uninstall:
	sudo pip3 uninstall -y dist/*.whl

lint:
	docker run -it -v ${PWD}:/src ghcr.io/google/addlicense -c "Krishna Miriyala<krishnambm@gmail.com>" -l mit **/*.py
	pyflakes gitlab_settings_manager/*.py
	pycodestyle gitlab_settings_manager/*.py --ignore=E501
	pylint gitlab_settings_manager/*.py -d C0116,C0114,W0703
	yamllint -s gitlab_settings_manager/*.yml

lint_fix:
	autopep8 -i gitlab_settings_manager/*.py

clean:
	rm -rf ./dist ./*egg-info*

publish: clean build install
	twine upload dist/*
