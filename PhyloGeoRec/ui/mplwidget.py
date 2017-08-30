# -*- coding: utf-8 -*-
"""
/***************************************************************************
 mplWidget 
                                 Matplotlib Custom Widget for Qt
 Designed for Phylogeography Reconstruction Tool for QGIS
                              -------------------
        begin                : 2016-06-07
        git sha              : $Format:%H$
        copyright            : (C) 2016 by Maulana Malik Nashrulloh/NK Research Lab
        email                : mmnashrullah@gmail.com
 ***************************************************************************/

 /***************************************************************************
 *                                                                         *
 *   Based from tutorial on: 											   *
 *   Tosi, S. 2009. Matplotlib for Python Developers. 					   *
 *	 (Chapter 6: Embedding Matplotlib in Qt4)					           *
 *                                                                         *
 *	 For Phylogenetic Works, see:										   *
 *	 Antao, T. 2015. Bioinformatics with Python Cookbook. 				   *
 *	 (Chapter 6: Phylogenetics)				   							   *
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

# Python Qt4 bindings for GUI objects
from PyQt4 import QtGui

# import the Qt4Agg FigureCanvas object, that binds Figure to
# Qt4Agg backend. It also inherits from QWidget
from matplotlib.backends.backend_qt4agg \
import FigureCanvasQTAgg as FigureCanvas

# Matplotlib Figure object
from matplotlib.figure import Figure

class mplCanvas(FigureCanvas):
	"""Class to represent the FigureCanvas widget"""
	def __init__(self):
		# setup Matplotlib Figure and Axis
		self.fig = Figure()
		self.ax = self.fig.add_subplot(111)
		# initialization of the canvas
		FigureCanvas.__init__(self, self.fig)
		# we define the widget as expandable
		FigureCanvas.setSizePolicy(self, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
		# notify the system of updated policy
		FigureCanvas.updateGeometry(self)

class mplWidget(QtGui.QWidget):
	"""Widget defined in Qt Designer"""
	def __init__(self, parent = None):
		# initialization of Qt MainWindow widget
		QtGui.QWidget.__init__(self, parent)
		# set the canvas to the Matplotlib widget
		self.canvas = mplCanvas()
		# create a custom widget layout (VBoxLayout)
		self.customWidget = QtGui.QVBoxLayout()
		# add mpl widget to vertical box
		self.customWidget.addWidget(self.canvas)
		# set the layout to the vertical box
		self.setLayout(self.customWidget)
		