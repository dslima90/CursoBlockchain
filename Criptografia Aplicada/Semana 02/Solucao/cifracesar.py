
"""

Enunciado:

A chave foi cifrada usando uma técnica de cifragem antiga e resultou no
seguinte texto:

dyhubvhfuhwnhbbbdyhubvhfuhwnhbbb


Algoritmo para testar se a cifra de César funciona para descriptografar essa string, que deve ser uma chave de 256 bits.

"""

CHAVE_PROF_THAIS = "dyhubvhfuhwnhbbbdyhubvhfuhwnhbbb"

def rotate(plain_list: list, x):
    """
        Rotaciona uma lista de acordo com um numero de posicoes dado.
    """
    return plain_list[-x:] + plain_list[:-x]

def caesarCipher(plain_text: str, key: int) -> str:
    """
    Aplica a cifra de César ao texto fornecido usando o deslocamento especificado.

    Args:
        texto (str): O texto a ser criptografado (ou descriptografado).
        key (int): A chave de deslocamento para a cifra de César.

    Returns:
        str: O texto criptografado (ou descriptografado).
    
    """
    
    ALPHABET = "abcdefghijklmnopqrstuvwxyz"
    
    rotated_alphabet = rotate(ALPHABET, key % len(ALPHABET)) # rotaciona o alfabeto de acordo com a chave
    
    plain_text = plain_text.lower() # garante tudo minusculo
    
    result = [ # converte do alfabeto para o alfabeto rotacionado
        rotated_alphabet[ALPHABET.index(letter)] 
            for letter in plain_text
    ]

    
    return "".join(result) # retorma em formato string



for i in range(1, 26):
    
    # obs.  no exemplo da aula usava 3 para criptografar e -3 para descriptografar
    print(i, caesarCipher(CHAVE_PROF_THAIS, i))