"""
Copyright (c) 2014, Sam Dodrill
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

from structures import *
from utils import *

NAME="Prefix reminder"
DESC="Shows the command prefix"

def initModule(cod):
    cod.addBotCommand("PREFIX", testbotCommand)

def destroyModule(cod):
    cod.delBotCommand("PREFIX")

def testbotCommand(cod, line, splitline, source, destination):
    "Shows command prefix"
    cod.reply(source, destination, "My command prefix is %s" % cod.config["me"]["prefix"])

