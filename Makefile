.PHONY: patch
patch:
	echo "Making a patch release"
	poetry run bump2version patch

.PHONY: minor
minor:
	echo "Making a minor release"
	poetry run bump2version minor


.PHONY: push
push:
	git push origin master --tags

.PHONY: check
check:
	poetry build
	twine check dist/*


.PHONY: release_test
release_test:
	make check
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*

.PHONY: release_pypi
release_pypi:
	make check
	twine upload dist/*

