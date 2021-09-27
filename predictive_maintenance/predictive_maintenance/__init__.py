# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Predictive_maintenance
                                 A QGIS plugin
 An interface to the analytics engine predicting failure points.
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2021-09-25
        copyright            : (C) 2021 by Siemens
        email                : anythingmapping@gmail.com
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
    """Load Predictive_maintenance class from file Predictive_maintenance.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .Predictive_maintenance import Predictive_maintenance
    return Predictive_maintenance(iface)
