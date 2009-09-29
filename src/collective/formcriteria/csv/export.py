import csv
import mimetypes

import ZTUtils

from plone.memoize import view

class ExportView(object):
    """Download collection query results in different formats"""

    formats = {'text/csv': 'writeCSV'}
    fmtparam_prefix = 'csv.fmtparam-'

    def __call__(self):
        content_type = self.request['Content-Type']
        self.request.response.setHeader('Content-Type', content_type)
        self.request.response.setHeader(
            'Content-Disposition',
            'attachment;filename=%s%s' % (
                self.context.getId(),
                mimetypes.guess_extension(content_type)))
        method = getattr(self, self.formats[content_type])
        method(self.context.queryCatalog(REQUEST=self.request))
        return self.request.response

    def _get_fmtparam(self):
        prefix_len = len(self.fmtparam_prefix)
        return dict(
            (key[prefix_len:], value)
            for key, value in self.request.form.iteritems()
            if key.startswith(self.fmtparam_prefix))

    def writeCSV(self, brains):
        """
        Download collection query results in CSV format

        Request query terms starting with self.fmtparam
        (default='csv.fmtparam-') will be converted into kwargs to the
        underlying csv.writer instantiation.
        """
        keys = self.getCustomViewFields()
        vocab = self.context.getField('customViewFields').Vocabulary(
            self.context)

        csvwriter = csv.writer(self.request.response,
                               **self._get_fmtparam())
        csvwriter.writerow(
                tuple(vocab.getValue(key) for key in keys))
        for brain in brains:
            csvwriter.writerow(
                tuple(brain[key] for key in keys))

    @view.memoize
    def getCustomViewFields(self):
        columns = getattr(self.context, 'columns', None)
        if columns is not None:
            return [column.Field() for column in
                    columns.contentValues()]
        return []
            
    def getCSVQuery(self):
        info = self.context.restrictedTraverse(
            '@@sort_info').getSortInfo()
        kw = {'Content-Type': 'text/csv'}
        if info['selected']:
            kw[info['selected']['id']] = True                           
        return ZTUtils.make_query(info['form'], kw)
