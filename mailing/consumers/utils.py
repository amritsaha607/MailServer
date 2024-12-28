from collections import defaultdict

user_to_channel_mappings = defaultdict(list)


def get_channel_list(email):
    return user_to_channel_mappings[email]


def get_group_name(group_id):
    return f'group_{group_id}'
