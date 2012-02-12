"""
    Created on 2012-02-12
    @author: jldupont
"""

def dnorm(d):
    """
    Normalize dictionary
    
    >>> dnorm({"SoMeKeY":"  spaces  "})
    {'somekey': 'spaces'}
    """
    r={}
    for e in d:
        try:    r[e.lower()]=d[e].strip()
        except: r[e.lower()]=d[e]
    return r
