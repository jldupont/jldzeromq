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
    :param topic:
    :param msg:
    """
    connect_to=args.connect_to
    topic=args.topic
    msg=args.msg
    
    try:
        ctx = zmq.Context()
        s = ctx.socket(zmq.PUB)
        s.bind(connect_to)
        
    except Exception:
        raise Exception("Can't connect a socket to address: %s" % connect_to)
    
    ### leave time for subscribers to connect!
    sleep(0.2)
    
    try:
        s.send_multipart([topic, msg])
        logging.info("Sent to topic '%s': %s" % (topic, msg))
    except:
        raise Exception("Error sending on topic '%s': %s" % (topic, msg))
    