messages:
	cd projects; django-admin.py makemessages -l de
	cd projects; django-admin.py compilemessages

test:
	python manage.py test groupcalendar --failfast -v3

coverage:
	coverage run --source='.' manage.py test groupcalendar
	coverage report --omit "manage.py" --show-missing

reinstall:
	rm -f ../../db/db.sqlite3;
	touch ../../db/db.sqlite3;
	chmod 777 ../../db
	chmod 777 ../../db/db.sqlite3
	python manage.py syncdb;
	python manage.py load_example_data
