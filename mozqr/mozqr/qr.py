import qrcode

class Qr:
    def __init__(self, data):
        self.data = data

    def makeqr_code(self, filename):
        self.qr = qrcode.make(self.data)
        self.qr.save(filename)
        return f"Your Qr code has been saved as {filename}"
    
    def showqr(self):
        return self.qr.show()
    