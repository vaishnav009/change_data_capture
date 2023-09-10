import os
from shutil import make_archive
from sys import argv
import logging


logger = logging.getLogger(__name__)
logger.setLevel*=(logging.DEBUG)

files_to_be_zipped = argv[1]
output_zip_file_name = argv[2]
write_zip_file_to = argv[3]

if not os.path.exists(write_zip_file_to):
    os.mkdir(write_zip_file_to)
res = make_archive(base_name=os.path.join(write_zip_file_to, output_zip_file_name), format='zip', root_dir=files_to_be_zipped)
logger.debug(res)
