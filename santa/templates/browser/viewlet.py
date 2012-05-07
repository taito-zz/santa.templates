from Acquisition import aq_inner
from OFS.interfaces import IItem
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces import IPloneSiteRoot
from five import grok
from plone.app.layout.viewlets.interfaces import IPortalHeader
from plone.app.viewletmanager.manager import OrderedViewletManager
from plone.registry.interfaces import IRegistry
from santa.templates import _
from santa.templates.browser.interfaces import ISantaTemplatesLayer
from zope.component import getMultiAdapter
from zope.component import getUtility


grok.templatedir('viewlets')


class HeadTitleViewlet(grok.Viewlet):
    grok.context(IItem)
    grok.layer(ISantaTemplatesLayer)
    grok.name('santa.head.title')
    grok.require('zope2.View')
    grok.template('head-title')
    grok.viewletmanager(IPortalHeader)

    def update(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        