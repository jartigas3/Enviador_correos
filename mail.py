import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import requests
import os
import logging
import datetime


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="app.log",  
    filemode="a"         
)

def enviar_correo_con_adjunto(sender_email, recipient_emails, subject, body, attachment_path,
                              smtp_host='smtp.gmail.com', smtp_port=587, username=None, password=None):
    """
    Envía un correo electrónico con un archivo adjunto utilizando un servidor SMTP.
    """
    logging.info("Preparando el correo con adjunto...")  
    
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
        logging.info(f"Archivo adjunto '{attachment_path}' agregado correctamente.")
    except Exception as e:
        logging.error(f"Error al adjuntar el archivo: {e}")
        return

    # Conectar al servidor SMTP y enviar el correo
    try:
        logging.info(f"Conectando al servidor SMTP ({smtp_host}:{smtp_port})...")
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            if username and password:
                logging.info("Iniciando sesión en el servidor SMTP...")
                server.login(username, password)
            server.sendmail(sender_email, recipient_emails, msg.as_string())
            logging.info("Correo enviado exitosamente con adjunto.")
            logging.info("Correo enviado a los destinatarios: " + ', '.join(recipient_emails))
    except Exception as e:
        logging.error(f"Error al enviar el correo: {e}")


def descargar_pdf(url, nombre_archivo):
    """Descarga un PDF desde la url especificada y lo guarda con el nombre indicado."""
    logging.info(f"Iniciando descarga del PDF desde la URL: {url}")  
    try:
        response = requests.get(url)
        response.raise_for_status()  # Lanza error si no recibe un status 200
        with open(nombre_archivo, 'wb') as f:
            f.write(response.content)
        logging.info(f"PDF descargado correctamente en '{nombre_archivo}'.")
    except Exception as e:
        logging.error(f"Error al descargar el PDF: {e}")


def main():
    """ 
    1. Descarga el PDF.
    2. Envía el correo con el PDF adjunto.
    """
    logging.info("===== Inicio de la ejecución del programa =====")  
    logging.info("===== Extrayendo fecha =====")

    hoy = datetime.datetime.now()
    año = hoy.year
    mes = hoy.month

    logging.info(f"===== url extraído: http://161.131.215.59:8090/wsRentabilidadJs/descargar?ano={año}&mes={mes}&grupo=1&rut=0&sesion=1 =====")

    
    # URL real con un PDF de prueba (ajusta a tus necesidades)
    url_del_pdf = f"http://161.131.215.59:8090/wsRentabilidadJs/descargar?ano={año}&mes={mes}&grupo=1&rut=0&sesion=1"
    nombre_archivo_pdf = "archivo_descargado.pdf"

    # 2) Descarga el PDF
    descargar_pdf(url_del_pdf, nombre_archivo_pdf)

    # 3) Enviar el correo
    sender_email = "gmail"
    recipient_emails = ["mail1", "mail2"]
    subject = "Reporte mensual"
    body = "Adjunto encontrarás el reporte mensual en formato PDF."
    
    logging.info("Iniciando el proceso de envío de correo...")  
    enviar_correo_con_adjunto(
        sender_email=sender_email,
        recipient_emails=recipient_emails,
        subject=subject,
        body=body,
        attachment_path=nombre_archivo_pdf,
        smtp_host='smtp.gmail.com',
        smtp_port=587,
        username="gmail",
        password="clave_2_pasos"  
    )

    logging.info("===== Fin de la ejecución del programa =====\n")


if __name__ == "__main__":
    main()
