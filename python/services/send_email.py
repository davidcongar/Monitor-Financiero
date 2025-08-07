# python/services/send_email.py

import smtplib
from flask import render_template
import os

def send_html_email(subject, recipient_email, template, sender_name="Snapp Solutions", **kwargs):
    EMAIL_USUARIO = os.getenv("EMAIL_USUARIO")
    EMAIL_CONTRASENA = os.getenv("EMAIL_CONTRASENA")
    try:
        # Conexión con el servidor SMTP
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()

            # Verificar si las variables de entorno están correctamente cargadas
            if not EMAIL_USUARIO or not EMAIL_CONTRASENA:
                raise Exception(
                    "Las credenciales de correo no están configuradas correctamente."
                )

            # Iniciar sesión en la cuenta de correo
            server.login(EMAIL_USUARIO, EMAIL_CONTRASENA)

            # Renderizar la plantilla HTML con los datos
            html_content = render_template(template, **kwargs)

            # Construir el mensaje de correo
            from_email = f"{sender_name} <{EMAIL_USUARIO}>"
            message = f"Subject: {subject}\nFrom: {from_email}\nTo: {recipient_email}\nContent-Type: text/html\n\n{html_content}".encode(
                "utf-8"
            )

            # Enviar el correo
            server.sendmail(EMAIL_USUARIO, recipient_email, message)

    except smtplib.SMTPException as smtp_error:
        # Capturar errores específicos de SMTP
        raise Exception(f"Error SMTP al enviar el correo: {smtp_error}")

    except Exception as e:
        # Capturar cualquier otro error
        raise Exception(f"Error general al enviar el correo: {e}")


def forgot_password_email(recipient_email,contrasena):
    try:
        # Enviar correo al cliente
        send_html_email(
            subject="Nueva contraseña - Monitor Financiero",
            recipient_email=recipient_email,
            template="partials/email_template.html",
            body_content="Se acaba de crear una nueva contraseña para tu correo electrónico",
            details_list=[
                f"Nueva contraseña: {contrasena}"
            ]
        )
    except Exception as e:
        raise Exception(f"Error al enviar correos: {e}")

def new_user_email(recipient_email,contrasena):
    try:
        # Enviar correo al cliente
        send_html_email(
            subject="Monitor Financiero",
            recipient_email=recipient_email,
            template="partials/email_template.html",
            body_content="Se acaba de crear tu usuario para el Monitor Financiero.",
            details_list=[
                "URL Plataforma: noticia.us-east-2.elasticbeanstalk.com",
                f"Correo electrónico: {recipient_email}",
                f"Contraseña: {contrasena}"
            ]
        )
    except Exception as e:
        raise Exception(f"Error al enviar correos: {e}")