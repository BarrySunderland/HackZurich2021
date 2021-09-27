# coding=utf-8
"""Resources test.

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

"""

__author__ = 'anythingmapping@gmail.com'
__date__ = '2021-09-25'
__copyright__ = 'Copyright 2021, Siemens'

import unittest

from qgis.PyQt.QtGui import QIcon



class Predictive_maintenanceDialogTest(unittest.TestCase):
    """Test rerources work."""

    def setUp(self):
        """Runs before each test."""
        pass

    def tearDown(self):
        """Runs after each test."""
        pass

    def test_icon_png(self):
        """Test we can click OK."""
        path = ':/plugins/Predictive_maintenance/icon.png'
        icon = QIcon(path)
        self.assertFalse(icon.isNull())

if __name__ == "__main__":
    suite = unittest.makeSuite(Predictive_maintenanceResourcesTest)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)



