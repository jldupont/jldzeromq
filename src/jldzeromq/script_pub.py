"""
    Created on 2012-01-20
    @author: jldupont
"""
import zmq
import logging,sys,os
from time import sleep

sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)

def run(sock_pub=None):

    try:
        ctx = zmq.Context()
        s = ctx.socket(zmq.PUB)
        s.bind(sock_pub)
        logging.info("Connected to socket: %s" % sock_pub)
    except Exception:
        raise Exception("Can't connect a socket to address: %s" % sock_pub)
    
    ### leave time for subscribers to connect!
    sleep(0.2)

    while True:
        
        iline=sys.stdin.readline()

        try:
            topic, sep, msg=iline.partition(":")
            assert(sep==":")
            assert(len(topic)>0)
        except:
            logging.warning("Invalid format, expecting:  'topic: msg'")
            continue
    
        try:
            s.send_multipart([topic, msg])
        except:
            raise Exception("Error sending on topic '%s': %s" % (topic, msg))
        
    