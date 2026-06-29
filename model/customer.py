class Customer:
    """موجودیت مشتری در سیستم صندوق"""
    def __init__(self, name, national_id, phone, customer_id=None, created_at=None):
        self.customer_id = customer_id
        self.name = name
        self.national_id = national_id
        self.phone = phone
        self.created_at = created_at