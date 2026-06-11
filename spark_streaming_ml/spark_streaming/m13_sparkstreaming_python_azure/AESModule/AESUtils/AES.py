import hashlib
import base64
from cryptography.fernet import Fernet
from pyspark.sql.functions import udf, col
from pyspark.sql.types import StringType

class AESService:
    def __init__(self, key):
        # Process the key immediately upon initialization
        encryption_key = key or "my_default_secret_key"
        raw_key_bytes = encryption_key.encode('utf-8')
        hash_bytes = hashlib.sha256(raw_key_bytes).digest()
        self.safe_fernet_key = base64.urlsafe_b64encode(hash_bytes).decode('utf-8')

    def _encrypt_data(self, data):
        """
        Encrypts a string value using Fernet (AES).
        Instantiates Fernet locally to ensure Spark worker safety.
        """
        if data:
            try:
                # Re-instantiate Fernet here to avoid pickling the object across workers
                cipher_suite = Fernet(self.safe_fernet_key)
                encrypted_bytes = cipher_suite.encrypt(str(data).encode('utf-8'))
                return encrypted_bytes.decode('utf-8')
            except Exception:
                return None
        return None

    def _decrypt_data(self, data):
        """
        Decrypts a string value using Fernet (AES).
        Instantiates Fernet locally to ensure Spark worker safety.
        """
        if data:
            try:
                # Re-instantiate Fernet here to avoid pickling the object across workers
                cipher_suite = Fernet(self.safe_fernet_key)
                # Decode the input string to bytes, then decrypt
                decrypted_bytes = cipher_suite.decrypt(str(data).encode('utf-8'))
                return decrypted_bytes.decode('utf-8')
            except Exception:
                # If decryption fails (e.g. data wasn't encrypted or key is wrong), return None
                return None
        return None

    def encrypt_pii_columns(self, df, columns_to_encrypt):
        """
        Takes a DataFrame and a list of column names.
        Returns the DataFrame with those columns encrypted.
        """
        encrypt_udf = udf(self._encrypt_data, StringType())
        
        encrypted_df = df
        for column_name in columns_to_encrypt:
            if column_name in df.columns:
                print(f" -> Encrypting column: {column_name}")
                encrypted_df = encrypted_df.withColumn(column_name, encrypt_udf(col(column_name)))
        
        return encrypted_df

    def decrypt_pii_columns(self, df, columns_to_decrypt):
        """
        Takes a DataFrame and a list of column names.
        Returns the DataFrame with those columns decrypted.
        """
        decrypt_udf = udf(self._decrypt_data, StringType())
        
        decrypted_df = df
        for column_name in columns_to_decrypt:
            if column_name in df.columns:
                print(f" -> Decrypting column: {column_name}")
                decrypted_df = decrypted_df.withColumn(column_name, decrypt_udf(col(column_name)))
        
        return decrypted_df