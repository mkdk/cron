import Queue
import threading
import urllib2
import time
import os
from proxy_set import get_proxy


input_file = os.path.join(os.path.abspath(os.path.dirname(__file__)),'proxy.txt')
threads = 10

queue = Queue.Queue()
output = []


class ThreadUrl(threading.Thread):
    """Threaded Url Grab"""
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            proxy_info = self.queue.get()

            try:
                proxy_handler = urllib2.ProxyHandler({'http':proxy_info})
                opener = urllib2.build_opener(proxy_handler)
                opener.addheaders = [('User-agent','Mozilla/5.0')]
                urllib2.install_opener(opener)
                req = urllib2.Request("http://www.google.com")
                sock=urllib2.urlopen(req, timeout= 7)
                rs = sock.read(1000)
                if '<title>Google</title>' in rs:
                    output.append(('0',proxy_info))
                else:
                    raise "Not Google"
            except:
                output.append(('x',proxy_info))
            #signals to queue job is done
            self.queue.task_done()

start = time.time()
def main():

    #spawn a pool of threads, and pass them queue instance
    for i in range(5):
        t = ThreadUrl(queue)
        t.setDaemon(True)
        t.start()
    hosts = [host.strip() for host in open(input_file).readlines()]
    #populate queue with data
    for host in hosts:
        queue.put(host)

    #wait on the queue until everything has been processed
    queue.join()

get_proxy()
print("="*100)
print('wait, try to find good proxy')
print("="*100)
# main()
#
# with open('proxy.txt', 'w') as w:
#     for proxy, host in output:
#         if proxy == '0':
#             w.write(host+'\n')

print("="*100)
print('in proxy.txt now only good proxy')
print("="*100)
print "Elapsed Time: %s" % (time.time() - start)
