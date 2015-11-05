#!/bin/bash

sudo rm lunchroll.db
sudo sqlite3 lunchroll.db < schema.sql
sudo chmod -R 777 /var/www/lunchroll/app
sudo chown -R www-data /var/www/lunchroll/app
