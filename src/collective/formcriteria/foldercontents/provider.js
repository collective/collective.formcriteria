var _FolderContentsColumnOrCurrentFormVarPP = function() {

this.check = function(args) {
;;; if (args.length != 1) {
;;;     throw new Error('folderContentsColumnOrCurrentFormVar method needs 0 or 1 arguments [varname]');
;;; }
};

this.eval = function(args, node) {
    var value = kukit.dom.getAttribute(node, "id").slice(15, -7);
    if (value) {
        return value;
    }
    if (args.length == 1) {
        return kukit.fo.getFormVar(new kukit.fo.CurrentFormLocator(node),
            args[0]);
    } else {
        // no form var name, just get the value of the node.
        return kukit.fo.getValueOfFormElement(node);
    }
};

};

kukit.pprovidersGlobalRegistry.register(
    'folderContentsColumnOrCurrentFormVar',
    _FolderContentsColumnOrCurrentFormVarPP);
