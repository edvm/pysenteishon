import pyqrcode

def qr_to_terminal(ip):
    ipqr = pyqrcode.create(ip)
    print(ipqr.terminal())
