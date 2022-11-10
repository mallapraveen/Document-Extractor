class CustomException(Exception):
    """Custom Exception

        Attributes:
            message -- explanation of the error
        """

    def __init__(self, message="Request failed"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message}'


class BearerAccessToken(Exception):
    """Exception raised for errors in getting the bearer access token.

    Attributes:
        status_code -- status code of the request made
        message -- explanation of the error
    """

    def __init__(self, status_code, message="Request failed"):
        self.status_code = status_code
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'Status Code:{self.status_code} -> {self.message}'


class GetFileId(Exception):
    """Exception raised for errors in getting NGIN file system.

    Attributes:
        file_id -- fileId of the image
        status_code -- status code of the request made
        message -- explanation of the error
    """

    def __init__(self, file_id, status_code, message="Request failed"):
        self.file_id = file_id
        self.status_code = status_code
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.status_code} -> {self.message}'


class TesseractOCR(CustomException):
    """Exception raised for errors in Tesseract Extraction Service.
    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        super().__init__(f"Tesseract Extraction Failed with error --> {message}")


class Aadhar_Extraction(CustomException):
    """Exception raised for errors in Aadhar Model Extraction.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        super().__init__(f"Aadhar Model Extraction failed with error --> {message}")


class PAN_Extraction(CustomException):
    """Exception raised for errors in PAN Model Extraction.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        super().__init__(f"PAN Model Extraction failed with error --> {message}")


class Cheque_Extraction(CustomException):
    """Exception raised for errors in PAN Model Extraction.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        super().__init__(f"Cheque Model Extraction failed with error --> {message}")


class Classify_Document(CustomException):
    """Exception raised for errors in PAN Model Extraction.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        super().__init__(f"Classification of document failed with error --> {message}")


class Classify_Extract_Document(CustomException):
    """Exception raised for errors in PAN Model Extraction.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        super().__init__(f"Classification and extraction of document failed with error --> {message}")
