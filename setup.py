#!/usr/bin/env python
"""
    Jean-Lou Dupont's ZeroMQ scripts
    
    Created on 2012-01-19
    @author: jldupont
"""
__author__  ="Jean-Lou Dupont"
__version__ ="0.2.11"

DESC="""
Overview
--------

Collection of 0mq related scripts

* jld0sub: subscribe to topics, output to stdout w/wo JSON
* jld0pub: publish to a topic, input from stdin w/wo JSON
* jld0fabric: fabric to publish/subscribe pattern

"""


from distutils.core import setup
from setuptools import find_packages


setup(name=         'jldzeromq',
      version=      __version__,
      description=  'Collection of ZeroMQ related tools',
      author=       __author__,
      author_email= 'jl@jldupont.com',
      url=          'http://www.systemical.com/doc/opensource/jldzeromq',
      package_dir=  {'': "src",},
      packages=     find_packages("src"),
      scripts=      ['src/scripts/jld0sub',
                     'src/scripts/jld0pub',
                     'src/scripts/jld0fabric',  
                     ],
      zip_safe=False
      ,long_description=DESC
      ,install_requires=[ "pyzmq",
                         ]
      )

#############################################

f=open("latest", "w")
f.write(str(__version__)+"\n")
f.close()

