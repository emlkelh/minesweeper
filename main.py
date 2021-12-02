# Tämän moduulin tehtävänä on huolehtia pelin muiden moduulien yhteistyöstä


import kayttoliittyma
import vakiot


def aloita_menu():
    kayttoliittyma.tee_ikkuna(vakiot.TYYPPI_MENU)


if __name__ == '__main__':
    aloita_menu()
