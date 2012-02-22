"""
    Created on 2012-01-20
    @author: jldupont
"""
import zmq
import logging,sys,os, json


def run(sock_pub=None, topic=None, json_mode=None, filter_topics=[]):

    try:
        ctx = zmq.Context()
        s = ctx.socket(zmq.PUB)
        s.bind(sock_pub)
        logging.info("Connected to socket: %s" % sock_pub)
    except Exception:
        raise Exception("Can't connect a socket to address: %s" % sock_pub)

    ppid=os.getppid()
    logging.info("Parent pid: %s" % ppid)
    logging.info("Starting loop...")    
    while True:
        
        ### protection against broken pipe
        if os.getppid()!=ppid:
            logging.warning("Parent process terminated... exiting")
            break
        
        iline=sys.stdin.readline().strip()
        
              
        if json_mode:
            try:
                jso=json.loads(iline)
            except:
                logging.warning("Can't decode json from: %s" % iline)
                continue
            
            topic=jso.get("topic", None)
            if topic is None:
                logging.warning("Missing 'topic' key in: %s" % iline)
                continue
            topic=str(topic)
            msg=json.dumps(jso)
        else:
            msg=iline   
            if topic is None:
                try:
                    topic, sep, msg=iline.partition(":")
                    assert(sep==":")
                    assert(len(topic)>0)
                except:
                    logging.warning("Invalid format, expecting:  'topic: msg'")
                    continue

        ## FILTER-OUT
        if topic in filter_topics:
            continue
    
        try:
            s.send_multipart([topic, msg])
        except Exception,e:
            logging.warning("Error sending on topic '%s': %s -- %s" % (topic, msg, str(e)))
        
    