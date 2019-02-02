
import io
import os
import re

_docs_path = os.path.dirname(__file__)
_version_path = os.path.abspath(os.path.join(_docs_path, '..', 'aiofunctools', '__init__.py'))
with io.open(_version_path, 'r', encoding='latin1') as fp:
    try:
        _version_info = re.search(r"^__version__ = '"
                                  r"(?P<major>\d+)"
                                  r"\.(?P<minor>\d+)"
                                  r"\.(?P<patch>\d+)"
                                  r"(?P<tag>.*)?'$",
                                  fp.read(), re.M).groupdict()
    except IndexError:
        raise RuntimeError('Unable to determine version.')

extensions = [
    'm2r'
]

source_suffix = '.rst'


master_doc = 'index'

project = 'aiolambda'
copyright = 'Aiolambda contributors'

version = '{major}.{minor}'.format(**_version_info)
release = '{major}.{minor}.{patch}{tag}'.format(**_version_info)

exclude_patterns = ['_build', 'requirements.txt']

highlight_language = 'python3'

html_theme_options = {
    'description': 'Python async microservices fasts and functional',
    'canonical_url': 'http://docs.aiolambda.org/en/stable/',
    'github_user': 'pando85',
    'github_repo': 'aiolambda',
    'github_button': True,
    'github_type': 'star',
    'github_banner': True,
}

html_static_path = ['_static']

texinfo_documents = [
    ('index', 'aiolambda', 'aiolambda Documentation',
     'Pando85', 'aiolambda', 'One line description of project.',
     'Miscellaneous'),
]
