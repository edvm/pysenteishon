import os
import json
import uuid
import tempfile
import cherrypy
import pysenteishon

from functools import lru_cache
from pysenteishon.plugins.base import PysenteishonPlugin

try:
    import pyscreenshot as ImageGrab
except ImportError:
    print("Need to install pyscreenshot.")


class Screenshot(PysenteishonPlugin):

    def __init__(self):
        self.init_screenshot_dir()

    @property
    def screenshot_dir(self):        
        static_dir = os.path.join(os.path.split(pysenteishon.__file__)[0], 'static')
        return os.path.join(static_dir, 'screenshots')

    def init_screenshot_dir(self):
        if not os.path.isdir(self.screenshot_dir):
            os.makedirs(self.screenshot_dir)

    def execute(self):
        filename = uuid.uuid4()
        imagename = '{}.jpg'.format(filename)
        imagepath = os.path.join(self.screenshot_dir, imagename)
        ImageGrab.grab_to_file(imagepath)
        static_imagepath = '/screenshots/{}'.format(imagename)
        data = json.dumps({'image': static_imagepath})
        cherrypy.engine.publish('websocket-broadcast', data)