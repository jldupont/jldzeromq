"""
    Created on 2012-01-20
    @author: jldupont
"""
import zmq
import logging
from time import sleep

def run(args):
    """
    :param connec_to:
    :param topics:
    """
    connect_to=args.connect_to
    
    try:
        ctx = zmq.Context()
        s = ctx.socket(zmq.SUB)
        s.connect(connect_to)
    except Exception:
        raise Exception("Can't connect a socket to address: %s" % connect_to)
    
    try:
        for topic in args.topics:
            s.setsockopt(zmq.SUBSCRIBE, topic)
            logging.info("subscribed to topic: %s" % topic)
    except:
        raise Exception("Error subscribing to topic '%s'" % topic)
    
    logging.info("Starting loop...")
    while True:
        topic, msg = s.recv_multipart()
        logging.info('Topic: %s, msg:%s' % (topic, msg))
        sleep(0.1)
    