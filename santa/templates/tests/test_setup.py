from santa.templates.tests.base import IntegrationTestCase
from Products.CMFCore.utils import getToolByName


class TestCase(IntegrationTestCase):
    """TestCase for Plone setup."""

    def setUp(self):
        self.portal = self.layer['portal']

    def test_is_santa_templates_installed(self):
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        self.failUnless(installer.isProductInstalled('santa.templates'))

    def test_browserlayer(self):
        from santa.templates.browser.interfaces import ISantaTemplatesLayer
        from plone.browserlayer import utils
        self.failUnless(ISantaTemplatesLayer in utils.registered_layers())

    def test_uninstall__package(self):
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        installer.uninstallProducts(['santa.templates'])
        self.failIf(installer.isProductInstalled('santa.templates'))

    def test_uninstall__browserlayer(self):
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        installer.uninstallProducts(['santa.templates'])
        from santa.templates.browser.interfaces import ISantaTemplatesLayer
        from plone.browserlayer import utils
        self.failIf(ISantaTemplatesLayer in utils.registered_layers())
