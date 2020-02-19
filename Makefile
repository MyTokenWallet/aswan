init:
	pip install -r requirements.txt
	django-admin makemessages -a
	django-admin compilemessages
	docker ps

test:
	py.test tests

.PHONY: init test