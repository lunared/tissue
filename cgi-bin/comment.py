#!/usr/bin/env python3.6
from cgi import escape
import cgi
import cgitb
cgitb.enable()

from tissue.models import get_db

form = cgi.FieldStorage()
issue = form.getvalue('issue')
author = form.getvalue('author')
email = form.getvalue('email')
body = form.getvalue('body')
state = form.getvalue('state')

def validate(cursor):
    errors = {}
    if author is None:
        errors['author'] = "Author field is required"
    elif author.lower().strip() == 'system':
        errors['author'] = "Reserved author name detected"
    
    if email is None:
        errors['email'] = "Email field is required"

    if body is None:
        errors['body'] = "Body field is required"
    elif len(body.strip()) == 0:
        errors['body'] = "Body length must be greater than 0 characters"

    if issue is None:
        errors['issue'] = "Comment must belong to an issue"
    else:
        model = cursor.execute(
            """
            SELECT * FROM Issues WHERE id = ?
            """,
            (issue,)
        ).fetchone()
        if model is None:
            errors['issue'] = "Issue does not exist"
        elif state is not None and model['state'] == state:
            errors['state'] = "Can not change to the same state"

    if len(errors) > 0:
        raise ValueError(errors)

db = get_db()
try:
    cur = db.cursor()
    validate(cur)
    # write to database
    cur.execute(
        """
        INSERT INTO Comments (issue_id, author, email, body, created_at) VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
        """,
        (issue, author, email, body)
    )
    cur.execute(
        """
        UPDATE Issues 
        SET last_updated = CURRENT_TIMESTAMP
        WHERE id = ?
        """,
        (issue,)
    )

    if state is not None:
        cur.execute(
            """
            INSERT INTO Comments (
                issue_id, author, body, created_at
            ) VALUES (
                ?,
                "System",
                ?,
                CURRENT_TIMESTAMP
            )
            """,
            (issue, f"Ticket status changed to {state} by {author} <{email}>")
        )
        cur.execute(
            """
            UPDATE Issues
            SET state = ?
            WHERE id = ?
            """,
            (state, issue)
        )

    db.commit()

    print("Status: 303 See other")
    print(f"Location: /cgi-bin/issue.py?id={issue}")
    print()
except ValueError as e:
    print("Status: 406 Not Acceptable")
    print()
    print(e)
finally:
    db.close()
