﻿#
# This file is a command-module for Dragonfly.
# (c) Copyright 2008 by Christo Butcher
# Licensed under the LGPL, see <http://www.gnu.org/licenses/>
#

"""
Command-module for **Firefox**
==============================

This module offers commands to control `Foxit Reader
<http://www.foxitsoftware.com/pdf/rd_intro.php>`_, a free
and lightweight PDF reader.

"""


#---------------------------------------------------------------------------

from dragonfly.all import (Grammar, AppContext, MappingRule, Dictation,
                           Key, Text, Config, Section, Item, get_integer)
Integer = get_integer("en")


#---------------------------------------------------------------------------
# Set up this module's configuration.

config                             = Config("Foxit reader control")
config.lang                        = Section("Language section")
config.lang.new_win                = Item("new (window | win)")
#config.generate_config_file()
config.load()


#---------------------------------------------------------------------------
# Create the main command rule.

class CommandRule(MappingRule):

    mapping  = {
                "zoom in [<n>]":            Key("c-equals:%(n)d"),
                "zoom out [<n>]":           Key("c-hyphen:%(n)d"),
                "zoom [one] hundred":       Key("c-1"),
                "zoom [whole | full] page": Key("c-2"),
                "zoom [page] width":        Key("c-3"),

                "find <text>":              Key("c-f") + Text("%(text)s")
           	                                 + Key("f3"),
                "find next":                Key("f3"),

                "[go to] page <int>":       Key("cs-n") + Text("%(int)d\n"),

                "print file":               Key("c-p"),
                "print setup":              Key("a-f, r"),
               }
    extras   = [
                Integer("n", 1, 10),
                Integer("int", 1, 10000),
                Dictation("text"),
               ]
    defaults = {
                "n": 1,
               }


#---------------------------------------------------------------------------
# Create and load this module's grammar.

context = AppContext(executable="foxitr")
grammar = Grammar("foxit reader", context=context)
grammar.add_rule(CommandRule())
grammar.load()

# Unload function which will be called by natlink at unload time.
def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None
