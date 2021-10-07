import argparse
import sqlite3 as sql
import csv
from config import EXPORT_QUERY

ap = argparse.ArgumentParser()

ap.add_argument('-db', '-database', required=True,
                help='DB file path')
ap.add_argument('-exp', '-export', required=True,
                help='Name table or query from config for export into *.csv')
ap.add_argument('--tbl', '-table', action='store_true',
                help='Export object is table')

args = ap.parse_args()

connection = None

try:
    filename = args.db + '_' + args.exp + '.csv'

    connection = sql.connect(args.db)
    cur = connection.cursor()

    if args.tbl:
        cur.execute("select * from " + args.exp)
    else:
        cur.execute(EXPORT_QUERY[args.exp])

    with open(filename, 'w', newline='', encoding='utf-8') as out_csv_file:
        csv_out = csv.writer(out_csv_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
        csv_out.writerow([d[0] for d in cur.description])
        csv_out.writerows(cur.fetchall())
finally:
    if connection:
        connection.close()
    print('Done.')
