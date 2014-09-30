from distutils.core import setup


setup(
    name='pysenteishon',
    author='Emiliano Dalla Verde Marcozzi <edvm@fedoraproject.org>',
    version='0.1',
    package_dir={'': 'src'},
    package_data={'': ['templates/*', 'static/*']},
    packages=[''],
    scripts=[
        'scripts/pysenteishon',
    ]
)
