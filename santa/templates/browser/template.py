from Products.ATContentTypes.interfaces.document import IATDocument
from Products.ATContentTypes.interfaces.folder import IATFolder
from Products.CMFCore.utils import getToolByName
from five import grok
from santa.content.partner import IPartner
from santa.templates.browser.interfaces import ISantaTemplatesLayer


grok.templatedir('templates')


class FolderView(grok.View):
    grok.context(IATFolder)
    grok.layer(ISantaTemplatesLayer)
    grok.name('santa-view')
    grok.template('folder-view')


class PartnerView(grok.View):
    grok.context(IPartner)
    grok.layer(ISantaTemplatesLayer)
    grok.name('view')
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
