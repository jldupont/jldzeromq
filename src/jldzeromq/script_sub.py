"""
    Created on 2012-01-20
    @author: jldupont
"""
import os
import zmq
import logging, sys

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
    
    ppid=os.getppid()
    logging.info("Parent pid: %s" % ppid)
    logging.info("Starting loop...")
    while True:
        topic, msg = s.recv_multipart()
        sys.stdout.write('%s: %s' % (topic, msg))
        
        ### protection against broken pipe
        if os.getppid()!=ppid:
            logging.warning("Parent process terminated... exiting")
            break

    