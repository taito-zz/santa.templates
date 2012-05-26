from Acquisition import aq_parent
from DateTime import DateTime
from OFS.interfaces import IItem
from Products.ATContentTypes.interfaces.document import IATDocument
from Products.ATContentTypes.interfaces.event import IATEvent
from Products.ATContentTypes.interfaces.folder import IATFolder
from Products.ATContentTypes.interfaces.image import IATImage
from Products.ATContentTypes.interfaces.news import IATNewsItem
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot
from Products.PloneFormGen.interfaces import IPloneFormGenForm
from five import grok
from plone.app.contentlisting.interfaces import IContentListing
from plone.app.layout.viewlets.interfaces import IPortalHeader
from plone.app.viewletmanager.manager import OrderedViewletManager
from plone.namedfile.file import NamedImage
from santa.content.partner import IPartner
from santa.templates import _
from santa.templates.browser.interfaces import ISantaTemplatesLayer
from zope.component import getMultiAdapter


grok.templatedir('templates')


class TopView(grok.View):
    grok.context(IPloneSiteRoot)
    grok.layer(ISantaTemplatesLayer)
    grok.name('santa-view')
    grok.template('top-view')


class FolderView(grok.View):
    grok.context(IATFolder)
    grok.layer(ISantaTemplatesLayer)
    grok.name('santa-view')
    grok.template('folder-view')


class PartnerView(grok.View):
    grok.context(IPartner)
    grok.layer(ISantaTemplatesLayer)
    grok.name('santa-view')
    grok.template('partner-view')

    def _document(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        languages = getToolByName(self.context, 'portal_languages')
        oids = languages.supported_langs
        query = {
            'path': {
                'query': '/'.join(self.context.getPhysicalPath()),
                'depth': 1,
            },
            'object_provides': IATDocument.__identifier__,
        }
        brains = catalog(query)
        if brains:
            brain = brains[0]
            bid = brain.id
            if bid in oids:
                return brain

    def title(self):
        doc = self._document()
        return doc and doc.Title or self.context.Title()

    def description(self):
        doc = self._document()
        return doc and doc.Description or self.context.Description()

    def text(self):
        doc = self._document()
        if doc:
            obj = doc.getObject()
            return obj.CookedBody()

    def image(self):
        if self.context.image:
            scales = self.context.restrictedTraverse('@@images')
            return scales.tag('image', scale='mini')
