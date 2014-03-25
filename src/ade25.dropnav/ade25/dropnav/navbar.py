from five import grok
from plone import api
from Acquisition import aq_inner
from zope.component import getMultiAdapter
from zope.interface import Interface

from Products.CMFCore.utils import getToolByName

from plone.app.layout.viewlets.interfaces import IPortalHeader
from plone.app.layout.navigation.navtree import buildFolderTree
from plone.app.layout.navigation.root import getNavigationRoot
from Products.CMFPlone.browser.navtree import DefaultNavtreeStrategy


class NavbarViewlet(grok.Viewlet):
    grok.name('ade25.dropnav.NavbarViewlet')
    grok.context(Interface)
    grok.require('zope2.View')
    grok.viewletmanager(IPortalHeader)

    def update(self):
        context = aq_inner(self.context)
        self.portal_state = getMultiAdapter((self.context, self.request),
                                            name=u'plone_portal_state')
        self.available = self.testIfThemeEnabled()
        portal_tabs_view = getMultiAdapter((context, self.request),
                                           name='portal_tabs_view')
        self.portal_tabs = portal_tabs_view.topLevelTabs()

        self.selected_tabs = self.selectedTabs(portal_tabs=self.portal_tabs)
        self.selected_portal_tab = self.selected_tabs['portal']

    def selectedTabs(self, default_tab='index_html', portal_tabs=()):
        plone_url = getToolByName(self.context, 'portal_url')()
        plone_url_len = len(plone_url)
        request = self.request
        valid_actions = []
        url = request['URL']
        path = url[plone_url_len:]
        for action in portal_tabs:
            if not action['url'].startswith(plone_url):
                continue
            action_path = action['url'][plone_url_len:]
            if not action_path.startswith('/'):
                action_path = '/' + action_path
            if path.startswith(action_path + '/') or path == action_path:
                valid_actions.append((len(action_path), action['id']))
        valid_actions.sort()
        if valid_actions:
            return {'portal': valid_actions[-1][1]}
        return {'portal': default_tab}

    def navStrategy(self):
        context = aq_inner(self.context)
        root = getNavigationRoot(context)
        query = {
            'path': root,
            'review_state': 'published',
            'portal_type': ('Folder'),
            'sort_order': 'getObjPositionInParent'
        }
        root_obj = context.unrestrictedTraverse(root)
        strategy = DefaultNavtreeStrategy(root_obj)
        strategy.rootPath = '/'.join(root_obj.getPhysicalPath())
        strategy.showAllParents = False
        strategy.bottomLevel = 999
        tree = buildFolderTree(root_obj, root_obj, query, strategy=strategy)
        items = []
        for c in tree['children']:
            item = {}
            item['item'] = c['item']
            item['children'] = c.get('children', '')
            item['itemid'] = c['normalized_id']
            item_id = c['normalized_id']
            if item_id == context.getId():
                item['class'] = 'active'
            else:
                item['class'] = ''
            items.append(item)
        return items

    def get_root_url(self):
        context = aq_inner(self.context)
        site = api.portal.get_navigation_root(context=context)
        return site.absolute_url()

    def isActiveItem(self, itemid):
        context = aq_inner(self.context)
        context_id = context.getId()
        if itemid == context_id:
            return 'navitem active'
        else:
            return 'navitem'

    def testIfThemeEnabled(self):
        theme_header = self.request.get('HTTP_X_THEME_ENABLED', 'No info')
        return theme_header
