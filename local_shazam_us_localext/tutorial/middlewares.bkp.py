import base64

class ProxyMiddleware(object):
# overwrite process request
	def process_request(self, request, spider):
	    # Set the location of the proxy
		#request.meta['proxy'] = "http://162.243.93.33:8443" #my digital ocean IP
	    #request.meta['proxy'] = "http://146.185.167.83:8080"
		#request.meta['proxy'] = "http://100.44.118.68:8080"
		#request.meta['proxy'] = "http://1.171.31.239:8998"
		#request.meta['proxy'] = "http://1.163.189.77:8998"
		request.meta['proxy'] = "http://195.177.126.149:8080"
		#try next: 72.167.143.29:60088
        # now i need browser
		# #Use the following lines if your proxy requires authentication
	    # proxy_user_pass = "nounounou:b6o2TnA8RVyeTPk"
	    # #setup basic authentication for the proxy
	    # encoded_user_pass = base64.encodestring(proxy_user_pass)
	    # request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass