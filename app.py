# Synology application for DSM 7 Web Service - Telegram bots consuming
# Coryright ©2023.12-2025.01 by Arkadi Joutchenko aka Arabezar aka jaaz

from urllib.parse import parse_qsl, unquote
import logging
import config
import requests
import text
import datetime

log_level = logging.INFO
verbose = False

def application(env, start_response):
  start_response('200 OK', [('Content-Type', 'text/plain')])

  logging.basicConfig(level=log_level, filename="tg.log", encoding="utf-8")
  logging.info(f"{'=' * 50} {datetime.datetime.now()}")

  # log all environment vars
  logging.debug(text.LOG_APP_VAR_ENV)
  if verbose:
    for key, value in env.items():
      logging.debug(f"\t{key}: {value}")
  else:
    logging.info(f"\tREMOTE_ADDR:REMOTE_PORT: QUERY_STRING: {env['REMOTE_ADDR']}:{env['REMOTE_PORT']}: {unquote(env['QUERY_STRING'])}")
    # if env['QUERY_STRING']:
    #   logging.log(log_level, f"\t\tunquoted: {unquote(env['QUERY_STRING'])}")
  
  # log and check all query vars
  logging.debug(text.LOG_APP_VAR_QUERY)
  params = dict(parse_qsl(env['QUERY_STRING']))
  ok1, bot = check_param(params, 'tg', config.tokens)
  ok2, users = check_param(params, 'user', config.users, True)
  ok3, msg = check_param(params, 'text')

  # send message
  if ok1 and ok2 and ok3:
    valid_users = check_rights(bot, users)
    if valid_users:
      send_message(bot, valid_users, msg)
  else:
    logging.error(text.LOG_PARAM_ERR_WRONG)
  return [b' ']

def check_param(params, name, values = None, multi = False):
  is_valid = False
  value = None
  ret = []
  is_defined = name in params
  if is_defined:
    value = str(params[name]).strip()
    is_not_empty = len(value) > 0
    is_valid = is_not_empty
    if is_valid and values:
      if isinstance(values, (dict, list)):
        keys = value.split(',') if multi else [value]
        for val in keys:
          if val in values:
            ret += [values[val]]
          elif isinstance(values, dict):
            if val in values.values():
              ret += [val]
        is_valid = len(ret) > 0
  if not is_defined:
    param_msg = text.LOG_PARAM_ERR_NOT_DEFINED
  elif not is_not_empty:
    param_msg = text.LOG_PARAM_ERR_EMPTY
  elif not is_valid:
    param_msg = f"{value} {text.LOG_PARAM_ERR_NOT_FOUND}"
  else:
    param_msg = value
  logging.debug(f"\t{name}: {unquote(param_msg)}")
  return is_valid, ret if multi and ret else value

def check_rights(bot, users):
  bot_valid_users = [config.users[name] for name in config.rights[bot]]
  valid_users = [user for user in users if user in bot_valid_users]
  if not valid_users:
    logging.error(f"{text.LOG_PARAM_ERR_RIGHTS}: {users}")
  elif len(valid_users) < len(users):
    logging.warning(f"{text.LOG_PARAM_ERR_RIGHTS_SOME}: {[user for user in users if user not in bot_valid_users]}")
  return valid_users

def send_message(bot, users, msg):
  logging.debug(text.LOG_APP_STEP_SEND)
  for user in users:
    response = requests.get(f"https://api.telegram.org/bot{config.tokens[bot]}/sendMessage?parse_mode=HTML&chat_id={user}&text={msg}")
    logging.debug(f"{text.LOG_APP_STEP_RESPONSE}: {str(response.json())}")
    if not response.ok:
      logging.error(f"{text.LOG_APP_STEP_RESPONSE}: {str(response.json()['description'])}")

# Next lines are for testing purposes only
def dummy_response(status, headers):
  pass

if __name__ == "__main__":
  print(application({'REMOTE_ADDR': '192.168.1.1', 'REMOTE_PORT': '11173', 'QUERY_STRING': f'{config.TEST_QUERY_STR}'}, dummy_response))
