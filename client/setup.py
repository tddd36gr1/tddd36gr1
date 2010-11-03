#! /usr/bin/python2.5

'''
    Setup script, setup.py, is used to create installable packet from Python project.
    For more information see http://docs.python.org/distutils/setupscript.html
    
    This script with Makefile is used to generate the Debian package.
'''

from distutils.core import setup
import os, os.path;


# Source directory.
source_dir = 'src';

# Executables. These files will be installed into bin folder (example /usr/local/bin).
scripts = ['src/hello_world.py']

# Included packages from source directory.
packages = ['']

package_dir = {'' : source_dir}
    
def path_to_package(base_dir, path):
    '''
        Convert directory path to package name. 
    '''
    head, tail = os.path.split(path)
    
    if head == '' or head == base_dir:
        return tail
    else:
        return path_to_package(base_dir, head) + "." + tail


'''
    Append all packages from source_dir ('src'). 
'''
for dirpath, dirnames, filenames in os.walk(source_dir):
    if "__init__.py" in filenames:
        packages.append(path_to_package(source_dir, dirpath))


setup(
    name = 'client',
    version = '0.1',
    author = '',
    
    packages = packages,
    package_dir = package_dir,
    scripts = scripts,
    data_files=[]
    
)

