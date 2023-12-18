# Synology application for DSM 7 Web Service - Telegram bots consuming
# Coryright ©2023.12 by Arkadi Joutchenko aka Arabezar aka jaaz

from urllib.parse import parse_qsl
from log_mem import *
import config
import requests
import text

def application(env, start_response):
  global log
  start_response('200 OK', [('Content-Type', 'text/plain')])

  log = Log()
  log.append(text.LOG_APP_STEP_CHECK)
  params = dict(parse_qsl(env['QUERY_STRING']))
  ok1, bot_id = check_param(params, 'tg', config.tokens)
  ok2, chat_id = check_param(params, 'chat_id', config.chat_ids)
  ok3, msg = check_param(params, 'text')

  if ok1 and ok2 and ok3:
    send_message(bot_id, chat_id, msg)
  else:
    log.append(text.LOG_PARAM_ERR_WRONG)
  return [log.print()]

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
  log.append(f"{name}: {param_msg}", 1)
  return is_valid, value

def send_message(bot_id, chat_id, msg):
  log.append(text.LOG_APP_STEP_SEND)
  response = requests.get(f"https://api.telegram.org/bot{config.tokens[bot_id]}/sendMessage?parse_mode=HTML&chat_id={chat_id}&text={msg}")
  log.append(f"{text.LOG_APP_STEP_RESPONSE}: {str(response.json())}")

# Next lines are for testing purposes only
def dummy_response(status, headers):
  pass

if __name__ == "__main__":
  print(application({'QUERY_STRING': f'{config.TEST_QUERY_STR}'}, dummy_response))
