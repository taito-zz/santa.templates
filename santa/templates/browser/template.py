from Products.Five.browser import BrowserView
#from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class DemoView(BrowserView):

#    index = ViewPageTemplateFile('templates/demo.pt')

    def __call__(self):
        pass
#        return self.index()
