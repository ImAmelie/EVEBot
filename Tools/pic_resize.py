import os
import re
from PIL import Image

cur_dir = os.path.abspath(os.path.dirname(__file__))
file_list = os.listdir(cur_dir)

width = 100
height = 200

for file_name in file_list :
    if not (re.fullmatch(r'.*\.png$', file_name) is None) :
        Image.open(file_name).resize((width, height)).save(file_name)
