'''
V: 0.0.2.2

Baseado em:
http://stackoverflow.com/questions/11747254/python-brute-force-algorithm
http://www.enigmagroup.org/code/view/python/168-Rar-password-cracker
http://rarcrack.sourceforge.net/
'''

from itertools import chain, product
from os import popen
from sys import argv
import time

if argv[1] == '--help' or argv[1] == '-h':
    print('''Use: {} <Numero_do_inicio> <Numero_do_final> <Arquivo.rar>\n\n\
<Numero_do_inicio> = numero do tamanho da string inicial\n\
    ex: 5 = 00000\n\n\
<Numero_do_final> = numero do tamanho da string final\n\
    ex: 10 = ßßßßßßßßßß'''.format(argv[0]))
    exit()

elif len(argv) != 4:
    print('Use: {} <Numero_do_inicio> <Numero_do_final> <Arquivo.rar>'.format(
          argv[0]))

    print('Para mais informações, digite {} --help'.format(argv[0]))

    exit()

# ----- Inicio e final recebem os valores passados por argumentos
try:
    inicio = int(argv[1])
    final = int(argv[2])
except ValueError:
    print('Digite valores inteiros para a verificação')
    print('Para mais informações, digite {} --help'.format(argv[0]))
    exit()

# ----- Verificação de um cenário possível
if final < inicio:
    print('{} é maior que {}'.format(final, inicio))
    print('Para mais informações, digite %s --help'.format(argv[0]))
    exit()

# ----- Lista de caracteres aceitos
alfabeto = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!\
            \"#$%&\'()*+,-./:;<=>?@[\]^_`{|}~ÁáÂâàÀÃãÅåÄäÆæÉéÊêÈèËëÐðÍíÎîÌì\
            ÏïÓóÒòÔôØøÕõÖöÚúÛûÙùÜüÇçÑñÝý®©Þþß'

caracteres_especiais = "();<>\`|~\"&\'}]"


def forca_bruta(string, tamanho):
    """
    Gera combinações partindo dos argumentos.
    """
    return (''.join(candidato)
            for candidato in chain.from_iterable(product(string, repeat=x)
            for x in range(inicio, tamanho + 1)))


# Attack_list recebe a interação
attack_list = forca_bruta(alfabeto, final)


def formata(string):
    """
    Formata para os caracteres aceitos pelo unrar.
    """
    _string = []
    for x in string:
        if x in caracteres_especiais:
            x = (("\\%s") % (x))
        _string.append(x)
    return "".join(_string)


# ----- Laço do ataque
for attack in attack_list:
    comeco = time.time()
    print('Tentando:\t%s'.format(attack))
    attack = formata(attack)
    console = popen("unrar t -y -p{} {} 2>&1 | grep 'All OK'".format(attack,
                                                                     argv[3]))
    for x in console.readlines():
        if x == 'All OK\n':
            print("Senha encontrada {}".format(attack))
            print("Levou: {} segundos".format(time.time()-comeco))

            exit()
