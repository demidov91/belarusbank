import sys
import os
PROJ_PATH = os.path.dirname(__file__)

sys.path.insert(0, os.path.join(PROJ_PATH, 'env/lib/python3.4/site-packages/'))
sys.path.insert(0, PROJ_PATH)

from views import app as application


print(123)
