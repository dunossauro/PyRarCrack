#!/bin/python3
#   V: 0.0.1
#   D: github.com/z4r4tu5tr4
#
#
#   Baseado em:
#   http://stackoverflow.com/questions/11747254/python-brute-force-algorithm
#   http://www.enigmagroup.org/code/view/python/168-Rar-password-cracker
#   http://rarcrack.sourceforge.net/

import itertools
from os import system, popen
from sys import argv
import time

if argv[1] == '--help' or argv[1] == '-h':
    print("""Use: %s <Numero_do_inicio> <Numero_do_final> <Arquivo.rar>\n\n\
<Numero_do_inicio> = numero do tamanho da string inicial\n\
    ex: 5 = 00000\n\n\
<Numero_do_final> = numero do tamanho da string final\n\
    ex: 10 = ßßßßßßßßßß""")
    exit()

elif len(argv) != 4:
    print("Use: %s <Numero_do_inicio> <Numero_do_final> <Arquivo.rar>" % argv[0])
    print("Para mais informações, digite %s --help" % argv[0])
    exit()

# ----- Inicio e final recebem os valores passados por argumentos
try:
    inicio = int(argv[1])
    final = int(argv[2])
except ValueError:
    print("Digite valores inteiros para a verificação")
    print("Para mais informações, digite %s --help" % argv[0])
    exit()

# ----- Verificação de um cenário possível

if final < inicio:
    print(("%s é maior que %s") % (final, inicio))
    print("Para mais informações, digite %s --help" % argv[0])
    exit()

# ----- Lista de caracteres aceitos
alfabeto = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!\"#$%&\'()*+,-./:;<=>?@[\]^_`{|}~ÁáÂâàÀÃãÅåÄäÆæÉéÊêÈèËëÐðÍíÎîÌìÏïÓóÒòÔôØøÕõÖöÚúÛûÙùÜüÇçÑñÝý®©Þþß"
caracteres_especiais = "();<>\`|~\"&\''}]"

# ----- Função que gera combinações partindo dos argumentos
def forca_bruta(charset, maxlength):
    return (''.join(candidate)
        for candidate in itertools.chain.from_iterable(itertools.product(charset, repeat=x)
        for x in range(inicio, maxlength + 1)))

# ----- Attack_list recebe a interação
attack_list = forca_bruta(alfabeto, final)

# ----- Função que formata para os caracteres aceitos pelo unrar
def formata(string):
    _string = []
    for x in string:
        if x in caracteres_especiais:
            x = (("\\%s")%(x))
        _string.append(x)
    return "".join(_string)

# ----- Laço do ataque
for attack in attack_list:
    comeco = time.time()
    print(("Tentando:\t%s")%(attack))
    attack = formata(attack)
    console = popen("unrar t -y -p%s %s 2>&1 | grep 'All OK'" % (attack, argv[3]))
    for x in console.readlines():
        if x == "All OK\n":
            print (("Senha encontrada %s")%(attack))
            print (("Levou: %s segundos")%((time.time()-comeco)))

            exit()
