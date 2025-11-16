#!/usr/bin/env python
"""
Small helper to remove problematic migration rows from django_migrations.
Run from the `backend` directory with the same Python environment as your project.

Usage:
    python fix_migrations.py

This will delete all rows with app='admin' from django_migrations. After running it,
run `python manage.py migrate` to apply migrations in the correct order.
"""
import os
import sys
from pathlib import Path

# Ensure project root is on path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'learning_platform.settings')

try:
    import django
    django.setup()
    from django.db import connection

    with connection.cursor() as cur:
        print('Deleting admin migration entries from django_migrations...')
        cur.execute("DELETE FROM django_migrations WHERE app = 'admin';")
        print('Deleted rows (if any).')

    print('Done. Now run: python manage.py migrate')
except Exception as e:
    print('Error:', e)
    sys.exit(1)
