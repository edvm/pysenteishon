import sys
import platform
from distutils.core import setup as distutils_setup


def is_linux():
    return platform.system() == 'Linux'


def is_python3():
    return sys.version_info > (3, 0)


def dependencies_alright():
    if is_linux():
        try:
            from Xlib.display import Display
        except ImportError as exc:
            if is_python3():
                print('You must install python3-xlib to use Pysenteishon')
                print('Just type: pip install python3-xlib')
            else:
                print('You must install python-xlib to use Pytsenteishon')
                print('Just type: pip install svn+https://python-xlib.svn.sourceforge.net/svnroot/python-xlib/trunk/')
            return False

    return True


def setup():
    if not dependencies_alright():
        return
    distutils_setup(
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


setup()
