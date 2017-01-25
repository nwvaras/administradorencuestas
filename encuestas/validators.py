from django.core.exceptions import ValidationError

__author__ = 'Nicolas'

from itertools import cycle


def digito_verificador(rut):
    reversed_digits = map(int, reversed(str(rut)))
    factors = cycle(range(2, 8))
    s = sum(d * f for d, f in zip(reversed_digits, factors))
    return (-s) % 11


def verificar_rut(rut):

    rutsplited = rut.split('-')
    digito_ingresado = rutsplited[1]
    print rutsplited[0]
    print rutsplited[1]
    digito = digito_verificador(rutsplited[0])
    print digito
    if digito_ingresado == 'k' or digito_ingresado == 'K':
        digito = 10
    print digito_ingresado
    print digito
    if digito != digito_ingresado:
        print "digito " + str(digito) + " ingresasado " + str(digito_ingresado)
        print "why :c"
        raise ValidationError(
            "error de rut"
        )
    else:
        return True
