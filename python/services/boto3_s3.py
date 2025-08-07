# python/services/s3_boto3.py

import os
import uuid

import boto3
from botocore.exceptions import ClientError

from python.models.modelos import *

class S3Service:
    def __init__(self, use_local_profile=False, profile_name="default"):
        """
        Inicializa el servicio de S3. Permite el uso de perfiles locales.

        :param use_local_profile: Indica si debe usarse un perfil local.
        :param profile_name: El nombre del perfil AWS a usar localmente.
        """
        if use_local_profile:
            session = boto3.Session(profile_name=profile_name)
            self.s3_client = session.client("s3")
        else:
            self.s3_client = boto3.client(
                "s3",
                aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
                aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
                region_name=os.getenv("AWS_REGION"),
            )
        self.bucket_name = os.getenv("AWS_S3_BUCKET_NAME")

    def upload_file(self, file,file_uuid):
        """
        Sube un archivo a S3 con un nombre UUID y lo guarda en la base de datos.

        :param file: Archivo a subir.
        :return: URL del archivo subido.
        """
        try:
            filename = file.filename
            filepath = f"{file_uuid}_{filename}"
            # Subir a S3
            self.s3_client.upload_fileobj(file, self.bucket_name, filepath)
            return filename
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Error al subir el archivo: {e}")

    def generate_presigned_url(self, filepath, expiration=3600):
        """
        Genera una URL firmada para acceder al archivo de S3.

        :param filepath: La ruta del archivo en el bucket.
        :param expiration: Tiempo de expiración de la URL en segundos.
        :return: URL firmada.
        """
        try:
            response = self.s3_client.generate_presigned_url(
                "get_object",
                Params={"Bucket": self.bucket_name, "Key": filepath},
                ExpiresIn=expiration,
            )
            
            return response
        except ClientError as e:
            raise Exception(f"Error al generar la URL firmada: {e}")
