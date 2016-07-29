import base64

class ProxyMiddleware(object):
# overwrite process request
	def process_request(self, request, spider):
		request.meta['proxy'] = "http://109.196.127.35:8888"
