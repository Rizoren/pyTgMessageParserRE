CONFIG_TELEGRAM = {
    'api_id': ...,
    'api_hash': '...',
    'username': '...',
}

CONFIG_DB = {
    'base_model': r'schema.sql',
    'tgm_insert_query': "insert or replace into tg_message (id_msg, date_msg, from_author_id, text_msg, tg_group_id) values (?, ?, ?, ?, ?)",
    'tgm_after_insert_query': "delete from tg_message where text_msg is null or text_msg = ''",
    'tgm_export_query': "select '('||id_msg||', '||from_author_id||', '||tg_group_id||') '||date_msg||':\n'||text_msg||'\n' from tg_message",
}

EXPORT_QUERY = {
    'example': r"select id_msg, date_msg, from_author_id, text_msg, tg_group_id from tg_message t"
}
