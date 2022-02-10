import smtplib
from email.message import EmailMessage


def notify(subject, message, to="herbemalveillante@gmail.com"):
    """
    Permet d'envoyer un mail à mon adresse pro pour me notifier de quelque chose d'important.
    """
    msg = EmailMessage()
    msg.set_content(message)
    msg["subject"] = subject

    user = "alerts.herbemalveillante@gmail.com"
    msg["from"] = user
    with open("mail_secret.txt") as file:
        password = file.read()
    msg["to"] = to

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(user, password)
    server.send_message(msg)
    server.quit()

    print("Notification envoyée avec succès.")


if __name__ == "__main__":
    notify("Ping !", "Pong !")

# >o)
# (_> HM
