# -*- coding: utf-8 -*-
"""
/***************************************************************************
 PhyloGeoRec
                                 A QGIS plugin
 Phylogeography Reconstruction Tool for QGIS
                              -------------------
        begin                : 2016-04-13
        git sha              : $Format:%H$
        copyright            : (C) 2016 by Maulana Malik Nashrullah/NK Research Lab
        email                : mmnashrullah@gmail.com
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
from PyQt4.QtCore import *
from PyQt4.QtGui import *

# Initialize Qt resources from file resources_rc.py
import ui.resources_rc

# Import the code for the dialog
from ui.ui_phylogeorecdialog import Ui_PhyloGeoRecDialogBase

import os

# Import additional library
from qgis.gui import *
from qgis.core import *

from phylogeorectools import logMessage, removeTemporaryOutputDir


class PhyloGeoRec:

    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface

        # initialize plugin directory
        self.plugin_dir = os.path.dirname(QFile.decodeName(__file__))

        # initialize locale
        #locale = QSettings().value("locale/userLocale")[0:2]
        #localePath = os.path.join(self.plugin_dir, 'i18n', 'PhyloGeoRec_{0}.qm'.format(locale))

        #if os.path.exists(localePath):
        #  self.translator = QTranslator()
        #  self.translator.load(localePath)

        #  if qVersion() > '4.3.3':
        #    QCoreApplication.installTranslator(self.translator)

        self.objectTypeManager = None
        self.pluginManager = None

        self.exportSettings = {}
        self.lastTreeItemData = None
        self.settingsFilePath = None

    def initGui(self):
        # Create action that will start plugin configuration
        icon = QIcon(os.path.join(self.plugin_dir, "icon.png"))
        self.action = QAction(icon, u"PhyloGeoRec", self.iface.mainWindow())
        self.action.setObjectName("PhyloGeoRec")

        self.settingAction = QAction(u"Settings", self.iface.mainWindow())
        self.settingAction.setObjectName("PhyloGeoRecSettings")

        # connect the action to the run method
        self.action.triggered.connect(self.run)
        self.settingAction.triggered.connect(self.setting)

        # Add toolbar button and menu items
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu(u"PhyloGeoRec", self.action)
        self.iface.addPluginToMenu(u"PhyloGeoRec", self.settingAction)

    def unload(self):
        # Remove the menu items and icon
        self.iface.removeToolBarIcon(self.action)
        self.iface.removePluginMenu(u"PhyloGeoRec", self.action)
        self.iface.removePluginMenu(u"PhyloGeoRec", self.settingAction)

        # remove temporary output directory
        removeTemporaryOutputDir()

    def run(self):
        from vectorobject import ObjectTypeManager
        from pluginmanager import PluginManager
        from phylogeorecdialog import PhyloGeoRecDialog

        if self.objectTypeManager is None:
            self.objectTypeManager = ObjectTypeManager()

        if self.pluginManager is None:
            self.pluginManager = PluginManager()

        # restore export settings
        proj_path = QgsProject.instance().fileName()
        settingsFilePath = proj_path + ".qto3settings" if proj_path else None

        if not self.exportSettings or settingsFilePath != self.settingsFilePath:
            if settingsFilePath and os.path.exists(settingsFilePath):
                self.loadExportSettings(settingsFilePath)
                logMessage(u"Restored export settings of this project: {0}".format(os.path.basename(proj_path)))    #QgsProject.instance().title()

        dialog = PhyloGeoRecDialog(self.iface, self.objectTypeManager, self.pluginManager, self.exportSettings, self.lastTreeItemData)

        # show dialog
        dialog.show()
        ret = dialog.exec_()

        self.exportSettings = dialog.settings(True)

        item = dialog.ui.treeWidget.currentItem()
        self.lastTreeItemData = item.data(0, Qt.UserRole) if item else None

        # if export succeeded, save export settings in the directory that project file exists
        if ret and settingsFilePath:
            self.saveExportSettings(settingsFilePath)

        self.settingsFilePath = settingsFilePath

    def setting(self):
        from settingsdialog import SettingsDialog
        dialog = SettingsDialog(self.iface.mainWindow())
        dialog.show()
        if dialog.exec_():
            from pluginmanager import PluginManager
            self.pluginManager = PluginManager()

    def loadExportSettings(self, filename):
        import json
        with open(filename) as f:
            self.exportSettings = json.load(f)

    def saveExportSettings(self, filename):
        import codecs
        import json
        try:
            with codecs.open(filename, "w", "UTF-8") as f:
                json.dump(self.exportSettings, f, ensure_ascii=False, indent=2, sort_keys=True)
            return True
        except Exception as e:
            logMessage("Failed to save export settings: " + str(e))
            return False
