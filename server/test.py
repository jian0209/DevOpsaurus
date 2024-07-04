
import base64
import io
import time
import pyotp
import qrcode


def generate_qr_code(username: str) -> tuple[str, str]:
    secret_key = pyotp.random_base32()

    totp = pyotp.totp.TOTP(secret_key).provisioning_uri(
        name=username, issuer_name="devopsaurus")

    print(f"secret_key: {secret_key}")
    print(f"totp: {totp}")

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(totp)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

    return secret_key, img_base64


def verify_otp(secret_key: str, otp: str) -> bool:
    totp = pyotp.TOTP(secret_key)
    return totp.verify(otp)


if __name__ == '__main__':
    # generate_qr_code("admin")
    while True:
        print(verify_otp("Q6FQZO3HHQLIUYWTJKWNAC4DJYRLHTPR", input("Enter OTP: ")))
