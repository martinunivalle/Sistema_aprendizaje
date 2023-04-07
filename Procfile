release: python manage.py migrate
web: daphne Sis_aprendizaje.Sis_aprendizaje.asgi:application --port $PORT --bind 0.0.0.0 -v2
worker: python manage.py runworker channels --settings=Sis_aprendizaje.settings -v2
