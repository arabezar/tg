# Synology application for DSM 7 Web Service - Telegram bots consuming
# Coryright ©2023.12-2024.12 by Arkadi Joutchenko aka Arabezar aka jaaz

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

  logging.basicConfig(level=log_level, filename="tg.log", filemode="a")
  logging.log(log_level, '=' * 50)
  logging.log(log_level, f"{datetime.datetime.now()}")

  # log all environment vars
  logging.debug(text.LOG_APP_VAR_ENV)
  if verbose:
    for key, value in env.items():
      logging.debug(f"\t{key}: {value}")
  else:
    logging.log(log_level, f"\tREMOTE_ADDR:REMOTE_PORT: QUERY_STRING: {env['REMOTE_ADDR']}:{env['REMOTE_PORT']}: {env['QUERY_STRING']}")
  
  # log and check all query vars
  logging.debug(text.LOG_APP_VAR_QUERY)
  params = dict(parse_qsl(env['QUERY_STRING']))
  ok1, bot_id = check_param(params, 'tg', config.tokens)
  ok2, chat_id = check_param(params, 'chat_id', config.chat_ids)
  ok3, msg = check_param(params, 'text')

  # send message
  if ok1 and ok2 and ok3:
    send_message(bot_id, chat_id, msg)
  else:
    logging.error(text.LOG_PARAM_ERR_WRONG)
  return [b' ']

def check_param(params, name, values = None):
  is_valid = False
  value = None
  is_defined = name in params
  if is_defined:
    value = str(params[name]).strip()
    is_not_empty = len(value) > 0
    is_valid = is_not_empty
    if is_valid and values != None:
      if isinstance(values, (dict, list)):
        is_valid = value in values
  if not is_defined:
    param_msg = text.LOG_PARAM_ERR_NOT_DEFINED
  elif not is_not_empty:
    param_msg = text.LOG_PARAM_ERR_EMPTY
  elif not is_valid:
    param_msg = f"{value} {text.LOG_PARAM_ERR_NOT_FOUND}"
  else:
    param_msg = value
  logging.debug(f"\t{name}: {unquote(param_msg)}")
  return is_valid, value

def send_message(bot_id, chat_id, msg):
  logging.debug(text.LOG_APP_STEP_SEND)
  response = requests.get(f"https://api.telegram.org/bot{config.tokens[bot_id]}/sendMessage?parse_mode=HTML&chat_id={chat_id}&text={msg}")
  logging.debug(f"{text.LOG_APP_STEP_RESPONSE}: {str(response.json())}")

# Next lines are for testing purposes only
def dummy_response(status, headers):
  pass

if __name__ == "__main__":
  print(application({'REMOTE_ADDR': '192.168.1.1', 'REMOTE_PORT': '11173', 'QUERY_STRING': f'{config.TEST_QUERY_STR}'}, dummy_response))
