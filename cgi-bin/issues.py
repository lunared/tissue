#!/usr/bin/env python3.6
from cgi import escape
import cgi
import cgitb
cgitb.enable()

from tissue.render import base_template
from tissue.models import get_db

def get_project(id):
    return []

form = cgi.FieldStorage()
filter_by = form.getlist("filter_by")
project = form.getvalue('project')

db = get_db()
cur = db.cursor()
cur.execute(
    """
    SELECT * FROM Issues
    WHERE project_id = ?
    ORDER BY datetime(last_updated) DESC
    """,
    (project,)
)
issues = cur.fetchall()[:]
db.close()

def render_issue(issue):
    return f"""
        <tr>
            <td><a href="/cgi-bin/issue.py?id={issue['id']}">#{issue['id']} - {issue['title']}</a></td>
            <td>{issue['state']}</td>
            <td>{issue['last_updated']}</td>
        </tr>
    """


base_template(f"""
<a href="/cgi-bin/create_issue.py?project={project}">Create Issue</a>
<table summary="projects" class="projects striped">
    <thead>
        <th>Issue</th>
        <th>Status</th>
        <th>Last Activity</th>
    </thead>
    <tbody>
        {
            "".join([render_issue(c) for c in issues])
        }
    </tbody>
</table>
<div class="pagination">
    <span>Page 1 of 1</span>
    <form action="/cgi-bin/issues.py" method="GET">
        <input type="hidden" value="{project}" name="project">
        <input type="number" value="1" name="page">
        <button type="submit">Go</button>
    </form>
</div>
""")
