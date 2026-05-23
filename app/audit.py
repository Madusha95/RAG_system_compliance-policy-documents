import json


class AuditLogger:
    """
    Handles audit logging for all query requests.

    Each query is appended to audit.log in JSON Lines format,
    allowing full reconstruction of:
    - user question
    - model response
    - retrieved context
    - errors (if any)
    """
    def __init__(self, file_path: str = "audit.log"):
        # Path to the audit log file
        self.file_path = file_path

    # Open audit log in append mode
    def write(self, data: dict):
        with open(self.file_path, "a", encoding="utf-8") as file:
             # Convert dictionary to JSON string and write as one line
            file.write(json.dumps(data, ensure_ascii=False) + "\n")