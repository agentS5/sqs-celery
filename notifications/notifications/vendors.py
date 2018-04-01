class Vendors:
    def __init__(self, vendor_type):
        self.vendor_type = vendor_type
    def sms(self):
        return "Vendor Name " + self.vendor_type
    