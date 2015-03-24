from os import path
import subprocess


THIS_FOLDER = path.dirname(path.abspath(__file__))
AWS_KEY_PATH = '/Users/eso/.ssh/amazon-ec2-macbookpro.pem'


def create_session_on_server(host, email):
  return subprocess.check_output(
    [
      'fab',
      'create_session_on_server:email={}'.format(email),
      '--host={}'.format(host),
      '--hide=everything,status',
      '-i', AWS_KEY_PATH,
    ],
    cwd=THIS_FOLDER
  ).decode().strip()

def reset_database(host):
  subprocess.check_call(
    [
      'fab',
      'reset_database',
      '--host={}'.format(host),
      '-i', AWS_KEY_PATH,
    ],
    cwd=THIS_FOLDER
  )
