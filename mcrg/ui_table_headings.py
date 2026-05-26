from __future__ import annotations


def refresh_table_headings(app, g: dict):
    if not hasattr(app, "tree") or app.tree is None:
        return
    try:
        cols = list(app.tree["columns"])
    except Exception:
        return
    for c in cols:
        try:
            app.tree.heading(c, text=app._col_label(c), command=lambda _c=c: app._sort(_c))
        except Exception:
            pass

