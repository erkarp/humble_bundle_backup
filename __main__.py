"""
Script to back up approved pdf files in a speficied folder,
along with any mobi, epub, or zip files of the same name and
in the same folder to a specified new location
"""

import fnmatch
import os
import shutil
import sys

try:
    STARTING_DIRECTORY = os.path.dirname(sys.argv[1])
except IndexError:
    print('Missing starting directory')

try:
    TARGET_LOCATION = os.path.dirname(sys.argv[2])
except IndexError:
    print('Missing target location')


FILES_TO_BACKUP = []
OTHER_BOOK_FILES = []

for file in os.listdir(STARTING_DIRECTORY):
    if fnmatch.fnmatch(file, '*.pdf'):
        ANS = input(f'Back up {file}? (yes/no/del/end) ')

        if ANS == 'yes':
            FILES_TO_BACKUP.append(file)
        elif ANS == 'del':
            if input(f'Permenently delete {file}? (yes/no) ') == 'yes':
                os.remove(os.path.join(STARTING_DIRECTORY, file))
                print(f'Deleted {file}')
        elif ANS == 'end':
            break

    elif fnmatch.fnmatch(file, '*.epub') or fnmatch.fnmatch(file, '*.mobi') or fnmatch.fnmatch(file, '*.zip'):
        OTHER_BOOK_FILES.append(file)

for file in FILES_TO_BACKUP:
    file_base_name = file.replace('.pdf', '')
    other_files = []

    for book_file in OTHER_BOOK_FILES:
        if file_base_name in book_file:
            other_files.append(book_file)
            OTHER_BOOK_FILES.remove(book_file)

    if other_files:
        book_path = os.path.join(TARGET_LOCATION, file_base_name)
        os.mkdir(book_path)
        shutil.copy(os.path.join(STARTING_DIRECTORY, file), book_path)

        for other_file in other_files:
            shutil.copy(os.path.join(STARTING_DIRECTORY, other_file), book_path)

    else:
        shutil.copy(os.path.join(STARTING_DIRECTORY, file), TARGET_LOCATION)
