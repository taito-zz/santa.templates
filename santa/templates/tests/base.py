from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import unittest2 as unittest


class SantaTemplatesLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        """Set up Zope."""
        # Load ZCML
        import Products.PloneFormGen
        self.loadZCML(package=Products.PloneFormGen)
        z2.installProduct(app, 'Products.PloneFormGen')
        import santa.templates
        self.loadZCML(package=santa.templates)
        z2.installProduct(app, 'santa.templates')

    def setUpPloneSite(self, portal):
        """Set up Plone."""
        # Install into Plone site using portal_setup
        self.applyProfile(portal, 'Products.PloneFormGen:default')
        self.applyProfile(portal, 'santa.templates:default')

    def tearDownZope(self, app):
        """Tear down Zope."""
        z2.uninstallProduct(app, 'santa.templates')
        z2.uninstallProduct(app, 'Products.PloneFormGen')


FIXTURE = SantaTemplatesLayer()
INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,), name="SantaTemplatesLayer:Integration")
FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE,), name="SantaTemplatesLayer:Functional")


class IntegrationTestCase(unittest.TestCase):
    """Base class for integration tests."""

    layer = INTEGRATION_TESTING


class FunctionalTestCase(unittest.TestCase):
    """Base class for functional tests."""

    layer = FUNCTIONAL_TESTING
