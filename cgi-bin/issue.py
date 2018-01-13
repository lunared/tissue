#!/usr/bin/env python3.6
from cgi import escape
import cgi
import cgitb
cgitb.enable()

from tissue.render import render_banner


ticket_name = cgi.escape("Hello World <b>Test</b>")

issue = {
    "project": "tissue",
    "id": 1,
    "author": "Nicholas Hydock",
    "email": "nick@luna.red",
    "title": "Test Issue doesn't even show up properly",
    "text": "Y'all are dinguses, you really think you can provide an app that doesn't even work???\n\n people are even going to use it, the fuck is your problem.",
    "state": 'Open',
    "time": "2018-01-12T9:24:12-04:00",
    "lastUpdated": "2018-01-12T10:24:12-04:00",
}

comments = [
    {
        "author": "System",
        "text": "Ticket opened",
        "time": "2018-01-12T9:24:12-04:00",
    },
    {
        "author": "Nicholas Hydock",
        "email": "nick@luna.red",
        "text": "This app is trash, wtf, why is there such a bug in it.",
        "time": "2018-01-12T9:25:29-04:00",
    },
    {
        "author": "Patrick Flanagan",
        "email": "pjf@luna.red",
        "text": "Not enough GNU and/or too much GNU.  Have you tried running it on a BSD server?",
        "time": "2018-01-12T10:07:33-04:00",
    },
    {
        "author": "Chris Hersh",
        "email": "satan@luna.red",
        "text": "Rewrite it in Rust",
        "time": "2018-01-12T10:24:12-04:00",
    }
]

STATES = [
    'Open',
    'Closed'
]

selected_state = 'Open'

def show_email(c):
    if c.get("email") is not None:
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
                <td>{issue['time']}</td>
            <tr>
            <tr>
                <td>Last Updated</td>
                <td>{issue['lastUpdated']}</td>
            <tr>
            <tr>
                <td>Summary</td>
                <td>{escape(issue['text'])}</td>
            </tr>
        </tbody>
    </table>
    """

def render_comments():

    def comment(c):
        return f"""
            <div class="comment">
                <strong>{escape(c['author'])}</strong>{show_email(c)}<br>
                <sub>{escape(c['time'])}</sub><br>
                <p>
                    {
                        escape(c['text'])
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
        <form id="comment-form" action="/comment.py" target="_blank" method="post">
            <fieldset>
                <legend>Add Comment</legend>
                <table>
                    <tbody>
                        <tr>
                            <td>Author Name</td>
                            <td><input type="text" name="name"></td>
                        </tr>
                        <tr>
                            <td>Email</td>
                            <td><input type="email" name="email"></td>
                        </tr>
                        <tr>
                            <td>Comment</td>
                            <td><textarea name="comment" rows="4"></textarea></td>
                        </tr>
                        <tr>
                            <td>Change State</td>
                            <td>
                                <select name="state">
                                    <option selected>--</option>
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

## HEADERS
print("Content-Type: text/html")
print("")

## CONTENT
print(f"""
<head>
    <title>Tissue - {ticket_name}</title>
    <link rel="stylesheet" type="text/css" href="/static/style.css">
</head>
<body>
    <header>
        {render_banner(issue['project'])}
    </header>
    <article>
        {render_ticket()}
        <h2>Activity</h2>
        {render_comments()}
    </article>
    <footer>
        {comment_form()}
    </footer>
</body>
""")