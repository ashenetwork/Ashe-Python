
class ASHEError(Exception):
  def __init__(self, message=None, code="0"):
    super(ASHEError, self).__init__(message)
    self.message = message
    self.code = code
