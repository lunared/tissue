#!/usr/bin/env python3.6
from cgi import escape
import cgi
import cgitb
cgitb.enable()

from tissue.render import render_banner

def get_project(id):
    return []

form = cgi.FieldStorage()
filter_by = form.getlist("filter_by")
project = form.getvalue('project')
issues = [
    {
        "id": 1,
        "title": "Test Issue doesn't even show up properly",
        "state": "Open",
        "lastUpdated": "2018-01-12T10:24:12-04:00",
    },
    {
        "id": 2,
        "title": "OwO what is this?",
        "state": "Open",
        "lastUpdated": "2018-01-12T10:24:12-04:00",
    },
    {
        "id": 5,
        "title": "WoW Gold good shit",
        "state": "Open",
        "lastUpdated": "2018-01-12T10:24:12-04:00",
    },
    {
        "id": 666,
        "title": "Uninstall League",
        "state": "Open",
        "lastUpdated": "2018-01-12T10:24:12-04:00",
    },
]

def render_issue(issue):
    return f"""
        <tr>
            <td><a href="/cgi-bin/issue.py?id={issue['id']}">#{issue['id']} - {issue['title']}</a></td>
            <td>{issue['state']}</a></td>
            <td>{issue['lastUpdated']}</td>
        </tr>
    """


## HEADERS
print("Content-Type: text/html")
print("")

## CONTENT
print(f"""
<head>
    <title>Tissue - Projects</title>
    <link rel="stylesheet" type="text/css" href="/static/style.css">
</head>
<body>
    <header>
        {render_banner()}
    </header>
    <article>
        <table summary="projects" class="projects">
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
    </article>
    <footer>
        <div class="pagination">
            <span>Page 1 of 1</span>
            <form action="/cgi-bin/issues.py" method="GET">
                <input type="hidden" value="{project}" name="project">
                <input type="number" value="1" name="page">
                <button type="submit">Go</button>
            </form>
        </div>
    </footer>
</body>
""")