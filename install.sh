#!/bin/sh

createdb --encoding='utf-8' univ6
sudo -u postgres sh -c "psql -c \"CREATE USER rector WITH PASSWORD 'rector';\""
sudo -u postgres sh -c "createdb --encoding='utf-8' university"
chmod 777 univ_zlib.dump
sudo -u postgres sh -c "pg_restore -d university univ_zlib.dump"
