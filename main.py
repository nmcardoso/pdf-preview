import urllib.request
import os
import shutil
import subprocess

import yaml


def main():
  try:
    shutil.rmtree('output')
  except:
    pass

  try:
    shutil.rmtree('/tmp/pdf')
  except:
    pass

  repos = {}

  with open('files.yaml') as file:
    repos = yaml.load(file, Loader=yaml.FullLoader)
  
  for repo_index, (repo_name, repo_data) in enumerate(repos.items()):
    files = repo_data['files']
    branch = repo_data['branch']
    
    print(f'\nRepository [{repo_index + 1}/{len(repos)}]: {repo_name}')
    
    for file_index, path in enumerate(files):
      print(f'  File [{file_index + 1}/{len(files)}]: {path}')
      
      folder, filename = os.path.split(path)

      pdf_folder = os.path.join('/tmp', 'pdf', repo_name, branch, folder)
      pdf_path = os.path.join(pdf_folder, filename)

      png_folder = os.path.join('output', repo_name, branch, folder)
      command_output = os.path.join(png_folder, '.'.join(filename.split('.')[:-1]))

      if not os.path.exists(png_folder):
        os.makedirs(png_folder)
      if not os.path.exists(pdf_folder):
        os.makedirs(pdf_folder)

      url = f'https://raw.githubusercontent.com/nmcardoso/{repo_name}/{branch}/{path}'
      urllib.request.urlretrieve(url, pdf_path)

      subprocess.run(['pdftoppm', '-png', pdf_path, command_output])
    
    print('\n\n')


if __name__ == '__main__':
  main()
