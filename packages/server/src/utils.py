import base64

def b64decode(s):
    s_bytes = s.encode("utf-8")
    return base64.b64decode(s_bytes).decode('utf-8')