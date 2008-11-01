#
# This file is a command-module for Dragonfly.
# (c) Copyright 2008 by Christo Butcher
# Licensed under the LGPL, see <http://www.gnu.org/licenses/>
#

"""
Command-module example of **MappingRule** use
=============================================
This module is a simple example of Dragonfly use.  It 
implements several keyboard shortcuts for controlling 
notepad.  This module is a demonstration of the Dragonfly 
library.

Grammars, Contexts, and Rules
-----------------------------
Several key concepts of the Dragonfly library are used
in this module.

*Grammars*
    Grammars are very important in Dragonfly.  They take 
    care of the communication between a command-module and 
    NaturallySpeaking's recognition engine.

    A grammar is in essence a collection of rules.  It 
    contains the rules, loads them into NaturallySpeaking, 
    activates them according to the context, and manages 
    that they process the results of a recognition.

*Contexts*
    Contexts determined when grammars and rules are 
    active.  The commands in this module are for notepad, 
    and the grammar is therefore created with an 
    application context ``AppContext`` that is only
    active when notepad is in the foreground.

*Rules*
    Rules define what can actually be said.  They can be 
    thought of as distinct command utterances.  Rules are 
    built up out of elements, and can form fairly complex 
    structures.  See the Dragonfly documentation for more 
    details on this topic.

    This module uses a mapping rule ``MappingRule`` which 
    maps spoken-forms to Dragonfly actions, namely 
    keystrokes.  This is a common pattern, and the mapping 
    rule takes care of most implementation details.

"""


from dragonfly.grammar.grammar     import Grammar
from dragonfly.grammar.context     import AppContext
from dragonfly.grammar.mappingrule import MappingRule
from dragonfly.grammar.elements    import Dictation
from dragonfly.actions.actions     import Key, Text


#---------------------------------------------------------------------------
# Create this module's grammar and the context under which it'll be active.

grammar_context = AppContext(executable="notepad")
grammar = Grammar("notepad_example", context=grammar_context)


#---------------------------------------------------------------------------
# Create a mapping rule which maps things you can say to actions.
#
# Note the relationship between the *mapping* and *extras* keyword
#  arguments.  The extras is a list of Dragonfly elements which are
#  available to be used in the specs of the mapping.  In this example
#  the Dictation("text")* extra makes it possible to use "<text>"
#  within a mapping spec and "%(text)s" within the associated action.

example_rule = MappingRule(
    name="example",    # The name of the rule.
    mapping={          # The mapping dict: spec -> action.
             "save [file]":            Key("c-s"),
             "save [file] as":         Key("a-f, a"),
             "save [file] as <text>":  Key("a-f, a/20") + Text("%(text)s"),
             "find <text>":            Key("c-f/20") + Text("%(text)s\n"),
            },
    extras=[           # Special elements in the specs of the mapping.
            Dictation("text"),
           ],
    )

# Add the action rule to the grammar instance.
grammar.add_rule(example_rule)


#---------------------------------------------------------------------------
# Load the grammar instance and define how to unload it.

grammar.load()

# Unload function which will be called by natlink at unload time.
def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None
