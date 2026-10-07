#!/bin/bash
# Start the Nii Kpakpo campaign Django dev server
echo "Starting dev server at http://127.0.0.1:8000"
echo "Admin panel:  http://127.0.0.1:8000/admin/"
echo "Login:        admin / admin123"
venv/bin/python manage.py runserver
