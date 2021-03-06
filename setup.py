import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.txt')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

requires = [
    'plaster_pastedeploy',
    'setuptools == 39.0.1',
    'pyramid',
    'pyramid_mako',
    'pyramid_debugtoolbar',
    'waitress',
    'holidays',
    'pandas',    
    'openpyxl',
    'psycopg2-binary',
    'pdfrw',
    'pyPDF2',
    'tinycss2 == 0.6.0',
    'pdfkit == 0.6.1',
    'cairocffi == 0.9.0',
    'weasyprint == 43'
]

tests_require = [
    'WebTest >= 1.3.1',  # py3 compat
    'pytest >= 3.7.4',
    'pytest-cov',
]

setup(
    name='pay_calculator',
    version='0.0',
    description='pay_calculator',
    long_description=README + '\n\n' + CHANGES,
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Pyramid',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
    ],
    author='',
    author_email='',
    url='',
    keywords='web pyramid pylons',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    extras_require={
        'testing': tests_require,
    },
    install_requires=requires,
    entry_points={
        'paste.app_factory': [
            'main = pay_calculator:main',
        ],
    },
)
