"""Funções para normalização e limpeza de texto e listas de textos.

"""
import unicodedata


def ascii_sanitizar(text):
    """Remove marcas de diacríticos (acentos e caracteres especiais)
    Retorna NFC normalizado ASCII
    """
    return unicodedata.normalize('NFKD', text) \
        .encode('ASCII', 'ignore') \
        .decode('ASCII')


def unicode_sanitizar(text):
    """Remove marcas de diacríticos (acentos e caracteres especiais)
    Retorna NFC normalizado
    """
    norm_txt = unicodedata.normalize('NFD', text)
    shaved = ''.join(char for char in norm_txt
                     if not unicodedata.combining(char))
    return unicodedata.normalize('NFC', shaved)


def sanitizar(text, norm_function=unicode_sanitizar):
    """Remove espaços à direita e esquerda, passa para "casefold"(caixa baixa),
    usa função normalização para retirar marcas de diacríticos (acentos e
     caracteres especiais), remove espaços adicionais entre palavras.
    Retorna texto sanitizado e normalizado
    Depois desse produto, suas buscas nunca mais serão as mesmas!!! :-p
    """
    if text is None or text == '':
        return text
    text = text.strip()
    text = text.casefold()
    text = norm_function(text)
    word_list = text.split()
    text = ' '.join(word.strip() for word in word_list
                    if len(word.strip()))
    return text


def sanitizar_lista(lista, norm_function=unicode_sanitizar):
    """Percorre lista de listas sanitizando inline
    Por ora só suporta lista 'bidimensional', como um csv"""
    for row in range(len(lista)):
        for col in range(len(lista[row])):
            lista[row][col] = sanitizar(lista[row][col], norm_function)
    return lista
