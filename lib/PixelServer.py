import serial
import os
from serial.tools import list_ports
from BaseHTTPServer import HTTPServer
import threading
from pubsub import pub


class PixelServer:
    def __init__(self, responseHandler, comportname, host='', tcpport=8035):
        self.responseHandler = responseHandler
        self.comportname = comportname
        self.tcpport = tcpport
        self.host = host
        self.comport = self.startPort(self.comportname)
        self.HTTPServer = HTTPServer((self.host, self.tcpport), responseHandler)
        pub.subscribe(self.pixelListener, 'pixel')

    def startPort(self, comport):
        port = serial.Serial(comport)
        port.timeout = 0.5
        pub.sendMessage('comports', comports=self.getPorts(), active=comport)
        return port

    def pixelListener(self, val, msg='', bright='', source=''):
        command = val + "|" + msg + ("|" + bright if bright != "" else "") + "\n"
        self.comport.write(command)

    def getPorts(self):
        if os.name == 'nt':
            # windows
            for i in range(256):
                try:
                    s = serial.Serial(i)
                    s.close()
                    yield 'COM' + str(i + 1)
                except serial.SerialException:
                    pass
        else:
            # unix
            for port in list_ports.comports():
                yield port[0]

    def info(self):
        print self.comport.getSettingsDict()
        print "Serial Terminal on %s [%s, %s%s%s%s%s]" % (
            self.comport.portstr,
            self.comport.baudrate,
            self.comport.bytesize,
            self.comport.parity,
            self.comport.stopbits,
            self.comport.rtscts and ' RTS/CTS' or '',
            self.comport.xonxoff and ' Xon/Xoff' or ''
        )

    def startServer(self):
        try:
            threading.Thread(target=self.HTTPServer.serve_forever).start()
            # self.HTTPServer.serve_forever()
        except KeyboardInterrupt:
            self.HTTPServer.socket.close()
