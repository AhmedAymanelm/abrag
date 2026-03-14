import os
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from dotenv import load_dotenv

load_dotenv(override=True)

# Robust boolean parsing for environment variables
def get_env_bool(var_name: str, default: str) -> bool:
    val = os.getenv(var_name, default).lower()
    return val in ["true", "1", "t", "yes"]

# Debug log for Railway (without sensitive data)
print(f"DEBUG: Email Config - Server: {os.getenv('MAIL_SERVER', 'smtp.gmail.com')}, Port: {os.getenv('MAIL_PORT', '465')}, SSL: {os.getenv('MAIL_SSL_TLS', 'True')}, STARTTLS: {os.getenv('MAIL_STARTTLS', 'False')}")

conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME", ""),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD", ""),
    MAIL_FROM=os.getenv("MAIL_FROM", ""),
    MAIL_PORT=int(os.getenv("MAIL_PORT", 465)),
    MAIL_SERVER=os.getenv("MAIL_SERVER", "smtp.gmail.com"),
    MAIL_STARTTLS=get_env_bool("MAIL_STARTTLS", "False"),
    MAIL_SSL_TLS=get_env_bool("MAIL_SSL_TLS", "True"),
    USE_CREDENTIALS=get_env_bool("USE_CREDENTIALS", "True"),
    VALIDATE_CERTS=get_env_bool("VALIDATE_CERTS", "True"),
)


async def send_verification_email(email_to: str, token: str):
    html = f"""
    <div dir="rtl" style="font-family: Arial, sans-serif; text-align: right; padding: 20px;">
        <h2>تأكيد حساب أبراغ</h2>
        <p>مرحباً بك! لتأكيد حسابك، انسخ الكود التالي:</p>
        <div style="background: #f4f4f4; padding: 15px; margin: 20px 0; border-radius: 5px; word-break: break-all; text-align: left;" dir="ltr">
            <strong>{token}</strong>
        </div>
        <p>هذا الكود صالح لمدة 24 ساعة.</p>
    </div>
    """
    
    message = MessageSchema(
        subject="تأكيد حسابك - Abrag",
        recipients=[email_to],
        body=html,
        subtype=MessageType.html
    )
    
    fm = FastMail(conf)
    await fm.send_message(message)


async def send_reset_password_email(email_to: str, token: str):
    html = f"""
    <div dir="rtl" style="font-family: Arial, sans-serif; text-align: right; padding: 20px;">
        <h2>إعادة تعيين كلمة المرور</h2>
        <p>لقد طلبت إعادة تعيين كلمة المرور الخاصة بك. يرجى استخدام الكود التالي:</p>
        <div style="background: #f4f4f4; padding: 15px; margin: 20px 0; border-radius: 5px; word-break: break-all; text-align: left;" dir="ltr">
            <strong>{token}</strong>
        </div>
        <p>هذا الكود صالح لمدة 15 دقيقة.</p>
        <p>إذا لم تطلب هذا، يمكنك تجاهل هذه الرسالة.</p>
    </div>
    """
    
    message = MessageSchema(
        subject="إعادة تعيين كلمة المرور - Abrag",
        recipients=[email_to],
        body=html,
        subtype=MessageType.html
    )
    
    fm = FastMail(conf)
    await fm.send_message(message)
