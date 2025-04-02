from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from base64 import b64encode


mode = AES.MODE_CFB


def encrypt(key, filename, mode):
    """
    :param key: chave aes
    :param filename: nome do arquivo a ser cifrado
    :param mode: modo de operação desejado
    o texto cifrado é salvo em um arquivo e printado na tela em base64
    #Passo 1: abrir o arquivo no modo leitura
    #Passo 2: inicializar o AES com chave 'key' e modo de operação 'mode'
    #Passo 3: cifrar de acordo com o modo de operação escolhido. Pode precisar de
    um IV ou counter
    #Passo 4: salvar em outro arquivo o iv ou counter concatenado ao texto cifrado
    #Passo 5: mostrar na tela o resultado
    """
    
    cipher = AES.new(key, mode)
    
    with open(filename, 'rb') as f:
        
        data = f.read()

        texto_criptografado = cipher.encrypt(pad(data, AES.block_size))
        
        if mode == AES.MODE_ECB:
            iv = b''
            
        elif mode == AES.MODE_CTR:
            iv = cipher.nonce
        else:
            iv = cipher.iv
        
    with open(filename+'.enc', 'wb') as f:
        f.write(iv + texto_criptografado)

    print(b64encode(texto_criptografado), b64encode(iv), AES.block_size)


def decrypt(key, filename, mode):
    """
    :param key: chave aes
    :param filename: nome do arquivo a ser decifrado
    :param mode: modo de operação desejado
    retorna o texto decifrado
    #Passo 1: abrir o arquivo no modo leitura, recupera o IV e texto cifrado
    #Passo 2: inicializar a cifra com o IV de acordo com o modo de operação
    #Passo 3: Decifrar e retornar o texto decifrado
    """

    with open(filename, 'rb') as f:
        
        data = f.read()
        
        if mode == AES.MODE_ECB:
            cipher = AES.new(key, mode)
            iv = b""
            texto_criptografado = data
        elif mode == AES.MODE_CTR:
            iv = data[:8]
            cipher = AES.new(key, mode, nonce=iv)
            texto_criptografado = data[8:]
        else :
            iv = data[:AES.block_size]
            texto_criptografado = data[AES.block_size:]
            
            cipher = AES.new(key, mode, iv)

            
            
        print(b64encode(texto_criptografado), b64encode(iv), AES.block_size)

        plain_text = cipher.decrypt(texto_criptografado)
        
        # plain_text = unpad(plain_text, AES.block_size/2)
    
        
    print(plain_text)


# encrypt(b"averysecretkeyyyaverysecretkeyyy", 'test1.txt', mode)



decrypt(b"averysecretkeyyyaverysecretkeyyy", 'treasure.txt.enc', mode)