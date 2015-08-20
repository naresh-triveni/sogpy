from subprocess import call
import shlex, subprocess

def run_command(command):
  print command + " Started "
  args = shlex.split(command)
  process = subprocess.Popen(args,stdout=subprocess.PIPE)
  stdout = process.communicate()[0]
  print command + " Completed "