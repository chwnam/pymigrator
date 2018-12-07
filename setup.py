from distutils.core import setup

setup(
    name='pymigrator',
    version='2.4.0',
    description='A simple tabular data converter, especially for WordPress',
    author='Changwoo Nam',
    author_email='cs.chwnam@gmail.com',
    packages=['pymigrator', 'pymigrator.core', 'pymigrator.wp'],
    package_dir={'pymigrator': 'pymigrator'},
    url='http://changwoo.pe.kr/'
)
