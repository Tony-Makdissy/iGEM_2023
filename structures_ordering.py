# https://www.machinelearningplus.com/python/parallel-processing-python/?expand_article=1

import multiprocessing as mp
import time
import os

dir_name = 'test'

# check if a directory exists, if not create it
if not os.path.exists(dir_name):
    os.makedirs(dir_name)

# set the working directory to be dir_name after saving the current working directory
cwd = os.getcwd()
print(os.getcwd())

os.chdir(dir_name)
print(os.getcwd())


# run the script "HDOCKlite-v1.1/hdock" whith arguments 1CGI_r_b.pdb 1CGI_l_b.pdb -out ../test/Hdock.out
# os.system("../HDOCKlite-v1.1/hdock ../HDOCKlite-v1.1/1CGI_r_b.pdb ../HDOCKlite-v1.1/1CGI_l_b.pdb -out Hdock.out")

# os.system("../HDOCKlite-v1.1/createpl Hdock.out top100.pdb -nmax 100 -complex -models")

# go back to cwd
os.chdir(cwd)
print(os.getcwd())