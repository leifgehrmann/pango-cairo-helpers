from pathlib import Path
import sys
import os

extensions = [
    'sphinx.ext.autodoc', 'sphinx.ext.intersphinx', 'sphinx.ext.coverage']
master_doc = 'index'
project = 'pangocairohelpers'
copyright = '2019, Leif Gehrmann'
release = (Path(__file__).parent.parent / 'pangocairohelpers' / 'VERSION').read_text().strip()
version = '.'.join(release.split('.')[:2])
exclude_patterns = ['_build']
autodoc_member_order = 'bysource'
autodoc_default_flags = ['members']

sys.path.insert(0, os.path.abspath('..'))

html_theme = "sphinx_rtd_theme"
