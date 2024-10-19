import smtplib
import os

def send_text_to_self(subject: str, message: str, user:str, guild:str) -> bool:
    sender = os.getenv("MY_EMAIL")
    receipient = os.getenv("MY_PHONE_EMAIL")
    password = os.getenv("MY_APP_PASSWORD")

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender, password)
            out = f"\nFrom: {user} In {guild}\n\nSubject: {subject}\n\n{message}"
            result = server.sendmail(sender, receipient, out)
            if result == {}:
                return True
            else:
                print(f"Hmmm smth went wrong during SMTP transfer {result}")
                return False

    except Exception as e: 
        print(f"Sending text message to self failed {e}")
        return False