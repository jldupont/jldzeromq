"""
    Created on 2012-01-20
    @author: jldupont
"""
import zmq
import logging,sys,os, json

def extract(json_mode, specified_topic, iline):
    """
    Extracts topic:msg
    """
    if json_mode:
        try:
            jso=json.loads(iline)
        except:
            return ("warning", "Can't decode json from: %s" % iline)
        
        topic=jso.get("topic", None)
        if topic is None:
            return ("warning","Missing 'topic' key in: %s" % iline)

        topic=str(topic)
        msg=json.dumps(jso)
        return ("ok", (topic, msg))
        
    ### other case...
    msg=iline
    if specified_topic is not None:
        return ("ok", (specified_topic, msg))
    
    ### specified_topic not specified...
    try:
        topic, sep, msg=iline.partition(":")
        assert(sep==":")
        assert(len(topic)>0)
        return ("ok", (topic, msg))
    except:
        return ("warning", "Invalid format, expecting:  'topic: msg'")

    
    

def run(sock_fabric=None, specified_topic=None, json_mode=None, filter_topics=[]):

    ctx = zmq.Context()
    
    try:
        s = ctx.socket(zmq.DEALER)
        s.connect(sock_fabric)
        logging.info("Connected to fabric with socket: %s" % sock_fabric)
    except Exception:
        raise Exception("Can't connect to fabric: %s" % sock_fabric)

    ppid=os.getppid()
    logging.info("Process pid: %s" % os.getpid())
    logging.info("Parent pid : %s" % ppid)
    logging.info("Starting loop...")
    while True:
        
        ### protection against broken pipe
        if os.getppid()!=ppid:
            logging.warning("Parent process terminated... exiting")
            break
        
        iline=sys.stdin.readline().strip()
        
        code, maybe_data=extract(json_mode, specified_topic, iline) 
        if not code.startswith("ok"):
            logging.warning(maybe_data)
            continue
        
        topic, msg=maybe_data

        ## FILTER-OUT
        if topic in filter_topics:
            continue
    
        try:
            s.send_multipart([topic, msg])
        except Exception,e:
            logging.warning("Error sending on topic '%s': %s -- %s" % (topic, msg, str(e)))
            
        try:
            sys.stdout.write("%s: %s\n" % (topic, msg))
        except:
            pass

        
    