from os import path
import subprocess

THIS_FOLDER = path.dirname(path.abspath(__file__))

AWS_USER = 'ubuntu'
AWS_KEY_PATH = '~/.ssh/amazon-ec2-macbookpro.pem'

# TODO(eso) may have to modify the call to fab
#  to allow for ubuntu username and AWS key

def create_session_on_server(host, email):
  return subprocess.check_output(
    [
      'fab',
      'create_session_on_server:email={}'.format(email),
      # '--host={}@{}'.format(AWS_USER, host),
      '--host={}'.format(host),
      # '--i={}'.format(AWS_KEY_PATH),
      '--hide=everything,status',
    ],
    cwd=THIS_FOLDER
  ).decode().strip()

def reset_database(host):
  subprocess.check_call(
    [
      'fab',
      'reset_database',
      # '--host={}@{}'.format(AWS_USER, host)
      '--host={}'.format(host)
    ],
    cwd=THIS_FOLDER
  )
