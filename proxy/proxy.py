from redis_helper import getEngineIdByCaseId
from engine_cluster import getEngineAddress
import logging

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.httpclient
from tornado.web import HTTPError, asynchronous
from tornado.httpclient import HTTPRequest
from tornado.options import define, options
try:
    from tornado.curl_httpclient import CurlAsyncHTTPClient as AsyncHTTPClient
except ImportError:
    from tornado.simple_httpclient import SimpleAsyncHTTPClient as AsyncHTTPClient

define("port", default=8888, help="run on the given port", type=int)
define("api_protocol", default="http")
define("admin_address",default="localhost:8088")
define("debug", default=True, type=bool)

class ProxyHandler(tornado.web.RequestHandler):


    def parseCaseId(self,workitemId):
        caseId=workitemId.split(':')[0]
        if caseId.find('.')!=-1:
            caseId=caseId.split('.')[0]
        return caseId

    @asynchronous
    def get(self):
        # enable API GET request when debugging
        if options.debug:
            return self.post()
        else:
            raise HTTPError(405)


    @asynchronous
    def post(self):
        protocol = options.api_protocol


        workitemId=self.get_argument('workitemId',default=None)
        if workitemId:
            caseId= self.parseCaseId(workitemId)
            engineId=getEngineIdByCaseId(caseId)

            url="http://"+getEngineAddress(engineId)
        else:
            url=options.admin_address

        # update host to destination host
        headers = dict(self.request.headers)
        #headers["Host"] = host

        try:
            AsyncHTTPClient().fetch(
                HTTPRequest(url=url,
                            method="POST",
                            body=self.request.body,
                            headers=headers,
                            follow_redirects=False),
                self._on_proxy)
        except tornado.httpclient.HTTPError, x:
            if hasattr(x, "response") and x.response:
                self._on_proxy(x.response)
            else:
                logging.error("Tornado signalled HTTPError %s", x)

    def _on_proxy(self, response):
        if response.error and not isinstance(response.error,
                                             tornado.httpclient.HTTPError):
            raise HTTPError(500)
        else:
            self.set_status(response.code)
            for header in ("Date", "Cache-Control", "Server", "Content-Type", "Location"):
                v = response.headers.get(header)
                if v:
                    self.set_header(header, v)
            if response.body:
                self.write(response.body)
            self.finish()

def main():
    tornado.options.parse_command_line()
    application = tornado.web.Application([
        (r"/.*", ProxyHandler),
    ])
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
