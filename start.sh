#!/bin/bash
cd django_backend
uv run gunicorn frostgrave_site.wsgi:application --workers 2