import Acquisition
from OFS import CopySupport

from Products.CMFPlone.utils import transaction_note
from Products.CMFPlone import PloneMessageFactory as _


class TopicPathsButton(object):

    method = None
    transaction_note = None
    message = None

    def __call__(self):
        oblist = []
        op = 0
        context = Acquisition.aq_inner(self.context)
        paths = self.request['paths']
        for path in paths:
            obj = context.restrictedTraverse(path)
            container = Acquisition.aq_parent(
                Acquisition.aq_inner(obj))
            cp = getattr(container, self.method)([obj.getId()])
            op, mdatas = CopySupport._cb_decode(cp)
            oblist.extend(mdatas)
        cp = CopySupport._cb_encode((op, oblist))
        resp = self.request.response
        resp.setCookie('__cp', cp, path='%s' %
                       CopySupport.cookie_path(self.request))
        self.request['__cp'] = cp

        transaction_note(self.transaction_note % paths)
        message = _(self.message, mapping={u'count': len(paths)})
        context.plone_utils.addPortalMessage(message)

        resp.redirect(context.absolute_url())
        return ''


class TopicCopy(TopicPathsButton):

    method = 'manage_copyObjects'
    transaction_note = 'Copied %r'
    message = u'${count} item(s) copied.'


class TopicCut(TopicPathsButton):

    method = 'manage_cutObjects'
    transaction_note = 'Cut %r'
    message = u'${count} item(s) cut.'
