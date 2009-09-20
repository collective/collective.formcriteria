Two different cases: up and down

- up

In this case we want to query for children and show the parents of the
matching children up to a certain point.

If a path query term is present, get the set of doc ids for that one
query term.  For each item in the full query results, get the parent
doc id and if it's in the parents set, then include the parent.  If
not, stop ascending

Sorting is an issue here.  First sort on path, then group recursively
on path.  Sorting on the might not make any sense here when combined
with grouping by hierarchy because a result item that should sort to
the end may be listing before items that should sort to the beginning
just because the item lives in the same container as another item with
an early sort position.  As such, any requirement for something like
this is probably really a requirement for a flat, non-hierarchical
table of the queried items.

- down

In this case we want to indiscriminately show children irregardless of
the query.  The query will find the parents.

A special metadata column will list the ids of the children (in order
if applicable).  This column will be used to recurse.  Mus make sure
this metadata column is updated when the container is modified.

Sorting is not an issue here.
