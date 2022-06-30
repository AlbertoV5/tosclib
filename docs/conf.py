# Configuration file for the Sphinx documentation builder.

# -- Project information
project = "tosclib"
copyright = "2022, Alberto Valdez"
author = "Alberto Valdez"

release = "0.5"
version = "0.5.0"

# -- General configuration

extensions = [
    "sphinx.ext.duration",
    "sphinx.ext.doctest",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.intersphinx",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
    "sphinx_copybutton",
]

exclude_patterns = ["build"]

intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "sphinx": ("https://www.sphinx-doc.org/en/master/", None),
}
intersphinx_disabled_domains = ["std"]

# Napoleon Ext
napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_attr_annotations = True

autodoc_typehints = "description"
autodoc_class_signature = "separated"

html_theme = "furo"
