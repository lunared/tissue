#!/usr/bin/env python3.6
from cgi import escape
import cgi
import cgitb
cgitb.enable()

location = "http://localhost"
issue = 1

print(f'''
Status: 303 See other
Location: {location}/cgi-bin/issue.py?id={issue}

''')