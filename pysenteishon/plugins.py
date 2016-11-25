import os
import uuid
import cherrypy


def take_screenshot(filepath):
    """Take a screnshoot."""

    try :
        import Pillow
    except ImportError:
        print("Pillow not found, so take screenshot is disabled.")
        return

    try:
        import pyscreenshot as ImageGrab
    except ImportError:
        print("Need to install pyscreenshot.")

    filename = uuid.uuid4()
    filepath = os.path.join('/tmp', filename)
    im = ImageGrab.grab_to_file(filepath)
    cherrypy.engine.publish('/slides', filename)