"""
Integrate Jinja with RST / Sphinx

http://ericholscher.com/blog/2016/jul/25/integrating-jinja-rst-sphinx/
"""

from ...info import gammacat_info

gammacat_context = dict(
    version=gammacat_info.version,
)


def rstjinja(app, docname, source):
    """
    Render our pages as a jinja template for fancy templating goodness.
    """
    # Make sure we're outputting HTML
    if app.builder.format != 'html':
        return
    src = source[0]
    rendered = app.builder.templates.render_string(
        src,
        gammacat_context,
        # app.config.gammacat_context
    )
    source[0] = rendered


def setup(app):
    app.connect("source-read", rstjinja)
