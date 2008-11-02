#
# This file is a command-module for Dragonfly.
# (c) Copyright 2008 by Christo Butcher
# Licensed under the LGPL, see <http://www.gnu.org/licenses/>
#

"""
Command-module for direct opening of **user-defined targets**
=============================================================

This module offers very easy and direct opening of user-
defined targets.  User define their own targets in the 
configuration file, and then have instant access to them 
by saying "bring me <target>".  The configuration file 
format is described below.

Commands
--------
Command: **"bring me <target>"**
    Open the specified target.
    The *<target>* extra in this rule can be any one
    of the targets defined in this module's configuration file.

Customization
-------------
Users should customize this module by editing its configuration 
file.  In this file they should fill the ``targets.mapping`` 
with their own personal targets.  This target mapping maps *what 
you say* to *which target to open*.

For example:

.. code-block:: python

   targets.mapping = {
       "[my] favorite website": website("http://code.google.com/p/dragonfly"),
       "my local folder":       folder(r"C:\"),
      }

(Note the format of each target: ``"...": type("..."),`` 
And note the use of ``r"..."`` when specifying a path 
containing backslash characters; the *r* in front of the 
open-quote means that backslashes can be given literally 
and *don't* need to be doubled.)

Using the configuration above would allow the user to say:

 - **"bring me my favorite website"** and the Dragonfly homepage
   will be opened.
 - **"bring me my local folder"** and a Windows Explorer
   will be opened showing the local ``C:\`` folder.

"""


#---------------------------------------------------------------------------

import os
import os.path
import webbrowser
import subprocess

from dragonfly.grammar.grammar      import Grammar
from dragonfly.grammar.elements     import Choice
from dragonfly.grammar.compoundrule import CompoundRule
from dragonfly.config               import Config, Section, Item


#---------------------------------------------------------------------------
# Bringable classes.

class BringableBase(object):
    def __init__(self, target):
        self.target = target
    def __repr__(self):
        return "%s(%r)" % (self.__class__.__name__, self.target)
    __str__ = __repr__
    def bring_it(self):
        pass

class website(BringableBase):
    def bring_it(self):
        webbrowser.open(self.target)

class folder(BringableBase):
    def bring_it(self):
        subprocess.Popen(["explorer", self.target])


#---------------------------------------------------------------------------
# Set up this module's configuration.

config = Config("bring me")
config.targets         = Section("Targets section")
config.targets.mapping = Item(
                              default={
                                       "my site": website("http://www.google.com"),
                                      },
                              doc="Mapping of spoken targets to bringable targets.",
                              namespace={
                                         "website": website,
                                         "folder": folder
                                        },
                             )
config.lang            = Section("Language section")
config.lang.bring_me   = Item("bring me <target>",
                              doc="Command to bring a target; must contain the <target> extra.")
config.load()


#---------------------------------------------------------------------------
# Bring rule.

class BringRule(CompoundRule):

    spec = config.lang.bring_me
    extras = [Choice("target", config.targets.mapping)]

    def _process_recognition(self, node, extras):
        target = extras["target"]
        self._log.debug("%s: bringing target %s." % (self, target))
        target.bring_it()


#---------------------------------------------------------------------------
# Create and manage this module's grammar.

grammar = Grammar("bring me")
grammar.add_rule(BringRule())
grammar.load()
def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None
