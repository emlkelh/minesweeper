# sisältää metodit pelin käyttöliittymän (menun ja itse pelin) luomiseen ja käsittelyyn

import haravasto
import vakiot
import ikkunasto
import logiikka
import tallentaja


objektit = {
    "koko_valitsin": None,
    "kentän_leveys": None,
    "kentän_korkeus": None,
    "miinojen_määrä": None
}


def tee_ikkuna(tyyppi):
    if tyyppi == vakiot.TYYPPI_MENU:
        menu_ikkuna = ikkunasto.luo_ikkuna("Miinaharava")
        paakehys = ikkunasto.luo_kehys(menu_ikkuna, ikkunasto.ALA)
        ikkunasto.luo_tekstirivi(paakehys, "Miinantallaaja")
        ikkunasto.luo_vaakaerotin(paakehys, 6)
        ikkunasto.luo_nappi(paakehys, "Uusi peli", maarittele_pelin_koko)
        ikkunasto.luo_vaakaerotin(paakehys, 6)
        ikkunasto.luo_nappi(paakehys, "Tarkastele tuloksia", logiikka.katso_tulokset)
        ikkunasto.luo_vaakaerotin(paakehys, 6)
        ikkunasto.luo_nappi(paakehys, "Poistu", poistu)
        ikkunasto.luo_vaakaerotin(paakehys, 6)
        ikkunasto.kaynnista()
    elif tyyppi == vakiot.TYYPPI_TILASTOT:
        tilasto_ikkuna = ikkunasto.luo_ali_ikkuna("Tilastot")
        tilasto_kehys = ikkunasto.luo_kehys(tilasto_ikkuna, ikkunasto.YLA)
        lista_laatikko = ikkunasto.luo_listalaatikko(tilasto_kehys)
        tilastot = tallentaja.lataa(vakiot.PELIDATA)
        for tilasto in tilastot:
            paivamaara = tilasto[vakiot.PELIDATA_PVM]
            kellonaika = tilasto[vakiot.PELIDATA_KELLONAIKA]
            kesto = tilasto[vakiot.PELIDATA_KESTO]
            vuorot = tilasto[vakiot.PELIDATA_VUOROT]
            lopputulos = tilasto[vakiot.PELIDATA_TULOS]
            korkeus = tilasto[vakiot.PELIDATA_KORKEUS]
            leveys = tilasto[vakiot.PELIDATA_LEVEYS]
            miinat = tilasto[vakiot.PELIDATA_MIINAT]
            ikkunasto.lisaa_rivi_laatikkoon(lista_laatikko, "Pelattu: {} klo {}".format(paivamaara, kellonaika))
            ikkunasto.lisaa_rivi_laatikkoon(lista_laatikko, "Pelin kesto: {} minuuttia".format(kesto))
            ikkunasto.lisaa_rivi_laatikkoon(lista_laatikko, "Käytetyt vuorot: {} kpl".format(vuorot))
            ikkunasto.lisaa_rivi_laatikkoon(lista_laatikko, "Pelin lopputulos: {}".format(lopputulos))
            ikkunasto.lisaa_rivi_laatikkoon(lista_laatikko, "Pelialueen mitat: {}x{} ruutua".format(leveys, korkeus))
            ikkunasto.lisaa_rivi_laatikkoon(lista_laatikko, "Miinojen määrä: {} kpl".format(miinat))
            ikkunasto.lisaa_rivi_laatikkoon(lista_laatikko, " ")


def poistu():
    ikkunasto.lopeta()


