# setup.py
from distutils.core import setup
import py2exe

setup( windows=['AoD.py'], options = {'py2exe': {'packages':['PIL']} } )
