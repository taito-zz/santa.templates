from santa.templates.tests.base import IntegrationTestCase
from Products.CMFCore.utils import getToolByName


class TestCase(IntegrationTestCase):
    """TestCase for Plone setup."""

    def setUp(self):
        self.portal = self.layer['portal']

    def test_is_santa_templates_installed(self):
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        self.failUnless(installer.isProductInstalled('santa.templates'))

    def test_is_santa_content_installed(self):
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        self.failUnless(installer.isProductInstalled('santa.content'))

    def test_is_collective_contentleadimage_installed(self):
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        self.failUnless(installer.isProductInstalled('collective.contentleadimage'))

    def test_browserlayer(self):
        from santa.templates.browser.interfaces import ISantaTemplatesLayer
        from plone.browserlayer import utils
        self.failUnless(ISantaTemplatesLayer in utils.registered_layers())

    def test_metadata__version(self):
        setup = getToolByName(self.portal, 'portal_setup')
        self.assertEqual(
            setup.getVersionForProfile('profile-santa.templates:default'),
            u'1'
        )

    def test_types__Plone_Site__immediate_view(self):
        portal_types = getToolByName(self.portal, 'portal_types')
        type_info = portal_types.getTypeInfo('Plone Site')
        self.assertEqual(type_info.getProperty('immediate_view'), 'santa-view')

    def test_types__Plone_Site__default_view(self):
        portal_types = getToolByName(self.portal, 'portal_types')
        type_info = portal_types.getTypeInfo('Plone Site')
        self.assertEqual(type_info.getProperty('default_view'), 'santa-view')

    def test_types__Plone_Site__view_methods(self):
        portal_types = getToolByName(self.portal, 'portal_types')
        type_info = portal_types.getTypeInfo('Plone Site')
        self.assertEqual(type_info.getProperty('view_methods'), ('santa-view',))

    def test_portal__layout(self):
        self.assertEqual(self.portal.getLayout(), 'santa-view')

    def test__cli_properties(self):
        portal_properties = getToolByName(self.portal, 'portal_properties')
        cli_properties = getattr(portal_properties, 'cli_properties')
        self.assertEqual(
            cli_properties.getProperty('allowed_types'),
            ('Event',)
        )

    def test_viewlets__santa_top_manager(self):
        from zope.component import getUtility
        from plone.app.viewletmanager.interfaces import IViewletSettingsStorage
        storage = getUtility(IViewletSettingsStorage)
        self.assertEqual(
            storage.getOrder('santa.top.manager', '*'),
            (
                u'santa.viewlet.about',
                u'santa.viewlet.news',
                u'santa.viewlet.events',
                u'santa.viewlet.partners',
                u'santa.viewlet.cases',
            )
        )

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
