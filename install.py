# coding: utf-8
import sys

if len(sys.argv) < 2:
    print('ERROR::need kbengine assets path, Abort...')
    exit(1)

_INSTALL_PATH = sys.argv[1]
_SRC_PATH = './tips/'

import os
import errno

if 'scripts' not in os.listdir(_INSTALL_PATH):
    print("Error::no install path, must point in kbengine asset "
          "path, Abort...")
    exit(1)


from glob import iglob
from shutil import copyfile as copy

copy_dict = {}

for i in iglob(os.path.join(_INSTALL_PATH, 'scripts', '*/')):
    dir_name = os.path.split(os.path.dirname(i))[1]
    src_path = os.path.join(_SRC_PATH, dir_name, 'KBEngine.py')
    dst_path = os.path.join(i, 'KBEngine.py')

    if not os.path.exists(src_path):
        print('WARNING::src file not found in src: {}'.format(src_path))
        continue

    if not os.path.exists(os.path.dirname(dst_path)):
        print('ERROR::dir not found in dst: {}'.format(dst_path))
        exit(1)
    
    copy_dict[src_path] = dst_path


for a, b in copy_dict.items():
    print('INFO::link "{}" --> "{}"'.format(a, b))
    if os.path.exists(b):
        os.remove(b)

    try:
        os.link(a, b)
    except OSError as e:
        if e.errno == errno.EEXIST:
            os.remove(b)
            os.link(a, b)
        elif e.errno == 18:
            print('WARNING::failed in create link, use copy file')
            copy(a, b)

