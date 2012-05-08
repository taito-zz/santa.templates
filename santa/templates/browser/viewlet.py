from OFS.interfaces import IItem
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from five import grok
from plone.app.layout.viewlets.interfaces import IPortalHeader
from plone.app.viewletmanager.manager import OrderedViewletManager
from plone.registry.interfaces import IRegistry
from plone.z3cform.layout import FormWrapper
from santa.templates.browser.interfaces import ISantaTemplatesLayer
from zope.component import getMultiAdapter
from zope.component import getUtility
from plone.app.contentlisting.interfaces import IContentListing



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
        portal = portal_state.portal()
        items = {
            'title': portal.title,
            'description': portal.description,
            'portal_url': portal.absolute_url(),
        }
        head = portal.get('foundation')
        if head:
            query = {
                'path': {
                    'query': '/'.join(head.getPhysicalPath()),
                    'depth': 1
                }
            }
            brains = catalog(query)
            if len(brains) > 0:
                brain = brains[0]
                title = brain.Title
                description = brain.Description
                if title:
                    items.update({'title': title})
                if description:
                    items.update({'description': description})
        return items


class SantaTopViewletManager(OrderedViewletManager, grok.ViewletManager):
    """Viewlet manager to Santa Top."""
    grok.context(IPloneSiteRoot)
    grok.layer(ISantaTemplatesLayer)
    grok.name('santa.top.manager')


class BaseViewlet(grok.Viewlet):
    """Base Viewlet Class."""
    grok.baseclass()
    grok.context(IPloneSiteRoot)
    grok.layer(ISantaTemplatesLayer)
    grok.require('zope2.View')
    grok.viewletmanager(SantaTopViewletManager)


class AboutViewlet(BaseViewlet):
    grok.name('santa.viewlet.about')
    grok.template('about')

    def item(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        portal_state = getMultiAdapter((self.context, self.request), name="plone_portal_state")
        portal = portal_state.portal()
        item = portal.get('foundation')
        if item:
            query = {
                'path': {
                    'query': '/'.join(item.getPhysicalPath()),
                    'depth': 1,
                }
            }
            brains = catalog(query)
            if brains:
                brain = brains[0]
                obj = brain.getObject()
                return {
                    'description': brain.Description,
                    'text': obj.getField('text').get(obj),
                    'title': brain.Title,
                    'url': brain.absolute_url(),
                }

    def inquiries(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        portal_state = getMultiAdapter((self.context, self.request), name="plone_portal_state")
        portal = portal_state.portal()
        item = portal.get('inquiries')
        if item:
            query = {
                'path': {
                    'query': '/'.join(item.getPhysicalPath()),
                    'depth': 1,
                }
            }
            return IContentListing(catalog(query))
