#!/usr/bin/env python3.6
from cgi import escape
import cgi
import cgitb
cgitb.enable()

from tissue.render import render_banner

projects = [
    {
        "id": 1,
        "name": "Tissue",
        "description": "Light-weight issue tracker",
        "homepage": "https://github.com/lunared/tissue",
        "open": 129,
    },
    {
        "id": 2,
        "name": "C:\\raft",
        "description": "Retro dungeon crawler",
        "homepage": "https://smagac.github.io/",
        "open": 4
    },
]

def render_project(project):
    return f"""
        <tr>
            <td><a href="/cgi-bin/issues.py?project={project['id']}">{project['name']}</a></td>
            <td>{escape(project['description'])}</td>
            <td><a href="{project['homepage']}">{project['homepage']}</a></td>
            <td>{project['open']}</td>
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
    </article>
</body>
""")