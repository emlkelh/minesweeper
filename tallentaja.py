import json
import vakiot


# Data tallennetaan JSON-tiedostoon listana, joka sisältää
# jokaista pelikertaa varten oman sanakirjansa


def tallenna_data(pvm, kello, kesto, vuorot, lopputulos, leveys, korkeus, miinat):
    data_objekti = {
        vakiot.PELIDATA_PVM: pvm,
        vakiot.PELIDATA_KELLONAIKA: kello,
        vakiot.PELIDATA_KESTO: kesto,
        vakiot.PELIDATA_VUOROT: vuorot,
        vakiot.PELIDATA_TULOS: lopputulos,
        vakiot.PELIDATA_LEVEYS: leveys,
        vakiot.PELIDATA_KORKEUS: korkeus,
        vakiot.PELIDATA_MIINAT: miinat
    }
    lisaa_tietoja(data_objekti)


# lisää tiedot datatiedostoon
def lisaa_tietoja(kohde):
    data = lataa(vakiot.PELIDATA)
    data.append(kohde)
    tallenna(vakiot.PELIDATA, data)


# lukee koko datatiedoston
def lataa(tiedosto):
    try:
        with open(tiedosto, "r") as datatiedosto:
            tulos = json.load(datatiedosto)
    except IOError:
        # Datatiedostoa ei löytynyt, tehdään sellainen
        with open(tiedosto, "x") as d:
            tulos = []
    return tulos


def tallenna(tiedosto, kohde):
    with open(tiedosto, "w") as datatiedosto:
        json.dump(kohde, datatiedosto)
