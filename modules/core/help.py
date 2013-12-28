"""
Copyright (c) 2013, Sam Dodrill
All rights reserved.

This software is provided 'as-is', without any express or implied
warranty. In no event will the authors be held liable for any damages
arising from the use of this software.

Permission is granted to anyone to use this software for any purpose,
including commercial applications, and to alter it and redistribute it
freely, subject to the following restrictions:

    1. The origin of this software must not be misrepresented; you must not
    claim that you wrote the original software. If you use this software
    in a product, an acknowledgment in the product documentation would be
    appreciated but is not required.

    2. Altered source versions must be plainly marked as such, and must not be
    misrepresented as being the original software.

    3. This notice may not be removed or altered from any source
    distribution.
"""

NAME="Help command"
DESC="Shows commands and does lookups on them."

def initModule(cod):
    cod.addBotCommand("HELP", commandHELP)

def destroyModule(cod):
    cod.delBotCommand("HELP")

def rehash():
    pass

def commandHELP(cod, line, splitline, source, destination):
    """Does help lookups on other commands"""
    if len(splitline) < 2:
        commands = [n.lower() for n in cod.botcommands]
        commands.sort()

        commandlist = " ".join(commands)

        if source.isOper:
            opercmds = [n.lower() for n in cod.opercommands]
            opercmds.sort()

            commandlist = commandlist + \
                " (%s)" % " ".join(opercmds)

        cod.reply(source, destination, "Commands: %s" % commandlist)
    else:
        splitline[1] = splitline[1].upper()
        try:
            assert str(cod.botcommands[splitline[1]].__doc__) != None
            cod.reply(source, destination, "%s: %s" %\
                    (splitline[1], cod.botcommands[splitline[1]][0].__doc__))
        except IndexError:
            try:
                if source.isOper:
                    assert str(cod.botcommands[splitline[1]].__doc__) != "None"
                    cod.reply(source, destination, "%s: %s" %\
                            (splitline[1], cod.botcommands[splitline[1]][0].__doc__))
                else:
                    cod.reply(source, destination, "No help available for %s." % splitline[1])
            except IndexError:
                cod.reply(source, destination, "No help available for %s." % splitline[1])

