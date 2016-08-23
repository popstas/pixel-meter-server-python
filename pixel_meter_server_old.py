import serial
import time
import BaseHTTPServer
from BaseHTTPServer import HTTPServer
from BaseHTTPServer import BaseHTTPRequestHandler
import urlparse

logList = []

def main():
    port = startPort('/dev/ttyUSB0')
    time.sleep(2)
    server = startServer('', 8035, port)
    #port.write('199|pixel server\\started\n')
    #port.write('-1\n')
    #port.close()


class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def __init__(self, port, *args):
        self.port = port
        self.server_version = "Pixel server"
        BaseHTTPServer.BaseHTTPRequestHandler.__init__(self, *args)

    def do_HEAD(self):
        self.__headers()

    def do_GET(self):
        url = "http://" + self.address_string() + self.path
        o = urlparse.urlparse(url)
        #print o
        q = urlparse.parse_qs(o.query)
        path = o.path.split('/')

        self.__headers()

        if path[1] == "health":
            health = q["val"][0]
            print "send health: "+health
            msg = ""
            if "msg" in q:
                msg = q["msg"][0]
                print "send msg: "+msg
            bright = ""
            if "b" in q:
                bright = q["b"][0]
                print "send bright: "+bright
            logList.append({ 
                'time':time.strftime("%d.%m.%Y %H:%M:%S"),
                'val':health,
                'msg':msg.replace("\\", "<br />"),
                'bright':bright
            })
            self.port.write(health+"|"+msg+("|"+bright if bright!="" else "")+"\n")

        if path[1] == "log":
            self.wfile.write("<html><head><title>Pixel meter</title></head>")
            self.wfile.write("<body>")
            self.wfile.write('<table border="1" cellpadding="5" cellspacing="0" style="width="80%">')
            self.wfile.write('<tr><td>time</td><td>val</td><td>message</td></tr>')
            #print "log:"
            for event in logList:
                #print event
                self.wfile.write('<tr><td>'+event["time"]+'</td><td>'+event["val"]+'</td><td>'+event["msg"]+'&nbsp;</td></tr>')
            self.wfile.write('</table>')
            #self.wfile.write("<p>parsed: %s</p>" % o)
            #self.wfile.write("<p>url: %s</p>" % url)
            #self.wfile.write("<p>path: %s</p>" % self.path)
            #self.wfile.write("<p>query: %s</p>" % q)

            self.wfile.write("</body></html>")




    def __headers(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()


def startPort(portname):
    port = serial.Serial(portname)
    port.timeout = 0.5
    #info(port)
    return port


def handleRequestsUsing(port):
    return lambda *args: MyHandler(port, *args)


def info(port):
    print port.getSettingsDict()
    print "Serial Terminal on %s [%s, %s%s%s%s%s]" % (
    port.portstr,
    port.baudrate,
    port.bytesize,
    port.parity,
    port.stopbits,
    port.rtscts and ' RTS/CTS' or '',
    port.xonxoff and ' Xon/Xoff' or ''
    )


def startServer(host='', port=8000, comport=''):
    try:
        handler = handleRequestsUsing(comport)
        server = HTTPServer(('', port), handler)
        server.serve_forever()
    except KeyboardInterrupt:
        server.socket.close()
    return server


if __name__ == '__main__':
    main()

