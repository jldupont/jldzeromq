"""
    @author: Jean-Lou Dupont
"""

import logging, sys, os

### alignment for program name
ALIGN=15

sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)

name=os.path.basename(sys.argv[0])
fname="%-"+str(ALIGN)+"s" % name

FORMAT='%(asctime)s - '+fname+' - %(levelname)s - %(message)s'
formatter = logging.Formatter(FORMAT)

logging.basicConfig(level=logging.INFO, format=FORMAT)
