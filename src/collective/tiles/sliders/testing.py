# -*- coding: utf-8 -*-
"""Test Layer for collective.tiles.githubgist."""

from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import Layer
from plone.testing import z2


class Fixture(PloneSandboxLayer):
    """Custom Test Layer for collective.tiles.githubgist."""

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        """Set up Zope for testing."""
        # Load ZCML
        import plone.app.mosaic
        self.loadZCML(package=plone.app.mosaic)
        import collective.tiles.sliders
        self.loadZCML(package=collective.tiles.sliders)

    def setUpPloneSite(self, portal):
        self.applyProfile(portal, 'plone.app.mosaic:default')
        self.applyProfile(portal, 'collective.tiles.sliders:default')


FIXTURE = Fixture()

INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE, ),
    name='collective.tiles.sliders:Integration',
)

FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE, z2.ZSERVER_FIXTURE),
    name='collective.tiles.sliders:Functional',
)


ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(FIXTURE, REMOTE_LIBRARY_BUNDLE_FIXTURE, z2.ZSERVER_FIXTURE),
    name='collective.tiles.sliders:Acceptance',
)

ROBOT_TESTING = Layer(name='collective.tiles.sliders:Robot')
