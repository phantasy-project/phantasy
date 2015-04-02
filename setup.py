'''
Created on 

@author: Guobao Shen
'''
MAJOR = 0
MINOR = 1
MICRO = 0
ISRELEASED = True
VERSION = '%d.%d.%d' % (MAJOR, MINOR, MICRO)

from setuptools import setup, find_packages
setup(name='physutil',
      version=VERSION,
      description='FRIB Python based physics application application toolkit',
      author='Guobao Shen, Dylan Maxwell',
      author_email='shen@frib.msu.edu, maxwelld@frib.msu.edu',
      maintainer = "Guobao Shen",
      maintainer_email = "shen@frib.msu.edu",
      url = 'https"//git.nscl.msu.edu/physapps/physutil.git',
      packages= find_packages(exclude=['utest', 'demo', 'example']),
      classifiers=['Development Status :: 3 - Alpha',
                   'Intended Audience :: Developers',
                   'Programming Language :: Python :: 2.7',
     ],
      install_requires = []
    )
