import os
import sys


files = list()

for f in os.listdir(sys.argv[1]):
    with open(os.path.join(sys.argv[1], os.path.splitext(f)[0] + '.txt'), 'w'):
        pass


