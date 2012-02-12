"""
    Created on 2012-01-20
    @author: jldupont
"""
import zmq
import logging, sys,os

sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)

def run(sock_source=None, topics=None):

    try:
        ctx = zmq.Context()
        s = ctx.socket(zmq.SUB)
        s.connect(sock_source)
    except Exception:
        raise Exception("Can't connect a socket to address: %s" % sock_source)
    
    if topics is None or topics=="":
        logging.info("* Snooping mode engaged")
        topics=["",]
    
    try:
        for topic in topics:
            s.setsockopt(zmq.SUBSCRIBE, topic)
            if topic:
                logging.info("Subscribed to topic: %s" % topic)
    except:
        raise Exception("Error subscribing to topic '%s'" % topic)
    
    logging.info("Starting loop...")
    while True:
        topic, msg = s.recv_multipart()
        sys.stdout.write('%s: %s' % (topic, msg))

    