import csv
import mimetypes

class ExportView(object):

    formats = {'text/csv': 'writeCSV'}

    def __call__(self):
        content_type = self.request['Content-Type']
        self.request.response.setHeader('Content-Type', content_type)
        self.request.response.setHeader(
            'Content-Disposition',
            'attachment;filename=%s.%s' % (
                self.context.getId(),
                mimetypes.guess_extension(content_type)))
        method = getattr(self, self.formats[content_type])
        method(self.context(REQUEST=self.request))
        return self.request.response

    def writeCSV(self, brains):
        keys = self.context._catalog.names
        csvwriter = csv.writer(self.request.response)
        csvwriter.writerow(keys)
        for brain in brains:
            csvwriter.writerow(
                tuple(brain[key] for key in keys))
