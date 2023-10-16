class Client:
    def __init__(self, **kwargs):
        self.client_id = kwargs['client_id']
        self.client_email = kwargs['client_email']
        self.client_name = kwargs['client_name']
        self.client_cases = kwargs['client_cases']

    def __str__(self, **kwargs):
        return f"Client ID: {self.client_id}\n" \
               f"Client Email: {self.client_email}\n" \
               f"Client Name: {self.client_name}\n" \
               f"Client Cases: {self.client_cases}\n"
