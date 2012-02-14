"""
    Created on 2012-01-20
    @author: jldupont
"""
import zmq
import logging


def run(sock_pub=None, sock_sub=None):

    try:
        ctx = zmq.Context()
        ss = ctx.socket(zmq.SUB)
        ss.connect(sock_sub)
        ss.setsockopt(zmq.SUBSCRIBE, "")
        logging.info("Connected to SUB socket: %s" % sock_sub)
    except Exception:
        raise Exception("Can't connect SUB socket to address: %s" % sock_sub)
    
    try:
        ctx = zmq.Context()
        sp = ctx.socket(zmq.PUB)
        sp.bind(sock_pub)
        logging.info("Connected to PUB socket: %s" % sock_pub)        
    except Exception:
        raise Exception("Can't connect a socket to address: %s" % sock_pub)

    
    logging.info("Starting loop...")
    while True:
        
        topic, msg = ss.recv_multipart()    
        sp.send_multipart([topic, msg])
