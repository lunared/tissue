def _render_banner(project=None):
    return f"""
    <h1><a href="/cgi-bin/projects.py">Tissue</a> - Lightweight Issue Tracker</h1>
    """
def _copyright():
    return f"""
        Copyright &copy; 2018 Luna.Red. All Rights Reverse Engineered.
    """

def base_template(content):
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
            {_render_banner()}
        </header>
        <article>
            {content}
        </article>
        <footer>
            {_copyright()}
        </footer>
    </body>
    """)