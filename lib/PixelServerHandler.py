from BaseHTTPServer import BaseHTTPRequestHandler
import urlparse
import time
from pubsub import pub

class PixelServerHandler(BaseHTTPRequestHandler):
    def __init__(self, *args):
        self.server_version = "Pixel server"
        self.loglist = []
        BaseHTTPRequestHandler.__init__(self, *args)

    def __headers(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

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
            #print "send health: "+health
            msg = ""
            if "msg" in q:
                msg = q["msg"][0]
                #print "send msg: "+msg
            bright = ""
            if "b" in q:
                bright = q["b"][0]
                #print "send bright: "+bright
            source = ""
            if "source" in q:
                source = q["source"][0]
            self.loglist.append({
                'time':time.strftime("%d.%m.%Y %H:%M:%S"),
                'val':health,
                'msg':msg.replace("\\", "<br />"),
                'bright':bright,
                'source':source
            })
            pub.sendMessage('pixel', val=health, msg=msg, bright=bright, source=source)

        if path[1] == "log":
            self.wfile.write("<html><head><title>Pixel meter</title></head>")
            self.wfile.write("<body>")
            self.wfile.write('<table border="1" cellpadding="5" cellspacing="0" style="width="80%">')
            self.wfile.write('<tr><td>time</td><td>val</td><td>message</td></tr>')
            #print "log:"
            for event in self.loglist:
                #print event
                self.wfile.write('<tr><td>'+event["time"]+'</td><td>'+event["val"]+'</td><td>'+event["msg"]+'&nbsp;</td></tr>')
            self.wfile.write('</table>')
            #self.wfile.write("<p>parsed: %s</p>" % o)
            #self.wfile.write("<p>url: %s</p>" % url)
            #self.wfile.write("<p>path: %s</p>" % self.path)
            #self.wfile.write("<p>query: %s</p>" % q)

            self.wfile.write("</body></html>")
