from Acquisition import aq_inner
from five import grok
from santa.templates.browser.interfaces import ISantaTemplatesLayer
from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot
from Products.ATContentTypes.interfaces.folder import IATFolder
from Products.ATContentTypes.interfaces.document import IATDocument
from Products.CMFCore.utils import getToolByName
from Products.PloneFormGen.interfaces import IPloneFormGenForm
from plone.app.contentlisting.interfaces import IContentListing


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
