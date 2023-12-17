# Synology application for DSM 7 Web Service - Telegram bots consuming
# Coryright ©2023.12 by Arkadi Joutchenko aka Arabezar aka jaaz

from urllib.parse import parse_qsl
from log_mem import *
import config
import requests

def application(env, start_response):
  global log
  start_response('200 OK', [('Content-Type', 'text/plain')])

  log = Log()
  log.append("Checking parameters...")
  params = dict(parse_qsl(env['QUERY_STRING']))
  ok = check_param(params, 'tg')
  ok = check_param(params, 'chat_id') and ok
  ok = check_param(params, 'text') and ok

  if ok:
    send_message(params['tg'], params['chat_id'], params['text'])
  else:
    log.append("Not all params are specified. No sending performed.")
  return [log.print()]

def check_param(params, name):
  ok = name in params
  log.append(f"{name}: {params[name] if ok else 'None'}", 1)
  return ok

def send_message(bot_id, chat_id, text):
  log.append("Sending message...")
  if bot_id in config.tokens and chat_id in config.chat_ids and text != '':
    response = requests.get(f"https://api.telegram.org/bot{config.tokens[bot_id]}/sendMessage?parse_mode=HTML&chat_id={chat_id}&text={text}")
    log.append(f"Response: {str(response.json())}", 1)
  else:
    log.append("Specified bot and user ids should be defined in config, also text should be not blank.", 1)

# Next lines are for testing purposes only
def dummy_response(status, headers):
  pass

if __name__ == "__main__":
  print(application({'QUERY_STRING': f'{config.TEST_QUERY_STR}'}, dummy_response))
