# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from plone import api
from collective.tiles.sliders.testing import COLLECTIVE_TILES_SLIDERS_INTEGRATION_TESTING  # noqa

import unittest


class TestSetup(unittest.TestCase):
    """Test that collective.tiles.sliders is properly installed."""

    layer = COLLECTIVE_TILES_SLIDERS_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if collective.tiles.sliders is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'collective.tiles.sliders'))

    def test_browserlayer(self):
        """Test that ICollectiveTilesSlidersLayer is registered."""
        from collective.tiles.sliders.interfaces import (
            ICollectiveTilesSlidersLayer)
        from plone.browserlayer import utils
        self.assertIn(
            ICollectiveTilesSlidersLayer,
            utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = COLLECTIVE_TILES_SLIDERS_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['collective.tiles.sliders'])

    def test_product_uninstalled(self):
        """Test if collective.tiles.sliders is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'collective.tiles.sliders'))

    def test_browserlayer_removed(self):
        """Test that ICollectiveTilesSlidersLayer is removed."""
        from collective.tiles.sliders.interfaces import \
            ICollectiveTilesSlidersLayer
        from plone.browserlayer import utils
        self.assertNotIn(
           ICollectiveTilesSlidersLayer,
           utils.registered_layers())
