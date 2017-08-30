# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Default Settings of PhyloGeoRec
                             -------------------
        begin                : 2016-02-08
        git sha              : $Format:%H$
        copyright            : (C) 2016 by Maulana Malik Nashrulloh/NK Research Lab
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

plugin_version = "1.00.b7.5"
debug_mode = 0


class DefaultSettings:

    def __init__(self):
        # template
        self.template = "3DViewer(dat-gui).html"

        # world
        self.baseSize = 100
        self.zExaggeration = 10
        self.zShift = 0

        # controls
        self.controls = "OrbitControls.js"    # last selected one has priority

    def __getattr__(self, name):
        raise AttributeError

def_vals = DefaultSettings()
