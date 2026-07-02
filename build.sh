#!/usr/bin/env bash
# exit on error
set -o errexit

# 👇 この行を追加（Poetryの環境に gunicorn を強制的にインストールする）

poetry install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate