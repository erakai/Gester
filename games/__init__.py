import sys
from os.path import abspath, join, dirname

# Add the 'src' directory to the Python path
src_dir = abspath(join(dirname(__file__), "..", "src"))
sys.path.append(src_dir)