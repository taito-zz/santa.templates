from OFS.interfaces import IItem
from Products.CMFCore.utils import getToolByName
from five import grok
from plone.app.layout.viewlets.interfaces import IPortalHeader
from santa.templates.browser.interfaces import ISantaTemplatesLayer
from zope.component import getMultiAdapter


grok.templatedir('viewlets')


class HeadTitleViewlet(grok.Viewlet):
    grok.context(IItem)
    grok.layer(ISantaTemplatesLayer)
    grok.name('santa.head.title')
    grok.require('zope2.View')
    grok.template('head-title')
    grok.viewletmanager(IPortalHeader)

    def head(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        portal_state = getMultiAdapter((self.context, self.request), name="plone_portal_state")
        head = portal_state.portal().get('head')
        if head:
            query = {
                'path': {
                    'query': '/'.join(head.getPhysicalPath()),
                    'depth': 1
                }
            }
            return catalog(query)[0]
