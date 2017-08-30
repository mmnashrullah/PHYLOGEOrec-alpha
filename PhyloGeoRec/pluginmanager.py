# -*- coding: utf-8 -*-
"""
/***************************************************************************
 pluginmanager.py
        begin                : 2016-06-17
        copyright            : (C) 2016 Maulana Malik Nashrulloh
        email                : mnashrullah@gmail.com
		
 Modified from the original module of pluginmanager.py of Qgis2threejs plugin
        copyright            : (C) 2015 by Minoru Akagi
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
import os
import sys

from PyQt4.QtCore import QDir, QFile, QSettings
from phylogeorectools import logMessage


class PluginManager:

    def __init__(self, allPlugins=False):
        self.allPlugins = allPlugins
        self.reloadPlugins()

    def reloadPlugins(self):
        self.modules = []
        self.plugins = []

        if self.allPlugins:
            plugin_dir = QDir(os.path.join(os.path.dirname(QFile.decodeName(__file__)), "plugins"))
            plugins = plugin_dir.entryList(QDir.Dirs | QDir.NoSymLinks | QDir.NoDotAndDotDot)
        else:
            p = QSettings().value("/PhyloGeoRec/plugins", "", type=unicode)
            plugins = p.split(",") if p else []

        import importlib
        for name in plugins:
            try:
                modname = "PhyloGeoRec.plugins." + str(name)
                module = reload(sys.modules[modname]) if modname in sys.modules else importlib.import_module(modname)
                self.modules.append(module)
                self.plugins.append(getattr(module, "plugin_class"))
            except ImportError:
                logMessage("Failed to load plugin: " + str(name))

    def demProviderPlugins(self):
        plugins = []
        for plugin in self.plugins:
            if plugin.type() == "demprovider":
                plugins.append(plugin)
        return plugins

    def findDEMProvider(self, id):
        for plugin in self.plugins:
            if plugin.type() == "demprovider" and plugin.providerId() == id:
                return plugin.providerClass()
        return None
