import csv
import mimetypes

import ZTUtils


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
        columns = self.context.restrictedTraverse(
            'columns_view').ordered

        csvwriter = csv.writer(self.request.response,
                               **self._get_fmtparam())
        csvwriter.writerow(
                tuple(column['name'] for column in columns))
        for brain in brains:
            row = []
            obj = None
            for column in columns:
                field = column['field']
                if field == 'getPath':
                    value = brain.getURL()
                else:
                    try:
                        value = brain[field]
                    except KeyError:
                        # If it's not in the catalog brains, try the
                        # real object
                        if obj is None:
                            obj = brain.getObject()
                        value = getattr(obj, field)
                        if callable(value):
                            value = value()
                row.append(value)
            csvwriter.writerow(row)

    def getCSVQuery(self):
        info = self.context.restrictedTraverse(
            '@@sort_info').getSortInfo()
        kw = {'Content-Type': 'text/csv'}
        if info['selected']:
            kw[info['selected']['id']] = True
        return ZTUtils.make_query(info['form'], kw)
