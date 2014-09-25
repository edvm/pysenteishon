from distutils.core import setup


setup(
    name='pysenteishon',
    author='Emiliano Dalla Verde Marcozzi <edvm@fedoraproject.org>',
    version='0.1',
    package_dir={'': 'src'},
    packages=[''],
    entry_points={
        'console_scripts': [
            'pysenteishon = src.web:run_pysenteishon']
    }
)
