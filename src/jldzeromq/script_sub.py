"""
    Created on 2012-01-20
    @author: jldupont
"""
import os, sys, logging
import zmq

def run(sock_source=None, topics=None, 
        topics_filter=None,
        just_msg_mode=None
        ,module=None
        ,function=None
        ,fargs=None):

    try:
        ctx = zmq.Context()
        s = ctx.socket(zmq.SUB)
        s.connect(sock_source)
    except Exception:
        raise Exception("Can't connect a socket to address: %s" % sock_source)
    
    if topics is None or topics=="":
        logging.info("* Snooping mode engaged")
        topics=["",]
    
    if topics_filter is None or topics_filter=="":
        topics_filter=["",]
    
    try:
        for topic in topics:
            s.setsockopt(zmq.SUBSCRIBE, topic)
            if topic:
                logging.info("Subscribed to topic: %s" % topic)
    except:
        raise Exception("Error subscribing to topic '%s'" % topic)
    
    if module is not None and function is not None:
        try:
            from tools_sys import prepare_callable
        except:
            raise Exception("Module 'importlib' is required to use this functionality")
        try:
            _mod, filter_func=prepare_callable(module, function)
        except:
            raise Exception("Couldn't prepare callable function out of '%s.%s'" % (module, function))
        logging.info("* Prepared filter function")
    else:
        filter_func=None
    
    
    ppid=os.getppid()
    logging.info("Process pid: %s" % os.getpid())
    logging.info("Parent pid : %s" % ppid)
    logging.info("Starting loop...")
    while True:
        
        if ppid!=os.getppid():
            logging.warning("Parent terminated... exiting")
            break
        
        topic, msg = s.recv_multipart()
        
        ### filter-out
        if topic in topics_filter:
            continue
        
        if filter_func is not None:
            try:
                topic, msg=filter_func(topic, msg, *fargs)
            except Exception,e:
                raise Exception("Specified callable function caused an error: %s" % str(e))
        
        if topic is not None:
            try:
                if just_msg_mode:
                    sys.stdout.write(msg+"\n")
                else:
                    sys.stdout.write('%s: %s\n' % (topic, msg))
            except:
                raise Exception("Exiting (probably broken pipe on stdout)...")
        
        ### protection against broken pipe
        if os.getppid()!=ppid:
            logging.warning("Parent process terminated... exiting")
            break

    