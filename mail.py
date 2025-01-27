import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import requests
import os

def enviar_correo_con_adjunto(sender_email, recipient_emails, subject, body, attachment_path,
                              smtp_host='smtp.gmail.com', smtp_port=587, username=None, password=None):
    """
    Envía un correo electrónico con un archivo adjunto utilizando un servidor SMTP.
    """
    # Crear la estructura del correo
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = ', '.join(recipient_emails)
    msg['Subject'] = subject

    # Adjuntar el cuerpo en texto plano
    msg.attach(MIMEText(body, 'plain'))

    # Agregar el archivo adjunto
    try:
        with open(attachment_path, 'rb') as attachment_file:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment_file.read())
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f"attachment; filename={os.path.basename(attachment_path)}"
        )
        msg.attach(part)
    except Exception as e:
        print(f"Error al adjuntar el archivo: {e}")
        return

    # Conectar al servidor SMTP y enviar el correo
    try:
        # Usamos SMTP normal con puerto 587
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.ehlo()  # Identificarnos con el servidor
            server.starttls()  # Encriptar la conexión
            server.ehlo()
            if username and password:
                server.login(username, password)
            server.sendmail(sender_email, recipient_emails, msg.as_string())
            print("Correo enviado exitosamente con adjunto.")
    except Exception as e:
        print(f"Error al enviar el correo: {e}")


def descargar_pdf(url, nombre_archivo):
    """Descarga un PDF desde la url especificada y lo guarda con el nombre indicado."""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Lanza error si no recibe un status 200
        with open(nombre_archivo, 'wb') as f:
            f.write(response.content)
        print(f"PDF descargado correctamente: {nombre_archivo}")
    except Exception as e:
        print(f"Error al descargar el PDF: {e}")


def main():
    """
    1. Descarga el PDF.
    2. Envía el correo con el PDF adjunto.
    """
    # URL real con un PDF de prueba
    url_del_pdf = "https://www.sharedfilespro.com/shared-files/38/?10-page-sample.pdf&download=1"
    nombre_archivo_pdf = "archivo_descargado.pdf"
    descargar_pdf(url_del_pdf, nombre_archivo_pdf)

    sender_email = "Tu_Mail"
    recipient_emails = ["mail1", "mail2"]
    subject = "Reporte mensual"
    body = "Adjunto encontrarás el reporte mensual en formato PDF."
    
    enviar_correo_con_adjunto(
        sender_email=sender_email,
        recipient_emails=recipient_emails,
        subject=subject,
        body=body,
        attachment_path=nombre_archivo_pdf,
        smtp_host='smtp.gmail.com',
        smtp_port=587,
        username="Tu_Mail",
        password="Tu_clave_de_Gmail"
    )


if __name__ == "__main__":
    main()
