#!/usr/bin/env python3.6
from cgi import escape
import cgi
import cgitb
cgitb.enable()

from tissue.render import base_template
from tissue.models import get_db

db = get_db()
cur = db.cursor()
cur.execute(
    """
    SELECT 
        id,
        name,
        description,
        homepage,
        (
            SELECT count(*) FROM Issues 
            where project_id = p.id AND (
                UPPER(state) NOT LIKE "CLOSED" OR state is null
            )
        ) as open
    FROM Projects p
    """
)
rows = cur.fetchall()
projects = [
    row for row in rows
]
db.close()

def render_project(project):
    return f"""
        <tr>
            <td><a href="/cgi-bin/issues.py?project={project['id']}">{project['name']}</a></td>
            <td>{escape(project['description'])}</td>
            <td><a href="{project['homepage']}">{project['homepage']}</a></td>
            <td>{project['open']}</td>
        </tr>
    """

base_template(f"""
<table summary="projects" class="projects striped">
    <thead>
        <th>Name</th>
        <th>Description</th>
        <th>Homepage</th>
        <th>Open Issues</th>
    </thead>
    <tbody>
        {
            "".join([render_project(c) for c in projects])
        }
    </tbody>
</table>
""")