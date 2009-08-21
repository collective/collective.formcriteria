from zope.app import pagetemplate

from plone.app.content.browser import tableview
from plone.app.content.browser import foldercontents

class Table(tableview.Table):
    """Use a table template which obeys the columns fields"""                

    render = pagetemplate.ViewPageTemplateFile("table.pt")

    def __init__(self, request, base_url, view_url, items, columns,
                 show_sort_column=False, buttons=[], pagesize=20):
        super(Table, self).__init__(
            request=request, base_url=base_url, view_url=view_url,
            items=items, show_sort_column=show_sort_column,
            buttons=buttons, pagesize=pagesize)
        self.columns = columns

class FolderContentsTable(foldercontents.FolderContentsTable):
    """Use a table template which obeys the columns fields"""                

    # Copied from
    # plone.app.content.browser.foldercontents.FolderContentsTable
    # v1.2.5
    def __init__(self, context, request, contentFilter={}):
        """Use a table template which obeys the columns fields"""
        self.context = context
        self.request = request
        self.contentFilter = contentFilter

        column_vocab = context.Vocabulary('customViewFields')[0]
        link_columns = context.getField(
            'customViewLinks').getAccessor(context)()
        columns = [
            dict(id=column, name=column_vocab.getValue(column),
                 link=(column in link_columns))
            for column in context.getCustomViewFields()]

        url = context.absolute_url()
        view_url = url + '/@@folder_contents'
        self.table = Table(
            request, url, view_url, self.items, columns,
            show_sort_column=self.show_sort_column,
            buttons=self.buttons)

class FolderContentsView(foldercontents.FolderContentsView):
    """List items in a tabular form including object buttons"""
    
    def contents_table(self):
        """Use the request as the contentFilter"""
        table = FolderContentsTable(
            self.context, self.request, contentFilter=self.request)
        return table.render()
