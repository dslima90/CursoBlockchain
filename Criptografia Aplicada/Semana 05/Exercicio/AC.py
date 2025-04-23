from cryptography import x509
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.x509.oid import NameOID
from datetime import datetime, timedelta, timezone
import random


class AC:
    def __init__(self):
        self.certificados = {}
        self.ca_certificate = None
        self.ca_private_key = None

    def self_signed_certificate(self, common_name="AC-Raiz", country="BR", state="SC", locality="Fln",
                                   organization="UFSC"):
        """
        Cria um certificado autoassinado para a CA.
        Args:
            common_name (str): O nome comum (CN) do certificado.
            country (str): O pais do certificado.
            state (str): O estado do certificado.
            locality (str): A cidade ou endereco do certificado.
            organization (str): O nome da CA.
        Returns:
            tuple: O certificado X.509 autoassinado e sua chave privada.
        """
        self.ca_private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)

        subject = issuer = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, country),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, state),
            x509.NameAttribute(NameOID.LOCALITY_NAME, locality),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, organization),
            x509.NameAttribute(NameOID.COMMON_NAME, common_name),
        ])

        self.ca_certificate = x509.CertificateBuilder() \
            .subject_name(subject) \
            .issuer_name(issuer) \
            .public_key(self.ca_private_key.public_key()) \
            .serial_number(random.randint(1, 1000000)) \
            .not_valid_before(datetime.now()) \
            .not_valid_after(datetime.now() + timedelta(days=1826)) \
            .add_extension(x509.BasicConstraints(ca=True, path_length=None), critical=True) \
            .sign(self.ca_private_key, hashes.SHA256())

        self.certificados[self.ca_certificate.serial_number] = self.ca_certificate

        return self.ca_certificate, self.ca_private_key

    def issue_end_certificate(self, public_key, common_name, country, state, locality, organization):
        """
        Emite um certificado final assinado pela CA
        Args:
            public_key (CryptoRSA.RsaKey): A chave publica do requerente do certificado.
            common_name (str): O nome comum (CN) do certificado.
            country (str): O pais do certificado.
            state (str): O estado do certificado.
            locality (str): A cidade ou endereco do certificado.
            organization (str): O nome da organizacao requerente.
        Returns:
            tuple: O certificado X.509.
        """

        subject = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, country),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, state),
            x509.NameAttribute(NameOID.LOCALITY_NAME, locality),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, organization),
            x509.NameAttribute(NameOID.COMMON_NAME, common_name),
        ])

        certificate = x509.CertificateBuilder() \
            .subject_name(subject) \
            .issuer_name(self.ca_certificate.subject) \
            .public_key(public_key) \
            .serial_number(random.randint(1, 1000000)) \
            .not_valid_before(datetime.now()) \
            .not_valid_after(datetime.now() + timedelta(days=365)) \
            .add_extension(x509.BasicConstraints(ca=False, path_length=None), critical=True) \
            .sign(self.ca_private_key, hashes.SHA256())

        self.certificados[certificate.serial_number] = certificate

        return certificate

    def validate_certificate(self, cert):
        """
        Valida um certificado e recupera a chave pública de um certificado com base no número de série.
        Args:
            cert (Certificate): O número de série do certificado.
        Returns:
            CryptoRSA.RsaKey or False: A chave publica do certificado, ou False se o certificado não for valido.
        """
        now = datetime.now(timezone.utc)
        if not (cert.not_valid_before_utc <= now <= cert.not_valid_after_utc):
            return False

        try:
            self.ca_certificate.public_key().verify(
                cert.signature,
                cert.tbs_certificate_bytes,
                padding.PKCS1v15(),
                cert.signature_hash_algorithm
            )
        except Exception as e:
            return False

        return cert.public_key()

minha_AC = AC() # Cria uma instancia da AC
minha_AC.self_signed_certificate() # Cria um certificado autoassinado
print(minha_AC.ca_certificate.serial_number) # Imprime o número de série do certificado
print(minha_AC.ca_certificate.issuer, minha_AC.ca_certificate.subject) # Imprime o issuer e o subject

chave_cliente = rsa.generate_private_key(public_exponent=65537, key_size=2048) # Cria uma chave privada rsa n2048
cert_cliente = minha_AC.issue_end_certificate(
    public_key=chave_cliente.public_key(), 
    common_name="Client", country="BR", state="SC",
    locality="Fln",organization="UFSC") # Cria um certificado para o cliente
print(cert_cliente.serial_number) # Imprime o número de série do certificado 
print(cert_cliente.issuer, cert_cliente.subject) # Imprime o issuer e o subject

outra_ac = AC() # Cria uma instancia da AC
outra_ac.self_signed_certificate() # Cria um certificado autoassinado
print(minha_AC.validate_certificate(outra_ac.ca_certificate))


