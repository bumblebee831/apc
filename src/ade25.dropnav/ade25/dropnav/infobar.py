from five import grok
from plone import api
from Acquisition import aq_inner
from zope.interface import Interface
from zope.component import getMultiAdapter

from plone.app.layout.viewlets.interfaces import IPortalFooter


class InfobarViewlet(grok.Viewlet):
    grok.name('ade25.dropnav.InfobarViewlet')
    grok.context(Interface)
    grok.require('zope2.View')
    grok.viewletmanager(IPortalFooter)

    def portal_url(self):
        return api.portal.get().absolute_url()

    def language_root_url(self):
        context = aq_inner(self.context)
        root = api.portal.get_navigation_root(context)
        return root.absolute_url()

    def current_lang(self):
        context = aq_inner(self.context)
        pstate = getMultiAdapter((context, self.request),
                                 name=u'plone_portal_state')
        lang = pstate.language()
        return lang
