

_memory = {}

def get_user(chat_id):
    return _memory.get(chat_id)

def set_user(chat_id, user_data):
    _memory[chat_id] = user_data

def delete_user(chat_id):
    if chat_id in _memory:
        del _memory[chat_id]

print(_memory)