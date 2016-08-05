Changelog
=========

2.1 (2016-08-05)
----------------

* Added travis build script
  [bogdangi]

* Fix issues with title and description inside form view and form criteria edit
  [bogdangi]

* Added further Plone 4.3 compatibility [miohtama]

* Use existing i18n message ID in form. [icemac]

2.0 - 2012-11-01
----------------

* Plone 4.2 and 4.3 compatibility.
  [rossp]

* Use localized format for DateTime column values.
  [rossp]

* Add missing form criteria support for the recurse field of path
  criteria.
  [rossp]

* Restrict some of the search form portlet support to the left and
  right column portlet managers on normal plone views, and
  additionally to the 4 dashboard portlet managers on the dashboard
  view for performance reasons.  This means if you want to use the
  search form portlet in a manager for which these registrations don't
  apply, you'll have to use your own registration like the
  <browser:viewlet> registrations in
  collective/formcriteria/form/configure.zcml.
  [rossp]

* Update chameleon compatibility to the new 2.x branch.
  [rossp]

* Optimize and improve performancde.
  [rossp]

* Various upstream template updates.
  [rossp, topherh]

* Add remote URL support to folder_summary_view.
  [topherh]

* Fix an issue with the permission protecting the Export action.
  [rossp]

* Handle catalog index ParseErrors gracefully.  Thanks to Larry
  Pitcher for the report.
  [rossp]

2.0b2 - 2011-01-13
------------------

* Retrofit some Plone 3 compatibility.  Plone 3 is un-supported in
  version 2+.  The tests pass but the UI hasn't been checked so YMMV.
  [rossp]

2.0b1 - 2011-01-11
------------------

* Added a rudimentary UI for managing collection columns.
  [rossp]

2.0a4 - 2011-01-11
------------------

* Restore the workflow menu which was missing from the topic
  folder_contents view.  Thanks to Larry Pitcher for the report.
  [rossp]

2.0a3 - 2011-01-10
------------------

* Change the permission for the grouped listing view so that anonymous
  visitors can access the view when the content is published.
  Thanks to Larry Pitcher for the report.
  [rossp]

* Add support for columns that don't have corresponding catalog
  metadata.  Be aware that using such columns can greatly affect
  performance as export requires looking up every object to retrieve
  the data.
  [rossp]

2.0a2 - 2010-11-23
------------------

* Fixed a problem with a faulty type assumption regarding
  DateTimeFields in the FormDateCriterion.  The FormDateCriterion
  doesn't actually used a DateTimeField.
  [rossp]

* Refactor the <form> and <button> based batch_macros so as to not
  conflict with other uses of the full "navigation" macro within an
  existing form resulting in nested <form>s.
  [rossp]

2.0a1 - 2010-11-21
------------------

* Ensure that the "default" profile is used by portal_quickinstaller
  by... well, default.  :-)
  [rossp]

* Use a <form> and <button> elements in the navigation/paging
  batch_macros to prevent "uri too long" errors when using paging with
  many form criteria.
  [rossp]

* Use method="post" for the criteria form to address "uri too long"
  when lots of form criteria are used.  Reported by mauro and
  confirmed to happen with just two date fields.
  [rossp]

* Added defines for Plone4 complatibility in folder_listing
  skin template.
  [seletz]

* Fix navigation_recurse template to match current Plone 4 version.
  [seletz] [ramonski]

* Add a collection listing portlet that makes use of the
  folder_listing macros for a richer portlet. [rossp]

* fix issue producing
  AttributeError: 'NoneType' object has no attribute 'title_or_id'
  when adding path criterions.
  [hplocher]

* Fix '<input type="hidden" name="sort_on"...', now uses the default
  sort criteria if present

* Use individual persistent objects to represent table columns such as
  with the fodler_contents view.  UI for editing the folder_contents
  column objects has yet to be implemented.

* Fix <tfoot> usage [rossp]

* Integrate sort criteria with folder contents view columns for KSS
  sorting [rossp]

* Add pulldown/select, single-value criterion based on
  FormSelectionCriterion, FormPortalTypeCriterion, and
  FormReferenceCriterion [rossp]

1.1.1 - 2009-08-31
------------------

