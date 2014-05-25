import sys
from os.path import join, dirname
__path__.append(join(dirname(__file__), '..', 'config', sys.platform))

from config import config

__all__ = ['PixelServer', 'PixelServerHandler', 'PixelTrayIcon', 'config']