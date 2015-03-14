import os
import sys

# Add the parent folder to sys.path, in order to be able to import jason
sys.path.insert(0, os.path.abspath('..'))

# Make jason available to all other modules inside the package
import jason
