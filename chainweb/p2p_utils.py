import base64
def _isBase64(base64String):
    try:
        if isinstance(base64String, str):
                # If there's any unicode here, an exception will be thrown and the function will return false
                sb_bytes = bytes(base64String, 'ascii')
        elif isinstance(base64String, bytes):
                sb_bytes = base64String
        else:
                raise ValueError("Argument must be string or bytes")
        return base64.b64encode(base64.b64decode(sb_bytes)) == sb_bytes
    except Exception:
            return False