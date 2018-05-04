# -*- coding: utf-8 -*-
"""
/***************************************************************************
 GeoTools
                                 A QGIS plugin
 Tools for Geoscience & Exploration
                              -------------------
        begin                : 2018-04-13
        git sha              : $Format:%H$
        copyright            : (C) 2018 by Roland Hill / MMG
        email                : roland.hill@mmg.com
 ***************************************************************************/
"""
from PyQt5.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QMenu, QDialog

from qgis.core import *
from qgis.utils import *
from qgis.gui import *

# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the dialog
from .geotools_dialog import GeoToolsDialog
#from .drillsetup_dialog import Ui_drillSetup_dialog
from .drillsetup_dialog import DrillSetupDialog

import os.path

class DrillManager:
    def __init__(self):
        pass
    
    def onDrillSetup(self):
#        dlg = QDialog()
        dlg = DrillSetupDialog()
#        ui.setupUi(dlg)
        dlg.show()
        result = dlg.exec_()

    def onDrillDisplayTraces(self):
        pass

    def onDrillCreateSection(self):
        pass

    
class GeoTools:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'GeoTools_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        self.drillManager = DrillManager()

        # Declare instance attributes
        self.actions = []
        #self.menu = self.tr(u'&GeoTools')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'GeoTools')
        self.toolbar.setObjectName(u'GeoTools')

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('GeoTools', message)


    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        actions = self.iface.mainWindow().menuBar().actions()
        """ Create main menu."""
        lastAction = actions[-1]
        self.menu = QMenu( u'&GeoTools', self.iface.mainWindow().menuBar() )
        self.iface.mainWindow().menuBar().insertMenu( lastAction, self.menu )
        
        """Create Drill menu."""
        self.menuDrill = self.menu.addMenu("Drilling")

        action = self.menuDrill.addAction("Drill Setup")
        action.triggered.connect(self.drillManager.onDrillSetup)
        action.setEnabled(True)
        self.actions.append(action)

        action = self.menuDrill.addAction("Display Traces")
        action.triggered.connect(self.drillManager.onDrillDisplayTraces)
        action.setEnabled(True)
        self.actions.append(action)
        
        action = self.menuDrill.addAction("Create Section")
        action.triggered.connect(self.drillManager.onDrillCreateSection)
        action.setEnabled(True)
        self.actions.append(action)
        
        """Create Raster menu."""
        self.menuDrill = self.menu.addMenu("Raster")

        action = self.menuDrill.addAction("Transparent White")
        action.triggered.connect(self.onRasterTransparentWhite)
        action.setEnabled(True)
        self.actions.append(action)
        
        action = self.menuDrill.addAction("Transparent Black")
        action.triggered.connect(self.onRasterTransparentBlack)
        action.setEnabled(True)
        self.actions.append(action)
        
        

#        icon_path = ':/plugins/geotools/icon.png'
#        self.add_action(
#            icon_path,
#            text=self.tr(u'GeoTools'),
#            callback=self.run,
#            parent=self.iface.mainWindow())

    def onRasterTransparentWhite(self):
        self.rasterTransparent(255, 255, 255)

    def onRasterTransparentBlack(self):
        self.rasterTransparent(0, 0, 0)

    def rasterTransparent(self, r, g, b):
        tr_list = []
        ltr = QgsRasterTransparency.TransparentThreeValuePixel()
        ltr.red = r
        ltr.green = g
        ltr.blue = b
        ltr.percentTransparent = 100
        tr_list.append(ltr)
        
        if Qgis.QGIS_VERSION_INT < 30000 :
            sl = self.iface.legendInterface().selectedLayers(True)
        else:
            sl = self.iface.layerTreeView().selectedLayers()
        for layer in sl:
        	raster_transparency  = layer.renderer().rasterTransparency()
        	raster_transparency.setTransparentThreeValuePixelList(tr_list)
        	layer.triggerRepaint()

    def unload(self):
        self.iface.mainWindow().menuBar().removeAction(self.menu.menuAction())
        del self.menu
        # remove the toolbar
        del self.toolbar


    def run(self):
        pass
#        """Run method that performs all the real work"""
        # show the dialog
#        self.dlg.show()
        # Run the dialog event loop
 #       result = self.dlg.exec_()
        # See if OK was pressed
 #       if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
 #           pass
