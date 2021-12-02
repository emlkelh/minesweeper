# sisältää pelin ja menun logiikan


import haravasto
import random
import vakiot
import kayttoliittyma
import time
import tallentaja


tila = {
    "maxKorkeus": 0,
    "maxLeveys": 0,
    "miinojen_määrä": 0,
    "kenttä": [],
    "merkityt_ruudut": [],
    "miinat": [],
    "aloitus_aika": 0.0,
    "vuorot": 0
}


def katso_tulokset():
    kayttoliittyma.tee_ikkuna(vakiot.TYYPPI_TILASTOT)


def anna_kentta():
    return tila["kenttä"]


def luo_kentta(leveys, korkeus, miinojen_maara):
    xlista = []
    tila[vakiot.MAX_LEVEYS] = leveys - 1
    tila[vakiot.MAX_KORKEUS] = korkeus - 1
    tila["miinojen_määrä"] = miinojen_maara
    # luodaan lista miinojen sijainneista
    sijoita_miinat(leveys, korkeus, miinojen_maara)
    # luodaan kenttä
    for r1 in range(leveys):
        xlista.append(" ")
    for r2 in range(korkeus):
        tila["kenttä"].append(xlista.copy())


def sijoita_miinat(leveys, korkeus, miinat):
    for i in range(miinat):
        satunnainen_x = random.randint(0, leveys - 1)
        satunnainen_y = random.randint(0, korkeus - 1)
        tila["miinat"].append((satunnainen_x, satunnainen_y))


# hiirikäsittelijä
def ruutu_valittu(x, y, nappi, muokkaus):
    valittu_x, valittu_y = maarita_ruutu(x, y)
    if nappi == haravasto.HIIRI_VASEN:
        avaa_ruutu(valittu_x, valittu_y)
    elif nappi == haravasto.HIIRI_OIKEA:
        merkitse_ruutu(valittu_x, valittu_y)


# avaa annetun ruudun muistissa olevasta pelikentän mallista, tarkistaa onko ruudussa miina
def avaa_ruutu(x, y):
    tila["vuorot"] += 1
    if (x, y) in tila["miinat"]:
        if not (x, y) in tila["merkityt_ruudut"]:
            paata_peli(vakiot.SYY_MIINA_TALLATTU)
    elif tila["kenttä"][y][x] == " ":
        avaa_viereiset_ruudut(x, y)


def merkitse_ruutu(x, y):
    if not tila["kenttä"][y][x] == "0":
        if (x, y) in tila["merkityt_ruudut"]:
            tila["merkityt_ruudut"].remove((x, y))
            tila["kenttä"][y][x] = " "
        else:
            tila["merkityt_ruudut"].append((x, y))
            tila["kenttä"][y][x] = "f"
            onko_kaikki_merkitty()


# tutki, mitä ruutua painettiin ja palauta sen koordinaatit muistissa olevassa pelikentän mallissa
def maarita_ruutu(x_koord, y_koord):
    x_ruuduissa = x_koord / 40
    y_ruuduissa = y_koord / 40
    for y, x_lista in enumerate(tila["kenttä"]):
        for x, merkki in enumerate(x_lista):
            if x <= x_ruuduissa <= x + 1 and y <= y_ruuduissa <= y + 1:
                return x, y


# pelaaja valitsi miinallisen ruudun tai kaikki miinattomat ruudut aukaistu
def paata_peli(syy):
    tallenna_tiedot(syy)
    tila["kenttä"].clear()
    tila["miinat"].clear()
    kayttoliittyma.lopeta_peli(syy)


def tallenna_tiedot(syy):
    minuutit = laske_peliaika()
    ajankohta = time.localtime()
    aika_tunnit = ajankohta[3]
    aika_minuutit = ajankohta[4]
    aika_vuosi = ajankohta[0]
    aika_kuukausi = ajankohta[1]
    aika_paiva = ajankohta[2]
    pvm = "{}.{}.{}".format(aika_paiva, aika_kuukausi, aika_vuosi)
    kellonaika = "{}.{}".format(aika_tunnit, aika_minuutit)
    tallentaja.tallenna_data(pvm, kellonaika, minuutit,
                             tila["vuorot"], syy, tila["maxLeveys"],
                             tila["maxKorkeus"], tila["miinojen_määrä"])


