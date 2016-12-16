import os
import json
import uuid
import cherrypy
import pysenteishon
import pyscreenshot as ImageGrab
from pysenteishon.plugins.base import PysenteishonPlugin


class Screenshot(PysenteishonPlugin):

    def __init__(self):
        os.makedirs(self.screenshot_dir, exist_ok=True)

    @property
    def screenshot_dir(self):
        static_dir = os.path.join(os.path.split(pysenteishon.__file__)[0], 'static')
        return os.path.join(static_dir, 'screenshots')

    def execute(self):
        filename = uuid.uuid4()
        imagename = '{}.jpg'.format(filename)
        imagepath = os.path.join(self.screenshot_dir, imagename)
        ImageGrab.grab_to_file(imagepath)
        static_imagepath = os.path.join('screenshots', imagename)
        data = json.dumps({'image': static_imagepath})
        cherrypy.engine.publish('websocket-broadcast', data)
