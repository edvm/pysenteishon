import sys
import platform
from distutils.core import setup as distutils_setup


def is_linux():
    return platform.system() == 'Linux'


def is_python3():
    return sys.version_info > (3, 0)


def setup():
    assert is_python3(), "Pysenteishon only runs with python >= 3."
    distutils_setup(
        name='pysenteishon',
        author='Emiliano Dalla Verde Marcozzi <edvm@fedoraproject.org>',
        version='0.2',
        package_dir={'': 'src'},
        install_requires=[r.strip() for r in open('requirements.txt', 'r').readlines()],
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


setup()