# miinaton ruutu klikattu, avataan kaikki viereiset ruudut joissa ei miinaa
def avaa_viereiset_ruudut(aloitus_x, aloitus_y):
    turvalliset = [(aloitus_x, aloitus_y)]
    while True:
        if len(turvalliset) > 0:
            (x, y) = turvalliset[-1]
            viereiset = laske_viereiset_miinat(x, y)
            if viereiset > 0:
                tila["kenttä"][y][x] = str(viereiset)
                turvalliset.pop()
            else:
                tila["kenttä"][y][x] = "0"
                turvalliset.pop()
                # vasen
                if voiko_avata(vakiot.SIJAINTI_VASEN, x, y):
                    turvalliset.append((x - 1, y))
                # oikea
                if voiko_avata(vakiot.SIJAINTI_OIKEA, x, y):
                    turvalliset.append((x + 1, y))
                # alapuoli
                if voiko_avata(vakiot.SIJAINTI_ALA, x, y):
                    turvalliset.append((x, y - 1))
                # yläpuoli
                if voiko_avata(vakiot.SIJAINTI_YLA, x, y):
                    turvalliset.append((x, y + 1))
                # vasen yläkulma
                if voiko_avata(vakiot.SIJAINTI_VASEN_YLA, x, y):
                    turvalliset.append((x - 1, y + 1))
                # oikea yläkulma
                if voiko_avata(vakiot.SIJAINTI_OIKEA_YLA, x, y):
                    turvalliset.append((x + 1, y + 1))
                # vasen alakulma
                if voiko_avata(vakiot.SIJAINTI_VASEN_ALA, x, y):
                    turvalliset.append((x - 1, y - 1))
                # oikea alakulma
                if voiko_avata(vakiot.SIJAINTI_OIKEA_ALA, x, y):
                    turvalliset.append((x + 1, y - 1))
        else:
            break


def laske_viereiset_miinat(x, y):
    viereiset = 0
    # vasen
    if (x - 1, y) in tila["miinat"]:
        viereiset += 1
    # oikea
    if (x + 1, y) in tila["miinat"]:
        viereiset += 1
    # alapuoli
    if (x, y - 1) in tila["miinat"]:
        viereiset += 1
    # vasen yläkulma
    if (x - 1, y + 1) in tila["miinat"]:
        viereiset += 1
    # oikea yläkulma
    if (x + 1, y + 1) in tila["miinat"]:
        viereiset += 1
    # yläpuoli
    if (x, y + 1) in tila["miinat"]:
        viereiset += 1
    # vasen alakulma
    if (x - 1, y - 1) in tila["miinat"]:
        viereiset += 1
    # oikea alakulma
    if (x + 1, y - 1) in tila["miinat"]:
        viereiset += 1
    return viereiset


def voiko_avata(sijainti, x, y):
    leveys = tila[vakiot.MAX_LEVEYS]
    korkeus = tila[vakiot.MAX_KORKEUS]
    if sijainti == vakiot.SIJAINTI_YLA:
        if y + 1 <= tila[vakiot.MAX_KORKEUS]:
            if tila["kenttä"][y + 1][x] == " " and not (x, y + 1) in tila["miinat"]:
                return True
        return False
    elif sijainti == vakiot.SIJAINTI_ALA:
        if y - 1 >= 0:
            if tila["kenttä"][y - 1][x] == " " and not (x, y - 1) in tila["miinat"]:
                return True
        return False
    elif sijainti == vakiot.SIJAINTI_VASEN:
        if x - 1 >= 0:
            if tila["kenttä"][y][x - 1] == " " and not (x - 1, y) in tila["miinat"]:
                return True
        return False
    elif sijainti == vakiot.SIJAINTI_OIKEA:
        if x + 1 <= tila[vakiot.MAX_LEVEYS]:
            if tila["kenttä"][y][x + 1] == " " and not (x + 1, y) in tila["miinat"]:
                return True
        return False
    elif sijainti == vakiot.SIJAINTI_VASEN_ALA:
        if y - 1 >= 0 and x - 1 >= 0:
            if tila["kenttä"][y - 1][x - 1] == " " and not (x - 1, y - 1) in tila["miinat"]:
                return True
        return False
    elif sijainti == vakiot.SIJAINTI_VASEN_YLA:
        if y + 1 <= tila[vakiot.MAX_KORKEUS] and x - 1 >= 0:
            if tila["kenttä"][y + 1][x - 1] == " " and not (x - 1, y + 1) in tila["miinat"]:
                return True
        return False
    elif sijainti == vakiot.SIJAINTI_OIKEA_ALA:
        if y - 1 >= 0 and x + 1 <= tila[vakiot.MAX_LEVEYS]:
            if tila["kenttä"][y - 1][x + 1] == " " and not (x + 1, y - 1) in tila["miinat"]:
                return True
        return False
    elif sijainti == vakiot.SIJAINTI_OIKEA_YLA:
        if y + 1 <= tila[vakiot.MAX_KORKEUS] and x + 1 <= tila[vakiot.MAX_LEVEYS]:
            if tila["kenttä"][y + 1][x + 1] == " " and not (x + 1, y + 1) in tila["miinat"]:
                return True
        return False
    return False


def tarkista_koordinaatit(x, y):
    if 0 <= x <= tila[vakiot.MAX_LEVEYS] and 0 <= y <= tila[vakiot.MAX_KORKEUS]:
        return True
    else:
        return False


def aloita_alusta():
    kayttoliittyma.mene_menuun()


def onko_kaikki_merkitty():
    merkityt = 0
    for x, y in tila["miinat"]:
        if (x, y) in tila["merkityt_ruudut"]:
            merkityt += 1
    if merkityt == tila["miinojen_määrä"]:
        paata_peli(vakiot.SYY_KAIKKI_RUUDUT_AUKI)


def aloita_laskuri():
    tila["aloitus_aika"] = time.time()


def laske_peliaika():
    aloitus_aika = tila["aloitus_aika"]
    kulunut_aika = time.time() - aloitus_aika
    return int(kulunut_aika / 60)
