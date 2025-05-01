import hashlib
from datetime import datetime


def to_dict(instance):
    return {c.name: getattr(instance, c.name) for c in instance.__table__.columns}


def generate_token(username: str) -> str:
    now = datetime.now().isoformat()
    raw_string = f"{username}:{now}"
    token = hashlib.sha256(raw_string.encode()).hexdigest()[:20]
    return token