def maarittele_pelin_koko():
    koko_valitsin = ikkunasto.luo_ali_ikkuna("Valitse pelialueen koko")
    objektit["koko_valitsin"] = koko_valitsin
    otsikko_kehys = ikkunasto.luo_kehys(koko_valitsin, ikkunasto.YLA)
    paakehys = ikkunasto.luo_kehys(koko_valitsin, ikkunasto.VASEN)
    teksti_kehys = ikkunasto.luo_kehys(paakehys, ikkunasto.VASEN)
    teksti_laatikko_kehys = ikkunasto.luo_kehys(paakehys, ikkunasto.OIKEA)
    ikkunasto.luo_tekstirivi(otsikko_kehys, "Määrittele pelialueen mitat ruutuina")
    ikkunasto.luo_tekstirivi(teksti_kehys, "Leveys:")
    objektit["kentän_leveys"] = ikkunasto.luo_tekstikentta(teksti_laatikko_kehys)
    ikkunasto.luo_tekstirivi(teksti_kehys, "Korkeus:")
    objektit["kentän_korkeus"] = ikkunasto.luo_tekstikentta(teksti_laatikko_kehys)
    ikkunasto.luo_vaakaerotin(teksti_laatikko_kehys, 4)
    ikkunasto.luo_tekstirivi(teksti_laatikko_kehys, "Valitse miinojen määrä")
    objektit["miinojen_määrä"] = ikkunasto.luo_tekstikentta(teksti_laatikko_kehys)
    ikkunasto.luo_vaakaerotin(teksti_laatikko_kehys, 8)
    ikkunasto.luo_nappi(teksti_laatikko_kehys, "Aloita peli", aloita)
    ikkunasto.luo_vaakaerotin(teksti_laatikko_kehys, 2)
    ikkunasto.luo_nappi(teksti_laatikko_kehys, "Peruuta", peruuta_peli)
    ikkunasto.luo_vaakaerotin(teksti_laatikko_kehys, 2)
    ikkunasto.nayta_ali_ikkuna(koko_valitsin)


def aloita():
    try:
        leveys_syote = int(ikkunasto.lue_kentan_sisalto(objektit["kentän_leveys"]))
        korkeus_syote = int(ikkunasto.lue_kentan_sisalto(objektit["kentän_korkeus"]))
        miina_syote = int(ikkunasto.lue_kentan_sisalto(objektit["miinojen_määrä"]))
    except ValueError:
        ikkunasto.avaa_viesti_ikkuna("Vääriä lukuja", "Sinun tulee antaa pelkästään kokonaislukuja", True)
        ikkunasto.tyhjaa_kentan_sisalto(objektit["kentän_leveys"])
        ikkunasto.tyhjaa_kentan_sisalto(objektit["kentän_korkeus"])
        ikkunasto.tyhjaa_kentan_sisalto(objektit["miinojen_määrä"])
    else:
        if miina_syote > korkeus_syote * leveys_syote:
            ikkunasto.avaa_viesti_ikkuna("Vääriä lukuja", "Miinoja ei voi olla enemmän kuin ruutuja", True)
        else:
            ikkunasto.piilota_ali_ikkuna(objektit["koko_valitsin"])
            aloita_peli(leveys_syote, korkeus_syote, miina_syote)


def peruuta_peli():
    ikkunasto.piilota_ali_ikkuna(objektit["koko_valitsin"])


def aloita_peli(leveys, korkeus, miinat):
    ikkunasto.lopeta()
    rakenna_peli_alue(leveys, korkeus, miinat)


def rakenna_peli_alue(leveys, korkeus, miinat):
    logiikka.luo_kentta(leveys, korkeus, miinat)
    haravasto.luo_ikkuna(leveys * 40, korkeus * 40)
    haravasto.aseta_hiiri_kasittelija(logiikka.ruutu_valittu)
    haravasto.aseta_piirto_kasittelija(piirra_peli_alue)
    haravasto.lataa_kuvat("spritet")
    logiikka.aloita_laskuri()
    haravasto.aloita()


def piirra_peli_alue():
    haravasto.tyhjaa_ikkuna()
    haravasto.piirra_tausta()
    haravasto.aloita_ruutujen_piirto()
    for y, x_lista in enumerate(logiikka.anna_kentta()):
        for x, merkki in enumerate(x_lista):
            haravasto.lisaa_piirrettava_ruutu(merkki, x * 40, y * 40)
    haravasto.piirra_ruudut()


def lopeta_peli(syy):
    teksti = ""
    if syy == vakiot.SYY_KAIKKI_RUUDUT_AUKI:
        teksti = "Voitit pelin, hienoa!"
    else:
        teksti = "Tallasit miinan! Parempi onni ensi kerralla."
    haravasto.lopeta()
    peli_loppu = ikkunasto.luo_ikkuna("Peli loppui")
    kehys = ikkunasto.luo_kehys(peli_loppu, ikkunasto.ALA)
    ikkunasto.luo_tekstirivi(kehys, teksti)
    ikkunasto.luo_nappi(kehys, "Ok", logiikka.aloita_alusta)
    ikkunasto.kaynnista()


def mene_menuun():
    ikkunasto.lopeta()
    tee_ikkuna(vakiot.TYYPPI_MENU)
