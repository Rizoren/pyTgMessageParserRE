import argparse
from config import CONFIG_TELEGRAM
import grabber as gr
import database
import dto

ap = argparse.ArgumentParser()

ap.add_argument('-ch', '-channel', required=True,
                help='Telegram group/channel name')
ap.add_argument('-db', '-database', required=True,
                help='DB file path')
ap.add_argument('--dbe', action='store_true',
                help='DB exist flag')
ap.add_argument('--txt', action='store_true',
                help='Export message text into *.txt file flag')

args = ap.parse_args()

db = None

try:
    db = database.DataBase(args.db, args.dbe)

    grabber = gr.GrabberTg()
    grabber.client_init(api_id=CONFIG_TELEGRAM['api_id'],
                        api_hash=CONFIG_TELEGRAM['api_hash'],
                        username=CONFIG_TELEGRAM['username'])
    grabber.client_start()

    print('Getting messages from channel')
    messages = grabber.get_messages(args.ch, dto.tg_message_dto)

    print('Save in DB')
    db.db_save_tg_message_data(messages)

    if args.txt:
        print('Save in txt')
        db.db_export_txt_tg_message_data(args.db + '.txt')
finally:
    if db:
        db.db_close()
    print('Done.')
