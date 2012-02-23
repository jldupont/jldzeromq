"""
    @author: Jean-Lou Dupont
"""

import logging, sys, os

sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)

name=os.path.basename(sys.argv[0])

FORMAT='%(asctime)s - '+name+' - %(levelname)s - %(message)s'
formatter = logging.Formatter(FORMAT)

logging.basicConfig(level=logging.INFO, format=FORMAT)