* "Select all" and "Show all" (KSS) on folder contents view [rossp]

1.1.0 - 2009-08-21
------------------

* Use folder_contents instead of folder_contents_view to fix the links
  back to the folder contents form. [rossp]
* Tighten up the search form portlet spacing. [rossp]
* Use "Table Columns" fields for the folder contents form to control
  the folder contents columns
* Use a "Table Column Links" collection filed to specify which folder
  contents form columns should link to the item [rossp]
* Fix folder contents form buttons, "Copy", "Cut", "Rename", "Change
  State", and "Delete" now all work for objects listed by the
  collections even if they are in different folders.  [rossp]

1.0.2 - 2009-08-12
------------------

* Add some missing portal_types for criteria [rossp]
* Fix a unicode bug with GS portlets.xml import of the search portlet
  [rossp]

1.0.1 - 2009-08-11
------------------

* Merge collective.catalogexport to support CSV export of collection
  based user-submitted queries [rossp]

1.0 - 2009-04-20
----------------

* Ensure that only formFields are taken from the request
* Fix ignored integer range criteria (reported by SimO)
* Use a browser layer (suggested by optilude)
* Add ids and CSS classes to the batch_macro sort links (aaronv)
* Fix a bug with the "operator" field.  Thanks to Mauro!

0.9.5 - 2009-03-06
------------------

* Move package to src directory and fix testing buildout
* Register criteria AT types using the right package name
* Fix a bug with the JavaScript that narrows the criteria types by
  index/field
* Use separate meta_types instead of overwriting the ATCT meta types,
  may be backwards incompatible for previous installations

0.9.4 - 2009-02-08
------------------

* Add a layout that lists items grouped by the sort used
* Fix KeyError: u'unsorted' bug for existing ATTopics as reported by
  jonstahl

0.9.3 - 2009-01-31
------------------

* Fix widget JavaScript and CSS for search form portlet

0.9.2 - 2009-01-31
------------------

* Clarify selected sort
* Make portlet usable outside the context of the collection
* Fix portlet class
* Don't render hour and minute fields on date

0.9.1 - 2009-01-30
------------------

* Move the search form viewlet into a portlet
* Patch the ATCT addCrierion method to properly initialize criteria so
  that they can safely be created in code
* Use the same mismatched meta_type ATCT for the
  FormDateCriterion

0.9 - 2009-01-29
----------------

* Fix incompatibility when extended sort criterion were added to
  existing ATCT ATTopic instances

0.8 - 2009-01-29
----------------

* Added multiple sort links to the batch macro

0.7 - 2009-01-28
----------------

* Change to use the same names as ATCT where appropriate to avoid some
  problems where the ATCT names are expected.
* Flesh out the GenericSetup profile with all other bits in the Plone
  profile that make reference to criteria.

0.6 - 2009-01-26
----------------

* Use a form prefix for the search form.  Fixes calendar JavaScript
  bug.
* Fix criterion label to point to the correct form input
* Allow widget special help/description to appear even if the label
  isn't rendered and use this for the comma widget
* Fix the handling of postbacks in the comma widget
* Use a "Search Form" view that only renders the search form
* Added boolean criteria
* Added date criteria
* Added path criteria
* Added relative path criteria
* Added integer criteria

0.5 - 2009-01-25
----------------

* Form criteria are now designated by selecting which fields of each
  criterion should be rendered on the search form
* Improve label handling.  Remove labels for 'value' field and
  "required" markers for all fields.
* Make the search form collapsible and start collapsed when the form
  has been submitted
* Add a comma separated criterion

0.4 - 2009-01-15
----------------

* Add list criterion
* Add selection criterion
* Fix the form for access by anonymous users

0.3 - 2009-01-15
----------------

* Fully re-use the AT edit widgets
* Support criteria with multiple fields
* Use the widgets to process the form values
* Add checkbox criterion based on FormSelectionCriterion,
  FormPortalTypeCriterion, and FormReferenceCriterion
* Add a date range form criterion (JS calendar not working yet)

0.2 - 2008-05-27
----------------

* Fix i18n_domain in ZCML
* Make the authenticator view conditional for Plone 3.0 compatibility

0.1 - 2008-05-24
----------------

* Initial release

