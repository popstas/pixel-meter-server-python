import time
from lib import *
from lib.PixelServer import PixelServer
from lib.PixelServerHandler import PixelServerHandler

def main():
    server = PixelServer(PixelServerHandler, comportname=config['comportname'], tcpport=8035)
    time.sleep(2)
    server.startServer()


if __name__ == '__main__':
    main()

