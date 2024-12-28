# This config is just a template for yours one

tokens = {'my_bot_friendly_name': 'my_bot_token', } # my_bot_friendly_name - URL param tg value

users = {'my_any_nickname': 'my_telegram_user_id', } # my_any_nickname - URL param user value; can be my_telegram_user_id as well

rights = {'my_bot_friendly_name': ['my_any_nickname', ], } # access rights for bots and users above

TEST_QUERY_STR = 'tg=<my_bot_friendly_name>&user=<my_any_nickname|my_telegram_user_id>&text=Hello world!'
