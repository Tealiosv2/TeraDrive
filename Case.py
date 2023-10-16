
class Case:
    def __init__(self, **kwargs):
        self.case_id = kwargs["case_id"]
        self.client_id = kwargs["client_id"]
        self.case_status = kwargs["case_status"]
        self.case_notes = kwargs["case_notes"]
    
    def __str__(self):
        return f"Case ID: {self.case_id}\n" \
                f"Client Email: {self.client_id}\n" \
                f"Case Status: {self.case_status}\n" \
                f"Case Notes: {self.case_notes}\n"
