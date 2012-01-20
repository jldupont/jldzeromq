#!/usr/bin/env python
"""
    Jean-Lou Dupont's ZeroMQ scripts
    
    Created on 2012-01-19
    @author: jldupont
"""
__author__  ="Jean-Lou Dupont"
__version__ ="0.1.0"


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
                     ],
      package_data = {
                      '':[ "*.gif", "*.png", "*.jpg" ],
                      },
      include_package_data=True,                      
      zip_safe=False
      )
