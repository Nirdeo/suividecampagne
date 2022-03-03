run:
	python3 manage.py runserver

init:
	python3 scripts/init.py
	python3 scripts/upload_themes.py
	python3 scripts/upload_clients.py
	python3 scripts/upload_partners.py