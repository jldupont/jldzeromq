"""
    Created on 2012-01-19
    @author: jldupont
"""
import os

try:
    import zmq
except:
    raise Exception("* package 'pyzmq' is required - get it from Pypi\n")

try:
    import argparse
except:
    raise Exception("* package 'argparse' is necessary - get it from Pypi\n")

