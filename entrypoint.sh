#!/bin/sh

# ======= Attendre PostgreSQL =======
echo " Waiting for PostgreSQL..."
while ! nc -z $DB_HOST $DB_PORT; do
  sleep 1
done
echo " PostgreSQL is up!"

# ======= Appliquer les migrations =======
echo " Appliquer les migrations..."
python manage.py migrate

# ======= Lancer le serveur Django en arrière-plan =======
echo " Démarrer le serveur Django..."
python manage.py runserver 0.0.0.0:8000 &

# ======= Lancer le worker MQTT au premier plan =======
echo " Démarrer le worker MQTT..."
python manage.py mqtt_worker
