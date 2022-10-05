# Configuration file for the Sphinx documentation builder.

# -- Project information
project = "tosclib"
copyright = "2022, Alberto Valdez"
author = "Alberto Valdez"

release = "1.0"
version = "1.0.0"

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
    "sphinx_toolbox.more_autodoc.variables",
    "sphinx_toolbox.more_autodoc.typehints",
    "sphinx_toolbox.more_autodoc.genericalias",
    "sphinx_toolbox.more_autodoc.overloads",
]

html_static_path = ["_static"]
source_suffix = [".rst", ".md"]
suppress_warnings = ["ref.python"]
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
autodoc_typehints_description_target = "documented"
autodoc_class_signature = "separated"
autodoc_default_options = {
    "member-order": "bysource",
    "exclude-members": "__new__, __init__",
}

html_theme = "furo"
# https://sphinx-themes.org/sample-sites/furo/kitchen-sink/admonitions/
