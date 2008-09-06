#!/usr/bin/env python

""" Backend manager for wicd.

Manages and loads the pluggable backends for wicd.

"""

#
#   Copyright (C) 2007 Adam Blackburn
#   Copyright (C) 2007 Dan O'Reilly
#   Copyright (C) 2007 Byron Hillis
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License Version 2 as
#   published by the Free Software Foundation.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#


import sys
import os

import wicd.wpath as wpath


class BackendManager(object):
    def __init__(self):
        """ Initialize the backend manager. """
        self.backend_dir = wpath.backends
        self.__loaded_backend = None
        
    def _valid_backend_file(self, be_file):
        """ Make sure the backend file is valid. """
        return (os.access(be_file, os.F_OK) and 
                os.path.basename(be_file).startswith("be-") and
                be_file.endswith(".py"))
    
    def get_current_backend(self):
        if self.__loaded_backend and not self.__loaded_backend is None:
            return self.__loaded_backend.NAME
        else:
            return None
    
    def get_available_backends(self):
        """ Returns a list of all valid backends in the backend directory. """
        be_list = [""]
        for f in os.listdir(self.backend_dir):
            if self._valid_backend_file(os.path.join(self.backend_dir, f)):
                be_list.append(f[3:-3])
        return be_list
        
    def load_backend(self, backend_name):
        """ Load and return a backend module. 
        
        Given a backend name be-foo, attempt to load a python module
        in the backends directory called be-foo.py.  The module must
        include a certain set of classes and variables to be considered
        valid.
        
        """
        def fail(backend_name, reason):
            print "Failed to load backend %s: %s" % (backend_name, reason)
            
        print 'trying to load backend %s' % backend_name
        backend_path = os.path.join(self.backend_dir,
                                    'be-' + backend_name + '.py')
        if self._valid_backend_file(backend_path):
            sys.path.insert(0, self.backend_dir)
            backend = __import__('be-' + backend_name)
        else:
            fail(backend_name, 'Invalid backend file.')
            return None
        
        if not backend.NAME:
            fail(backend_name, 'Missing NAME declaration.')
            return None
        
        if not backend.WiredInterface:
            fail(backend_name, "Missing WiredInterface class")
            return None
        
        if not backend.WirelessInterface:
            fail(backend_name, "Missing WirelessInterface class")
            return None

        self.__loaded_backend = backend
        print 'successfully loaded backend %s' % backend_name
        return backend
        