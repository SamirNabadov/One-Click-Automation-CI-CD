import gitlab
import os, sys
import shutil, fileinput
import logging

def connect_gitlab(url, private_token, ssl_verify, api_version):
    if private_token is None:
        private_token = os.environ.get("GITLAB_TOKEN", None)

    gitlab_session = gitlab.Gitlab(url, private_token=private_token, ssl_verify=ssl_verify, api_version=api_version)
    gitlab_session.auth()
    try:
        gitlab_session.version()
    except (gitlab.exceptions.GitlabAuthenticationError):
        raise RuntimeError("Invalid or missing GITLAB_TOKEN")

    logging.info("Connected to: %s", url)
    return gitlab_session

def get_modules(filenname, word, module):
  with open(filenname, 'r') as file:
    lines = file.readlines()
    modules = []
    for line in lines:
      if word in line:
        if module in line:
          continue
        else:
          line = line.split(',')
          line = [i.strip() for i in line][0].split("'")[1]
          modules.append(line)

  return modules

def delete_folder(name):
    for root, dirs, files in os.walk(name):
        for f in files:
            os.unlink(os.path.join(root, f))
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))

def create_folder(name):
    if not os.path.exists(name):
        os.mkdir(name)

def recursive_copy(src, dest):
    for item in os.listdir(src):
        file_path = os.path.join(src, item)
        if os.path.isfile(file_path):
            shutil.copy(file_path, dest)
        elif os.path.isdir(file_path):
            new_dest = os.path.join(dest, item)
            create_folder(new_dest)
            recursive_copy(file_path, new_dest)

def file_copy(src, dest):
    try:
        shutil.copy(src, dest)
        print("File copied successfully.")
    except shutil.SameFileError:
        print("Source and destination represents the same file.")

def replacement(file, previousw, nextw):
    for line in fileinput.input(file, inplace=1):
        line = line.replace(previousw, nextw)
        sys.stdout.write(line)