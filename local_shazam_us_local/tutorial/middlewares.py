import base64

class ProxyMiddleware(object):
# overwrite process request
	def process_request(self, request, spider):
	    # Set the location of the proxy
		request.meta['proxy'] = "http://182.253.16.114:8080"
