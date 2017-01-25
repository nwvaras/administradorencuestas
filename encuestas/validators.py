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
    if digito == 10:
        digito = 'k'
    if digito != digito_ingresado:
        raise ValidationError(
            "error de rut"
        )
