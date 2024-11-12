pip install -r <(grep -v 'gunicorn' requirements.txt)
python manage.py collectstatic --no-input