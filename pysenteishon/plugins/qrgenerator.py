import pyqrcode
from pysenteishon.plugins.base import PysenteishonPlugin


class QRConsoleGenerator(PysenteishonPlugin):

    def qr_to_terminal(self, ip):
        ipqr = pyqrcode.create(ip)
        print(ipqr.terminal())
    
    def execute(self, ip):
        self.qr_to_terminal(ip)
