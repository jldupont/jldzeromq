"""
    Created on 2012-01-20
    @author: jldupont
"""
import zmq
import logging, os


def run(sock_pub=None, sock_sub=None):

    try:
        ctx = zmq.Context()
        sp = ctx.socket(zmq.ROUTER)
        sp.bind(sock_pub)
        logging.info("Ready to receive for publishers on socket: %s" % sock_pub)
    except Exception,e:
        raise Exception("Can't bind to socket for publishers: %s => %s" % (sock_pub, str(e)))
    
    try:
        ctx = zmq.Context()
        ss = ctx.socket(zmq.PUB)
        ss.bind(sock_sub)
        logging.info("Ready for subscribers on socket: %s" % sock_sub)        
    except Exception:
        raise Exception("Can't use socket '%s' for subscribers" % sock_sub)

    
    ppid=os.getppid()
    logging.info("Process pid: %s" % os.getpid())
    logging.info("Parent pid : %s" % ppid)
    logging.info("Starting loop...")
    while True:
        
        _, topic, msg = sp.recv_multipart()
        ss.send_multipart([topic, msg])
