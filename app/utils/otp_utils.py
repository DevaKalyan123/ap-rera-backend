import random
import time

OTP_STORE = {}  # {pan: {"otp": "123456", "expires": timestamp}}

def generate_otp(pan):
    otp = str(random.randint(100000, 999999))
    OTP_STORE[pan] = {
        "otp": otp,
        "expires": time.time() + 300  # 5 minutes
    }
    return otp


def verify_otp(pan, otp):
    data = OTP_STORE.get(pan)

    if not data:
        return False

    if time.time() > data["expires"]:
        OTP_STORE.pop(pan, None)
        return False

    if data["otp"] == otp:
        OTP_STORE.pop(pan, None)
        return True

    return False