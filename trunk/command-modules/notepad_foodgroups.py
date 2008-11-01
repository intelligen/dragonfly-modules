﻿#
# This file is a command-module for Dragonfly.
# (c) Copyright 2008 by Christo Butcher
# Licensed under the LGPL, see <http://www.gnu.org/licenses/>
#

"""
Command-module example of **CompoundRule** use
==============================================
This module is a simple example of Dragonfly use.  It 
shows how to use the ``CompoundRule`` class to implement 
very flexible and spoken-form independent commands.

"""


from dragonfly.grammar.grammar       import Grammar
from dragonfly.grammar.context       import AppContext
from dragonfly.grammar.compoundrule  import CompoundRule
from dragonfly.grammar.elements      import Choice, Dictation
from dragonfly.actions.actions       import Text


#---------------------------------------------------------------------------
# Create this module's grammar and the context under which it'll be active.

grammar_context = AppContext(executable="notepad")
grammar = Grammar("notepad_example", context=grammar_context)


#---------------------------------------------------------------------------
# Create a compound rule which demonstrates CompoundRule and Choice types.

class FoodGroupRule(CompoundRule):

    spec   = "(I ate <food> <time> | <time> I ate <food>) [and thought it was <opinion>]"
    time   = {
              "(two days ago | day before yesterday)":  2,
              "yesterday":                              1,
              "today":                                  0,
             }
    food   = {
              "(a Granny Smith | an) apple":  "fruit",
              "an orange":                    "fruit",
              "a hamburger":                  "meat",
              "a [juicy] steak":              "meat",
             }
    extras = [
              Choice("time", time),
              Choice("food", food),
              Dictation("opinion"),
             ]

    def _process_recognition(self, node, extras):
        days_ago  = extras["time"]
        foodgroup = extras["food"]
        day_word = (days_ago == 1 and "day" or "days")
        print "You ate %s %d %s ago." % (foodgroup, days_ago, day_word)
        Text("You ate %s %d %s ago." % (foodgroup, days_ago, day_word)).execute()
        if "opinion" in extras:
            print "You thought it was %s." % (extras["opinion"])
            Text("You thought it was %s." % (extras["opinion"])).execute()

grammar.add_rule(FoodGroupRule())


#---------------------------------------------------------------------------
# Load the grammar instance and define how to unload it.

grammar.load()

# Unload function which will be called by natlink at unload time.
def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None
