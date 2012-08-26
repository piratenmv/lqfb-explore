#!/usr/bin/env python2.7
#############################################################################
# Purpose:
#   Export the Postgres database "lqfb" as JSON format.
#
# Usage:
#   exportJSON.py
#
# Files:
#   Expects the Python module "psycopg2". Under Mac OS, use "port install
#   py27-psycopg2".
#
# Author:
#   Niels Lohmann <niels.lohmann@piraten-mv.de>
#############################################################################

import psycopg2
import json
import datetime

# helper to JSONify datetime in ISO format
dthandler = lambda obj: obj.isoformat() if isinstance(obj, datetime.datetime) else None

# connect to database
conn = psycopg2.connect(database="lqfb")
cur = conn.cursor()

# collect list of tables
cur.execute("""SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'""")
tables = list()
for t in cur.fetchall():
    tables.append(t[0])

fulldump = dict()

# traverse tables
for table in tables:
    query = 'SELECT * FROM ' + table + ';'
    cur.execute(query)

    colnames = [desc[0] for desc in cur.description]

    entry = list()

    for record in cur:
        row = dict()
        for i in range(0, len(colnames)):
            row[cur.description[i][0]] = record[i]
        entry.append(row)

    fulldump[table] = {"count": len(entry), "entries": entry}

# output tables as JSON
print(json.dumps(fulldump, default=dthandler, sort_keys=True, indent=2))

# disconnect from database
cur.close()
conn.close()
