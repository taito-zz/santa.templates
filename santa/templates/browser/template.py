from five import grok
from santa.templates.browser.interfaces import ISantaTemplatesLayer
from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot

grok.templatedir('templates')


class TopView(grok.View):
    grok.context(IPloneSiteRoot)
    grok.layer(ISantaTemplatesLayer)
    grok.name('santa-view')
    grok.template('top-view')
