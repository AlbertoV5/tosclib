# Configuration file for the Sphinx documentation builder.

# -- Project information
project = 'tosclib'
copyright = '2022, Alberto Valdez'
author = 'Alberto Valdez'

release = '0.1'
version = '0.1.3'

# -- General configuration

extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.intersphinx',
    # 'sphinx.ext.viewcode'
]

intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
}
intersphinx_disabled_domains = ['std']

# -- Options for HTML output
# https://docs.readthedocs.io/en/latest/guides/adding-custom-css.html

html_theme = 'sphinx_rtd_theme'
# html_theme_options = {
#     "style_nav_header_background" : '#2d2d2d',
# }

html_theme = 'furo'
html_theme = 'sphinx_book_theme'
html_theme = 'insegel' # https://sphinx-themes.org/sample-sites/insegel/kitchen-sink/admonitions/

# -- Options for EPUB output
epub_show_urls = 'footnote'


