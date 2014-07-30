import time
from lib import PixelServer, PixelServerHandler, config
from lib.PixelServer import PixelServer
from lib.PixelServerHandler import PixelServerHandler
from pubsub import pub

def main():
    server = PixelServer(PixelServerHandler, comportname=config['comportname'], tcpport=8035)
    time.sleep(2)
    server.startServer()
    pub.sendMessage('pixel', val='199', msg='server started', bright='10', source='self')
    time.sleep(2)
    pub.sendMessage('pixel', val='-1')


if __name__ == '__main__':
    main()

