#!/usr/bin/env python3.6
from cgi import escape
import cgi
import cgitb
cgitb.enable()

from tissue.render import base_template
from tissue.models import get_db

form = cgi.FieldStorage()
id = form.getvalue('id')

ticket_name = cgi.escape("Hello World <b>Test</b>")

db = get_db()
cur = db.cursor()
cur.execute("SELECT * FROM Issues WHERE id = ?", (id,))
issue = cur.fetchone()
cur.execute("SELECT * FROM Comments WHERE issue_id = ?", (id,))
comments = cur.fetchall()[:]
db.close()

STATES = [
    'Open',
    'Closed'
]

selected_state = 'Open'

def show_email(c):
    if c["email"] is not None:
        return f"""<i>&lt;{escape(c["email"])}&gt;</i>"""
    return ""

def render_ticket():
    return f"""
    <h1>#{issue['id']} - {escape(issue['title'])}</h1>
    <table summary="issue-summary" class="issue">
        <tbody>
            <tr>
                <td>Author</td>
                <td>{issue['author']} {show_email(issue)}</td>
            </tr>
            <tr>
                <td>State</td>
                <td>{issue['state']}</td>
            </tr>
            <tr>
                <td>Opened At</td>
                <td>{issue['opened']}</td>
            <tr>
            <tr>
                <td>Last Updated</td>
                <td>{issue['last_updated']}</td>
            <tr>
            <tr>
                <td>Summary</td>
                <td>{escape(issue['body'])}</td>
            </tr>
        </tbody>
    </table>
    """

def render_comments():

    def comment(c):
        return f"""
            <div class="comment">
                <strong>{escape(c['author'])}</strong>{show_email(c)}<br>
                <sub>{escape(c['created_at'])}</sub><br>
                <p>
                    {
                        escape(c['body'])
                    }
                </p>
            </div>
        """

    return f"""
    {"".join([comment(c) for c in comments])}
    """

def comment_form():
    state_dropdown = "".join([
        f'<option value="{s}">{s}</option>' 
        for s in STATES
    ])

    return f"""
        <form id="comment-form" action="/cgi-bin/comment.py" method="post">
            <input type="hidden" name="issue" value="{id}" />
            <fieldset>
                <legend>Add Comment</legend>
                <table>
                    <tbody>
                        <tr>
                            <td>Author Name</td>
                            <td><input type="text" name="author" required></td>
                        </tr>
                        <tr>
                            <td>Email</td>
                            <td><input type="email" name="email" required></td>
                        </tr>
                        <tr>
                            <td>Comment</td>
                            <td><textarea name="body" rows="4" required></textarea></td>
                        </tr>
                        <tr>
                            <td>Change State</td>
                            <td>
                                <select name="state">
                                    <option value="" selected>--</option>
                                    {state_dropdown}
                                </select>
                            </td>
                        </tr>
                        <tr>
                            <td><button type="submit">Submit</button></td>
                        </tr>
                    </tbody>
                </table>
            </fieldset>
        </form>
    """

base_template(f"""
{render_ticket()}
<h2>Activity</h2>
{render_comments()}
{comment_form()}
""")