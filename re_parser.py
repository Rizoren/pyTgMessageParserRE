import argparse
import re
import sqlite3 as sql


def empty_fnc(*args, **kwargs):
    ''' Empty function for using as default function if not exist in REGEX_MAP items '''
    pass
    
    
def custom_function(row, attr):
    ''' Example custom function for processing attribute '''
    c_result = row[0]
    return row[1], attr, c_result
    

def post_function(row, data):
    ''' Some function for additional changes in data '''
    ...

# Attribute names set
ATTR_SET = {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i'}

# Groups of attribute names
ATTR_GROUP = {
    'A': ('a','b','c'),
    'B': ('d','e','f'),
    'C': ('g','h','i')
}

# Model of attribute with rules of processing
REGEX_MAP = {
    'a': {                                          # - name attribute
        're': [                                     # - set array RE expressions for search attribute
            r'example_re_expression_1'
        ],
        're_flags': re.MULTILINE | re.IGNORECASE,   # - set RE flags
        'max_match_count': 1,                       # - set result array size
        'type': 'str',                              # - set result type: str | num | int
        'len': 1,                                   # - this key need if set result length, for str result type
        'for_first': True                           # - this key need if the result is the first element of result array
        'flag': True,                               # - this key need if the result is the fact of finding
        'custom_fnc': custom_function               # - custom function for processing attribute
        'post_custom_fnc': post_function            # - custom function for attribute postprocessing 
    }
}

ap = argparse.ArgumentParser()

ap.add_argument('-db', '-database', required=True,
                help='DB file path')
ap.add_argument('--clr', '--clear', action='store_true',
                help='Clear previous parsed data')

args = ap.parse_args()

conn = sql.connect(args.db)
cur = conn.cursor()


def parse(data, attr):
    ''' Function for message parse use items from ATTR_SET and REGEX_MAP '''
    result_data = []
    for row in data:
        max_mc = REGEX_MAP[attr].get('max_match_count', 0)
        result_type = REGEX_MAP[attr].get('type', '')
        result_len = REGEX_MAP[attr].get('len', 0)
        custom_fnc = REGEX_MAP[attr].get('custom_fnc', empty_fnc)
        post_fnc = REGEX_MAP[attr].get('post_custom_fnc', empty_fnc)
        flag_type = REGEX_MAP[attr].get('flag', False)

        if custom_fnc != empty_fnc:
            result_cf = custom_fnc(row, REGEX_MAP[attr], attr)
            if result_cf[2]:
                result_data.append(result_cf)

                if post_fnc != empty_fnc:
                    post_fnc(result_cf, result_data)
        else:
            for regexp in REGEX_MAP[attr]['re']:
                result = re.findall(regexp, row[0], REGEX_MAP[attr].get('re_flags', 0))

                if result and flag_type:
                    result_data.append((row[1], attr, 1))
                    break
                elif result and (max_mc == 0 or (max_mc != 0 and len(result) <= max_mc)):
                    if max_mc == 1:
                        if result_type == 'str' and result_len:
                            result = result[0][:result_len].lower()
                        else:
                            result = result[0]
                        result_data.append((row[1], attr, result))
                        if REGEX_MAP[attr].get('for_first', False):
                            break
                    else:
                        result_data.append((row[1], attr, result))
                        if REGEX_MAP[attr].get('for_first', False):
                            break

            result = None

    return result_data

# Clear attribute table
if args.clr:
    cur.execute("delete from user_attribute")
    conn.commit()

# Get messages from DB
cur.execute("select text_msg, from_author_id from tg_message order by from_author_id, date_msg")
messages = cur.fetchall()

# Processing
for a in ATTR_SET:
    cur.executemany("insert or replace into user_attribute (from_author_id, name_attr, val_attr) values (?, ?, ?)",
                    parse(messages, a))

# Example working with attribute groups, get and save size for each group as new attribute
for k, v in ATTR_GROUP.items():
    cur.execute("SELECT from_author_id, ? name_attr, count(distinct name_attr) cnt_atr FROM user_attribute WHERE name_attr IN (" + ",".join(["?"] * len(v)) + ") group by from_author_id",
                tuple([k]) + v)
    cur.executemany("insert or replace into user_attribute (from_author_id, name_attr, val_attr) values (?, ?, ?)",
                    cur.fetchall())

conn.commit()

print('Done.')
