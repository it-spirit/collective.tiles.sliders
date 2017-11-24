# -*- coding: utf-8 -*-
"""Post install import steps for collective.tiles.sliders."""

from plone import api
from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implementer


@implementer(INonInstallable)
class HiddenProfiles(object):
    """Define hidden GS profiles."""

    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller."""
        return [
            'collective.tiles.sliders:mosaic_support',
            'collective.tiles.sliders:uninstall',
        ]


def post_install(context):
    """Post install script"""
    portal_quickinstaller = api.portal.get_tool('portal_quickinstaller')
    if not portal_quickinstaller.isProductInstalled('plone.app.mosaic'):
        # skip if mosaic isn't installed
        return
    mosaic_profile = 'collective.tiles.sliders:mosaic_support'
    setup_tool = api.portal.get_tool('portal_setup')
    setup_tool.runImportStepFromProfile(mosaic_profile, 'plone.app.registry')


def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.
