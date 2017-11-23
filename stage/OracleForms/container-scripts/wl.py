# Caution: This file is part of the command scripting implementation.
# Do not edit or move this file because this may cause commands and scripts to fail.
# Do not try to reuse the logic in this file or keep copies of this file because this
# could cause your scripts to fail when you upgrade to a different version.
# Copyright (c) 2004,2016, Oracle and/or its affiliates. All rights reserved.

# To import WLST as a Jython module:

# Invoke WLST.
# c:\>java weblogic.WLST
# wls:/(offline)>

# Use the writeIniFile command to convert WLST definitions and method declarations to a .py file.
# wls:/(offline)> writeIniFile("wl.py")
# The Ini file is successfully written to wl.py
# wls:/(offline)>

# Open a new command shell and invoke Jython directly by entering the following command:
# c:\>java org.python.util.jython

# The Jython package manager processes the JAR files in your classpath. The Jython prompt appears:

# >>>

# Import the WLST module into your Jython module using the Jython import command.
# >>>import wl

# Now you can use WLST methods in the module. For example, to connect WLST to a server instance:
# wl.connect('username','password')

"""
This is WLST Module that a user can import into other Jython Modules

"""
from weblogic.management.scripting.utils import WLSTUtil
import sys
origPrompt = sys.ps1
key = 'WLSTMODULE'
theInterpreter = WLSTUtil.ensureInterpreter()
WLSTUtil.ensureWLCtx(theInterpreter)
execfile(WLSTUtil.getWLSTCoreScriptPath())
execfile(WLSTUtil.getWLSTNMScriptPath())
execfile(WLSTUtil.getWLSTScriptPath())
execfile(WLSTUtil.getOfflineWLSTScriptPath())
theInterpreter.set(key, WLS)
WLSTUtil.initOfflineContext(theInterpreter, key)
execfile(WLSTUtil.getWLSTCommonModulePath())
theInterpreter = None
sys.ps1 = origPrompt
modules = WLSTUtil.getWLSTModules()
for mods in modules:
    execfile(mods.getAbsolutePath())
jmodules = WLSTUtil.getWLSTJarModules()
for jmods in jmodules:
    fis = jmods.openStream()
    execfile(fis, jmods.getFile())
    fis.close()
    # Bug OWLS-39117  If this variable is false - the prompt will look wrong when changing trees
    # wlstPrompt = "false"


def invoke(methodName, parameters, signatures):
    return wlstInvoke(methodName, parameters, signatures)
