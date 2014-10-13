from distutils.core import setup


setup(
    name='pysenteishon',
    author='Emiliano Dalla Verde Marcozzi <edvm@fedoraproject.org>',
    version='0.1',
    package_dir={'': 'src'},
    package_data={
        '': [
            'templates/*',
            'static/js/*.js',
            'static/css/*.css',
            'static/font-awesome/css/*',
            'static/font-awesome/scss/*',
            'static/font-awesome/less/*',
            'static/font-awesome/fonts/*',
        ]
    },
    packages=[''],
    scripts=[
        'scripts/pysenteishon',
    ]
)
