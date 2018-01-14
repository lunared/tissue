#!/usr/bin/env python3.6
from cgi import escape
import cgi
import cgitb
import os
cgitb.enable()

from tissue.models import get_db
from tissue.render import base_template

def show_form():
    form = cgi.FieldStorage()
    project = form.getvalue('project')
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT name FROM Projects WHERE id = ?", (project,))
    try:
        name = cur.fetchone()['name']
    except TypeError:
        raise ValueError("Invalid Project Id")
    finally:
        db.close()

    base_template(f"""
        <form id="issue-form" action="/cgi-bin/create_issue.py" target="_blank" method="post">
            <fieldset>
                <legend>Add Comment</legend>
                <table>
                    <tbody>
                        <tr>
                            <td>Project</td>
                            <td>{name}<input name="project" type="hidden" value="{project}"></td>
                        </td>
                        <tr>
                            <td>Author Name</td>
                            <td><input type="text" name="author"></td>
                        </tr>
                        <tr>
                            <td>Email</td>
                            <td><input type="email" name="email"></td>
                        </tr>
                        <tr>
                            <td>Title</td>
                            <td><input type="text" name="title"></td>
                        </tr>
                        <tr>
                            <td>Description</td>
                            <td><textarea name="body" rows="6"></textarea></td>
                        </tr>
                        <tr>
                            <td><button type="submit">Submit</button></td>
                        </tr>
                    </tbody>
                </table>
            </fieldset>
        </form>
    """)

def create():
    form = cgi.FieldStorage()
    project = form.getvalue('project')
    author = form.getvalue('author')
    email = form.getvalue('email')
    title = form.getvalue('title')
    body = form.getvalue('body')

    def validate():
        if author.lower().strip() == 'system':
            raise ValueError("Reserved author name detected")
        
    def open_ticket():
        db = get_db()
        cur = db.cursor()
        cur.execute(
            """
            INSERT INTO Issues (
                project_id,
                issue_num,
                author,
                email,
                title,
                body,
                opened,
                last_updated
            ) VALUES (
                ?,
                ( 
                    SELECT COALESCE(MAX(issue_num), 0) + 1
                    FROM Issues
                    WHERE project_id = ?
                ),
                ?,
                ?,
                ?,
                ?,
                CURRENT_TIMESTAMP,
                CURRENT_TIMESTAMP
            )
            """,
            (project,project,author,email,title,body)
        )
        issue = cur.lastrowid
        cur.execute(
            """
            INSERT INTO Comments (
                issue_id, author, body, created_at
            ) VALUES (
                ?,
                "System",
                "Ticket status changed to Open",
                CURRENT_TIMESTAMP
            )
            """,
            (issue,)
        )
        db.commit()
        db.close()
        return issue

    try:
        validate()
        issue = open_ticket()
        
        print("Status: 303 See other")
        print(f"Location: /cgi-bin/issue.py?id={issue}")
        print()
    except ValueError:
        print("Status: 406 Not Acceptable")
        print()
        print(e)


if os.environ['REQUEST_METHOD'] == 'GET':
    show_form()
elif os.environ['REQUEST_METHOD'] == 'POST':
    create()
else:
    raise Exception("Method Not Allowed")
    