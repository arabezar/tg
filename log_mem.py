app_debug = False

class Log:
  def __init__(self):
    self.log_list = []

  def append(self, text, indent = 0):
    if app_debug:
      self.log_list.append('\t' * indent + text)

  def print(self):
    return ('\n'.join(self.log_list) if app_debug else ' ').encode('ascii', 'replace')
