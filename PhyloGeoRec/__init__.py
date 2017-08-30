# -*- coding: utf-8 -*-
"""
/***************************************************************************
 PhyloGeoRec
                                 A QGIS plugin
 Phylogeography Reconstruction Tool for QGIS
                             -------------------
        begin                : 2016-04-13
        copyright            : (C) 2016 by Maulana Malik Nashrullah/NK Research Lab
        email                : mmnashrullah@gmail.com
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load PhyloGeoRec class from file PhyloGeoRec.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from phylogeorec import PhyloGeoRec
    return PhyloGeoRec(iface)
