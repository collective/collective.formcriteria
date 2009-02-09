from plone.app.content.browser import foldercontents

class FolderContentsView(foldercontents.FolderContentsView):
    """List items in a tabular form including object buttons"""
    
    def contents_table(self):
        """Use the request as the contentFilter"""
        table = foldercontents.FolderContentsTable(
            self.context, self.request, contentFilter=self.request)
        return table.render()
