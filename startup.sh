cd ecom_site;
python -m gunicorn --bind 0.0.0.0:8000 ecom_site.wsgi;