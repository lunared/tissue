def render_banner(project=None):
    p = f"""
    &gt; <a href="/cgi-bin/issues.py?project={project}">{project}</a>
    """ if project is not None else ""

    return f"""
    <h1>Tissue - Lightweight Issue Tracker</h1>
    <nav>
        <a href="/cgi-bin/projects.py">Projects</a>{p}
    </nav>
    """
