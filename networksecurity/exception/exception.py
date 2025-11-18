import sys


class NetworkSecurityException(Exception):
    def __init__(self, error_message,error_details:sys):
        self.error_message = error_message
        _,_exc_tb = error_details.exc_info()
        self.lineno = _exc_tb.tb_lineno
        self.file_name = _exc_tb.tb_frame.f_code.co_filename
        
    def __str__(self):
        return f"Error occurred in script: {self.file_name} at line number: {self.lineno} with message: {self.error_message}"
