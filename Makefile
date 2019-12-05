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

