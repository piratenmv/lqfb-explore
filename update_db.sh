#!/bin/sh
#############################################################################
# Purpose:
#   Import a Liquid Feedback database dump into a local Postgres database
#   with name "lqfn".
#
# Usage:
#   importDump.sh FILE
#
#   FILE: A LQFB database dump, available for instance at
#         https://lqfb.piratenpartei.de/lf/index/download.html or
#         https://lqpp.de/mv/index/download.html
#
# Note:
#   An import of a dump of the Piratenpartei Deutschland can take several
#   minutes.
#
# Files:
#   Expects a Postgres installation. For Mac OS, follow the instructions at
#   http://postgresapp.com/documentation
#
# Author:
#   Niels Lohmann <niels.lohmann@piraten-mv.de>
#############################################################################

# unzip database dump
gunzip -c $1  > db.sql

# reset database
dropdb 'lqfb'
createdb 'lqfb'

# import database dump
psql --file=db.sql --dbname=lqfb --quiet

# delete temp file
rm db.sql
