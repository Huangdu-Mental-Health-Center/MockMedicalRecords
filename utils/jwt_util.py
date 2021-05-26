import base64
import json

def decode_raw_jwt_and_return_user_id_str(authorization_jwt_raw: str) -> str:
    try:
        authorization_jwt = authorization_jwt_raw.split(" ")[1]
        payload_base64_encoded = authorization_jwt.split(".")[1]
        missing_padding = len(payload_base64_encoded) % 4
        if missing_padding:
            payload_base64_encoded += '=' * (4 - missing_padding)
        jwt_payload = json.loads(base64.b64decode(payload_base64_encoded).decode('utf-8'))
        return jwt_payload["http://schemas.xmlsoap.org/ws/2005/05/identity/claims/nameidentifier"]
    except:
        return ""