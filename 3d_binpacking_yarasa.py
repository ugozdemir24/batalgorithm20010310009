import random
import matplotlib.pyplot as plt
import time
import os
import math
import csv
from copy import deepcopy
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# =====================================================
# =====================================================

koliler_tipi = {
    "K-01": [3, 3, 4, 36],
    "K-02": [4, 3, 3, 36],
    "K-03": [5, 4, 4, 80],
    "K-04": [6, 4, 5, 120],
    "K-05": [8, 5, 6, 240],
    "K-06": [7, 6, 6, 252],
    "K-07": [10, 3, 4, 120],
    "K-08": [12, 3, 3, 108],
    "K-09": [5, 5, 8, 200],
    "K-10": [6, 4, 8, 192],
    "K-11": [5, 5, 5, 125],
    "K-12": [3, 4, 3, 36],
    "K-13": [9, 5, 7, 315],
    "K-14": [6, 5, 4, 120],
    "K-15": [11, 3, 4, 132]
}



araclar = {
    "A-01": [15, 10, 8, 1200],
    "A-02": [25, 15, 12, 4500],
    "A-03": [40, 20, 18, 14400],
    "A-04": [60, 25, 24, 36000]
}

# =====================================================
def veri_al():
    """Kullanicidan koli adetlerini alir ve algoritmada kullanilacak koli listesini olusturur."""
    tum_koliler = []
    print("\nKoli adetlerini girin\n")

    for k in koliler_tipi:
        adet = int(input(f"{k} kac tane: "))

        for _ in range(adet):
            bilgi = koliler_tipi[k]
            tum_koliler.append({
                "id": k,
                "d": bilgi[0],
                "y": bilgi[1],
                "g": bilgi[2],
                "h": bilgi[3]
            })

    return tum_koliler




def rotate(koli):
    """Bir kolinin boyutlarini rastgele cevirerek farkli 3D oryantasyonlar denenmesini saglar."""
    yeni = deepcopy(koli)
    boyutlar = [yeni["d"], yeni["y"], yeni["g"]]
    random.shuffle(boyutlar)
    yeni["d"] = boyutlar[0]
    yeni["y"] = boyutlar[1]
    yeni["g"] = boyutlar[2]
    return yeni

# =====================================================
def arac_uygun_mu(koli, arac_tipi):
    """Bir kolinin verilen arac tipine boyut olarak sigip sigmadigini kontrol eder."""
    D = araclar[arac_tipi][0]
    Y = araclar[arac_tipi][1]
    G = araclar[arac_tipi][2]
    return koli["d"] <= D and koli["y"] <= Y and koli["g"] <= G

# =====================================================
def uygun_araclar(koli):
    """Bir koli icin boyut sinirlarini saglayan arac tiplerini listeler."""
    uygun = []

    for a in araclar:
        if arac_uygun_mu(koli, a):
            uygun.append(a)

    return uygun

# =====================================================
def en_kucuk_uygun_arac(koli):
    """Koliye sigabilecek en kucuk kapasiteli araci secer ve bos hacmi azaltmaya yardim eder."""
    uygunlar = uygun_araclar(koli)

    if len(uygunlar) == 0:
        return random.choice(list(araclar.keys()))

    return min(uygunlar, key=lambda a: araclar[a][3])

# =====================================================
def yuksek_doluluk_arac_adaylari(koli):
    """Koli icin yuksek doluluk hedefleyen uygun buyuk arac adaylarini uretir."""
    uygunlar = uygun_araclar(koli)
    buyukler = [a for a in uygunlar if a in ["A-03", "A-04"]]

    if len(buyukler) > 0:
        return buyukler

    return uygunlar

# ================================================
def random_cozum(koliler, baslangic=False):
    """Baslangic veya kesif icin koli sirasi, oryantasyon ve arac tercihi iceren rastgele cozum uretir."""
    yeni_liste = deepcopy(koliler)
    random.shuffle(yeni_liste)
    cozum = []



    for koli in yeni_liste:
        yeni = deepcopy(koli)

        if random.random() < 0.6:
            yeni = rotate(yeni)

        uygunlar = yuksek_doluluk_arac_adaylari(yeni)

        if baslangic:
            if random.random() < 0.70:
                secilen = random.choice(uygunlar) if len(uygunlar) > 0 else random.choice(list(araclar.keys()))
            elif len(uygunlar) > 0:
                secilen = random.choice(uygunlar)
            else:
                secilen = random.choice(list(araclar.keys()))
        elif len(uygunlar) > 0:
            if random.random() < 0.65:
                secilen = random.choice(uygunlar)
            else:
                secilen = min(uygunlar, key=lambda a: araclar[a][3])
        else:
            secilen = random.choice(list(araclar.keys()))

        cozum.append({
            "koli": yeni,
            "arac": secilen
        })

    return cozum







# =====================================================
def hizli_araclara_dagit(cozum):
    """Koordinat hesaplamadan hacim ve arac uygunluguna gore hizli bir dagitim yapar."""
    arac_listesi = []
    ceza = 0
    sirali_cozum = sorted(
        cozum,




        key=lambda x: (
            max(x["koli"]["d"], x["koli"]["y"], x["koli"]["g"]),
            x["koli"]["h"]
        ),
        reverse=True
    )

    for item in sirali_cozum:
        koli = item["koli"]
        tip = item["arac"]

        if not arac_uygun_mu(koli, tip):
            ceza += 50000
            tip = en_kucuk_uygun_arac(koli)



        en_iyi_indeks = None
        en_iyi_kalan = None

        for indeks, arac in enumerate(arac_listesi):
            if arac_uygun_mu(koli, arac["tip"]) and koli["h"] <= arac["kalan"]:
                kalan_sonra = arac["kalan"] - koli["h"]

                if en_iyi_kalan is None or kalan_sonra < en_iyi_kalan:
                    en_iyi_kalan = kalan_sonra
                    en_iyi_indeks = indeks

        if en_iyi_indeks is not None:
            arac_listesi[en_iyi_indeks]["kalan"] -= koli["h"]
            arac_listesi[en_iyi_indeks]["kullanilan"] += koli["h"]
        else:
            kapasite = araclar[tip][3]
            arac_listesi.append({
                "tip": tip,
                "kalan": kapasite - koli["h"],
                "kullanilan": koli["h"],
                "kapasite": kapasite
            })

    return arac_listesi, ceza

# =====================================================
def hizli_fitness(cozum):
    """Cozumu arac sayisi, bos hacim, doluluk dengesi ve cezalara gore hizli sekilde puanlar."""
    arac_listesi, ceza = planli_hacim_dagit(cozum)
    toplam_bos = 0
    doluluklar = []
    buyuk_arac_dusuk_doluluk_cezasi = 0
    yuksek_doluluk_odulu = 0
    arac_tipi_cezasi = 0

    for a in arac_listesi:

        toplam_bos += a["kalan"]
        doluluk = a["kullanilan"] / a["kapasite"]
        doluluklar.append(doluluk)

        if doluluk < 0.85:
            buyuk_arac_dusuk_doluluk_cezasi += (0.85 - doluluk) * a["kapasite"] * 160





        if a["tip"] == "A-04" and doluluk < 0.70:
            buyuk_arac_dusuk_doluluk_cezasi += (0.70 - doluluk) * a["kapasite"] * 220

        if a["tip"] == "A-03" and doluluk < 0.65:
            buyuk_arac_dusuk_doluluk_cezasi += (0.65 - doluluk) * a["kapasite"] * 180

        if a["tip"] == "A-04" and doluluk < 0.80:
            arac_tipi_cezasi += (0.80 - doluluk) * a["kapasite"] * 150

        if a["tip"] == "A-03" and doluluk < 0.75:
            arac_tipi_cezasi += (0.75 - doluluk) * a["kapasite"] * 130

        if a["tip"] in ["A-03", "A-04"] and doluluk < 0.96:
            arac_tipi_cezasi += (0.96 - doluluk) * a["kapasite"] * 30


        if a["tip"] in ["A-01", "A-02"] and doluluk >= 0.94:
            yuksek_doluluk_odulu += doluluk * 3200

        if doluluk >= 0.96:
            yuksek_doluluk_odulu += doluluk * 2400

        if doluluk >= 0.99:
            yuksek_doluluk_odulu += 1600

    doluluk_cezasi = 0

    dusuk_doluluk_cezasi = 0
    denge_cezasi = 0
    ilk_arac_cezasi = 0
    hedef_doluluk_cezasi = 0

    for d in doluluklar:
        if d < 0.70:
            doluluk_cezasi += (0.70 - d) * 9000

        if d < 0.90:
            dusuk_doluluk_cezasi += (0.90 - d) * 18000

    if len(doluluklar) > 0:
        ortalama_doluluk = sum(doluluklar) / len(doluluklar)

        for d in doluluklar:
            denge_cezasi += abs(d - ortalama_doluluk) * 65000

        sirali_doluluklar = sorted(doluluklar, reverse=True)

        hedeflenen_arac_sayisi = max(1, int(math.ceil(len(sirali_doluluklar) * 0.75)))

        for sira, d in enumerate(sirali_doluluklar[:hedeflenen_arac_sayisi]):
            hedef = 0.98 if sira < max(1, hedeflenen_arac_sayisi - 1) else 0.94

            if d < hedef:

                ilk_arac_cezasi += (hedef - d) * 90000

        for d in sirali_doluluklar[hedeflenen_arac_sayisi:]:
            if d < 0.68:
                hedef_doluluk_cezasi += (0.68 - d) * 18000

        if ortalama_doluluk < 0.85:
            dusuk_doluluk_cezasi += (0.85 - ortalama_doluluk) * 3000000

    arac_sayisi = len(arac_listesi)
    sira_cezasi = 0

    for indeks, item in enumerate(cozum):
        uygun_indeks = list(araclar.keys()).index(item["arac"]) if item["arac"] in araclar else 0
        sira_cezasi += ((indeks + 1) * (item["koli"]["h"] + uygun_indeks * 17)) % 97

    sira_cezasi = (sira_cezasi % 1000) * 12

    skor = (
            arac_sayisi * 1000000 +
            toplam_bos * 10 +
            ceza +
            buyuk_arac_dusuk_doluluk_cezasi +
            arac_tipi_cezasi +
            doluluk_cezasi +
            dusuk_doluluk_cezasi +
            denge_cezasi +
            ilk_arac_cezasi +
            hedef_doluluk_cezasi -
            yuksek_doluluk_odulu +
            sira_cezasi
    )




    fitness =  skor/100000
    return fitness

# ================================================
def hizli_3d_decode(cozum):
    """Aday cozumu daha hizli bir 3D yerlestirme denemesiyle araclara ve koordinatlara donusturur."""
    toplam_hacim = sum(item["koli"]["h"] for item in cozum)
    plan = arac_plani_uret(toplam_hacim)
    araclar_detay = [arac_detay_katman_olustur(tip) for tip in plan]
    ceza = 0
    sirali_cozum = cozum_sirasi_uret(cozum, "hacim")

    for item in sirali_cozum:
        koli = item["koli"]
        tercih = item["arac"]
        yerlesti = False
        aday_sirasi = sorted(
            range(len(araclar_detay)),
            key=lambda i: (
                0 if araclar_detay[i]["tip"] == tercih else 1,
                araclar_detay[i]["kalan"],
                -araclar_detay[i]["kapasite"]
            )
        )

        for indeks in aday_sirasi:
            arac = araclar_detay[indeks]

            if not arac_uygun_mu(koli, arac["tip"]) or koli["h"] > arac["kalan"]:
                continue

            if maxrects_koli_yerlestir(arac, koli):
                yerlesti = True
                break

        if not yerlesti:
            tip = yeni_arac_tipi_sec(koli, 0, tercih)
            yeni_arac = arac_detay_katman_olustur(tip)

            if maxrects_koli_yerlestir(yeni_arac, koli):
                araclar_detay.append(yeni_arac)
                ceza += 750000
            else:
                ceza += 2000000




    araclar_detay = [a for a in araclar_detay if len(a["koliler"]) > 0]

    for arac in araclar_detay:
        if "katmanlar" in arac:
            del arac["katmanlar"]
        if "adaylar" in arac:
            del arac["adaylar"]
        if "dolu_hucreler" in arac:
            del arac["dolu_hucreler"]

    return araclar_detay, ceza

# =====================================================
def gercek_3d_fitness(cozum):
    """Cozumu gercek 3D yerlestirme ile degerlendirir ve cakisma/sinir risklerini fitnessa yansitir."""
    araclar_detay, yerlesim_cezasi = hizli_3d_decode(cozum)

    if len(araclar_detay) == 0:
        return 10**9, araclar_detay, 10**9

    toplam_kapasite = sum(a["kapasite"] for a in araclar_detay)
    toplam_kullanilan = sum(a["kapasite"] - a["kalan"] for a in araclar_detay)
    toplam_bos = toplam_kapasite - toplam_kullanilan
    ortalama_doluluk = toplam_kullanilan / toplam_kapasite if toplam_kapasite > 0 else 0
    doluluk_cezasi = 0
    denge_cezasi = 0
    sikilik_cezasi = 0
    yuksek_doluluk_odulu = 0
    doluluklar = []

    if ortalama_doluluk < 0.85:
        doluluk_cezasi += (0.85 - ortalama_doluluk) * 4000000

    for arac in araclar_detay:
        kullanilan = arac["kapasite"] - arac["kalan"]
        doluluk = kullanilan / arac["kapasite"]
        doluluklar.append(doluluk)

        if doluluk < 0.65:
            doluluk_cezasi += (0.65 - doluluk) * arac["kapasite"] * 180

        if doluluk < 0.85:
            doluluk_cezasi += (0.85 - doluluk) * arac["kapasite"] * 240

        if doluluk > 0.90:
            yuksek_doluluk_odulu += (doluluk - 0.90) * 90000

        if len(arac["koliler"]) > 0:
            tip = arac["tip"]
            max_x = max(k["px"] + k["d"] for k in arac["koliler"])
            max_y = max(k["py"] + k["y"] for k in arac["koliler"])
            max_z = max(k["pz"] + k["g"] for k in arac["koliler"])
            yayilim_orani = (
                max_x / araclar[tip][0] +
                max_y / araclar[tip][1] +
                max_z / araclar[tip][2]
            ) / 3
            kutu_hacmi = max(1, max_x * max_y * max_z)
            kutu_sikilik = min(1, kullanilan / kutu_hacmi)
            sikilik_cezasi += yayilim_orani * 18000
            sikilik_cezasi += (1 - kutu_sikilik) * 26000

    for d in doluluklar:
        denge_cezasi += abs(d - ortalama_doluluk) * 300000

    skor = (
        len(araclar_detay) * 1000000 +
        toplam_bos * 25 +
        doluluk_cezasi +
        denge_cezasi +
        sikilik_cezasi +
        yerlesim_cezasi -
        yuksek_doluluk_odulu
    ) / 100000

    return skor, araclar_detay, yerlesim_cezasi






# =====================================================
def final_3d_fitness(cozum):
    """Final adayini gercek 3D yerlestirme, doluluk ve arac sayisi uzerinden son kez puanlar."""
    araclar_detay, yerlesim_cezasi = cozumden_arac_detay_uret(cozum)

    if len(araclar_detay) == 0:
        return 10**9, araclar_detay, 10**9

    toplam_kapasite = sum(a["kapasite"] for a in araclar_detay)
    toplam_kullanilan = sum(a["kapasite"] - a["kalan"] for a in araclar_detay)
    toplam_bos = toplam_kapasite - toplam_kullanilan
    ortalama_doluluk = toplam_kullanilan / toplam_kapasite if toplam_kapasite > 0 else 0
    doluluk_cezasi = 0
    denge_cezasi = 0
    doluluklar = []

    if ortalama_doluluk < 0.75:
        doluluk_cezasi += (0.75 - ortalama_doluluk) * 9000000

    for arac in araclar_detay:
        kullanilan = arac["kapasite"] - arac["kalan"]
        doluluk = kullanilan / arac["kapasite"]
        doluluklar.append(doluluk)

        if doluluk < 0.75:
            doluluk_cezasi += (0.75 - doluluk) * arac["kapasite"] * 260

        if doluluk < 0.50:
            doluluk_cezasi += (0.50 - doluluk) * arac["kapasite"] * 500

    if len(doluluklar) > 0:
        ort = sum(doluluklar) / len(doluluklar)
        for doluluk in doluluklar:
            denge_cezasi += abs(doluluk - ort) * 250000

    skor = (
        len(araclar_detay) * 1000000 +
        toplam_bos * 35 +
        doluluk_cezasi +
        denge_cezasi +
        yerlesim_cezasi
    ) / 100000

    return skor, araclar_detay, yerlesim_cezasi



# =================================
def fitness(cozum):
    """Eski cagri uyumlulugu icin hizli fitness hesabini tek noktadan dondurur."""
    return hizli_fitness(cozum)

# =====================================================
def fazli_fitness(cozum, faz_no=1, gercek_3d=False, faz_ilerleme=0.0):
    """Faza gore hizli veya gercek 3D fitness hesaplar ve guven cezasini uygular."""
    if gercek_3d:
        skor, decoded, decoded_ceza = gercek_3d_fitness(cozum)
        return skor, "gercek3d", decoded, decoded_ceza

    hizli_skor = hizli_fitness(cozum)
    faz_ilerleme = max(0.0, min(1.0, faz_ilerleme))

    if faz_no == 1:
        guven_carpani = 1.50 - 0.35 * faz_ilerleme
    elif faz_no == 2:
        guven_carpani = 1.22 - 0.17 * faz_ilerleme
    else:
        guven_carpani = 1.08 - 0.08 * faz_ilerleme

    return hizli_skor * guven_carpani, "hizli+guven", None, 0

# =====================================================
def faz_bilgisi(iterasyon_indeksi, toplam_iterasyon, hedef_yarasa_sayisi):
    """Iterasyonun hangi fazda oldugunu, kesif/odak oranlarini ve faz ilerlemesini hesaplar."""
    birinci_sinir = max(1, int(math.ceil(toplam_iterasyon * 0.60)))
    ikinci_sinir = max(birinci_sinir + 1, int(math.ceil(toplam_iterasyon * 0.80)))
    ikinci_sinir = min(toplam_iterasyon, ikinci_sinir)

    if iterasyon_indeksi < birinci_sinir:
        kesif_orani = 1.00
        ad = "FAZ-1 TAM KESIF"
        no = 1
        baslangic = 0
        bitis = birinci_sinir
    elif iterasyon_indeksi < ikinci_sinir:
        kesif_orani = 0.45
        ad = "FAZ-2 KESIF + SINYAL"
        no = 2
        baslangic = birinci_sinir
        bitis = ikinci_sinir
    else:
        kesif_orani = 0.20
        ad = "FAZ-3 YOGUNLASMA + KACIS"
        no = 3
        baslangic = ikinci_sinir
        bitis = toplam_iterasyon

    faz_uzunlugu = max(1, bitis - baslangic - 1)
    faz_ilerleme = max(0.0, min(1.0, (iterasyon_indeksi - baslangic) / faz_uzunlugu))

    kesifci_sayisi = max(1, int(round(hedef_yarasa_sayisi * kesif_orani)))
    odaklanmaci_sayisi = hedef_yarasa_sayisi - kesifci_sayisi

    return {
        "ad": ad,
        "no": no,
        "aktif_yarasa": hedef_yarasa_sayisi,
        "kesifci_sayisi": kesifci_sayisi,
        "odaklanmaci_sayisi": odaklanmaci_sayisi,
        "kesif_orani": kesif_orani,
        "baslangic": baslangic,
        "bitis": bitis,
            "ilerleme": faz_ilerleme,
        "sinyal_takibi": no >= 2,
        "yerel_arama": no == 3
                    }

# =====================================================
def arac_plani_uret(toplam_hacim, maksimum_arac=6, hedef_doluluk=0.85):
    """Toplam hacme gore hedef doluluga yakin temel arac planini olusturur."""
    tipler = list(araclar.keys())
    hedef_sayi = max(1, min(maksimum_arac, math.ceil(toplam_hacim / araclar["A-03"][3])))
    adaylar = []

    def tara(indeks, kalan_sayi, secilen):
        """Arac tipi kombinasyonlarini ozyinelemeli olarak tarar ve uygun plan adaylarini toplar."""
        if indeks == len(tipler) - 1:
            plan = secilen + [tipler[indeks]] * kalan_sayi
            kapasite = sum(araclar[t][3] for t in plan)
            if kapasite >= toplam_hacim:
                doluluk = toplam_hacim / kapasite
                if doluluk >= hedef_doluluk:
                    buyuk_arac_sayisi = plan.count("A-04") + plan.count("A-03")
                    orta_arac_sayisi = plan.count("A-03")
                    a04_eksik_cezasi = 1 if toplam_hacim > araclar["A-04"][3] and plan.count("A-04") == 0 else 0
                    hedefe_yakinlik = abs(doluluk - 0.87)
                    adaylar.append((a04_eksik_cezasi, hedefe_yakinlik, -orta_arac_sayisi, -buyuk_arac_sayisi, kapasite, plan))
            return

        for adet in range(kalan_sayi + 1):
            tara(indeks + 1, kalan_sayi - adet, secilen + [tipler[indeks]] * adet)

    for arac_sayisi in range(1, maksimum_arac + 1):
        adaylar = []
        tara(0, arac_sayisi, [])

        if len(adaylar) > 0:
            adaylar.sort()
            plan = adaylar[0][5]
            return sorted(plan, key=lambda t: araclar[t][3], reverse=True)

    plan = []
    kalan = toplam_hacim

    while kalan > 0 and len(plan) < maksimum_arac:
        tip = "A-04" if kalan > araclar["A-03"][3] * 1.2 else "A-03"
        plan.append(tip)
        kalan -= araclar[tip][3]

    return plan

# =====================================================
def arac_plan_adaylari_uret(toplam_hacim, maksimum_arac=8, hedef_doluluk=0.75):
    """Final yerlestirme icin yuksek doluluk verebilecek alternatif arac planlarini uretir."""
    tipler = list(araclar.keys())
    adaylar = []
    gevsek_adaylar = []

    def tara(indeks, kalan_sayi, secilen):
        """Arac tipi kombinasyonlarini ozyinelemeli olarak tarar ve uygun plan adaylarini toplar."""
        if indeks == len(tipler) - 1:
            plan = secilen + [tipler[indeks]] * kalan_sayi
            kapasite = sum(araclar[t][3] for t in plan)

            if kapasite >= toplam_hacim:
                doluluk = toplam_hacim / kapasite
                sirali_plan = sorted(plan, key=lambda t: araclar[t][3], reverse=True)
                kayit = (-doluluk, kapasite, len(plan), sirali_plan)

                if doluluk >= hedef_doluluk:
                    adaylar.append(kayit)
                elif doluluk >= 0.62:
                    gevsek_adaylar.append(kayit)
            return

        for adet in range(kalan_sayi + 1):
            tara(indeks + 1, kalan_sayi - adet, secilen + [tipler[indeks]] * adet)

    for arac_sayisi in range(1, maksimum_arac + 1):
        tara(0, arac_sayisi, [])

    secilenler = adaylar if len(adaylar) > 0 else gevsek_adaylar

    if len(secilenler) == 0:
        return [arac_plani_uret(toplam_hacim, maksimum_arac)]

    secilenler.sort(key=lambda x: (x[2], x[1], x[0]))
    benzersiz = []
    gorulen = set()

    for _, _, _, plan in secilenler:
        anahtar = tuple(sorted(plan))

        if anahtar not in gorulen:
            gorulen.add(anahtar)
            benzersiz.append(plan)

        if len(benzersiz) >= 7:
            break

    return benzersiz

# =====================================================
def planli_hacim_dagit(cozum):
    """Onceden uretilen arac planina gore kolileri hacim bazli ve hizli bicimde dagitir."""
    toplam_hacim = sum(item["koli"]["h"] for item in cozum)
    plan = arac_plani_uret(toplam_hacim)
    arac_listesi = []
    ceza = 0

    for tip in plan:
        arac_listesi.append({
            "tip": tip,
            "kalan": araclar[tip][3],
            "kullanilan": 0,
            "kapasite": araclar[tip][3]
        })

    for item in cozum:
        koli = item["koli"]
        tercih = item["arac"]
        adaylar = []

        for indeks, arac in enumerate(arac_listesi):
            if not arac_uygun_mu(koli, arac["tip"]) or koli["h"] > arac["kalan"]:
                continue

            tercih_bonus = 0 if arac["tip"] == tercih else 1
            kalan_sonra = arac["kalan"] - koli["h"]
            adaylar.append((tercih_bonus, -arac["kapasite"], kalan_sonra, indeks))

        if len(adaylar) == 0:
            uygunlar = uygun_araclar(koli)
            tip = max(uygunlar, key=lambda a: araclar[a][3]) if len(uygunlar) > 0 else "A-04"
            kapasite = araclar[tip][3]
            arac_listesi.append({
                "tip": tip,
                "kalan": kapasite - koli["h"],
                "kullanilan": koli["h"],
                "kapasite": kapasite
            })
            ceza += 750000
        else:
            adaylar.sort()
            secilen = adaylar[0][3]
            arac_listesi[secilen]["kalan"] -= koli["h"]
            arac_listesi[secilen]["kullanilan"] += koli["h"]

    return [a for a in arac_listesi if a["kullanilan"] > 0], ceza

# =====================================================
def arac_sec_bat(koli, freq, loudness, oran):
    """Yarasa parametrelerine gore koli icin kesif veya odak agirlikli arac tercihi yapar."""
    uygunlar = uygun_araclar(koli)

    if len(uygunlar) == 0:
        return random.choice(list(araclar.keys()))

    if oran < 0.25:
        return random.choice(uygunlar)

    buyukler = [a for a in uygunlar if a in ["A-03", "A-04"]]

    if len(buyukler) > 0:
        uygunlar = sorted(buyukler, key=lambda a: araclar[a][3])
    else:
        uygunlar = sorted(uygunlar, key=lambda a: araclar[a][3])
    hedef_indeks = min(len(uygunlar) - 1, int(freq / 2.81 * len(uygunlar)))

    if random.random() < 0.35 * loudness:
        return random.choice(uygunlar)

    return uygunlar[hedef_indeks]

# =====================================================
def komsu(cozum, iterasyon, max_iter, pulse, loudness, velocity, freq, hedef_cozum, faz_no):
    """Mevcut cozumden yarasa hareketini temsil eden yeni komsu cozum uretir."""
    yeni = deepcopy(cozum)
    oran = iterasyon / max_iter
    dalga_gucu = abs(velocity) + freq + loudness
    min_degisim = 1

    if faz_no == 1:
        max_degisim = max(6, int(len(yeni) * 0.75))
        degisim = random.randint(max(3, len(yeni) // 5), max_degisim)
        hedefe_yakinlas = 0.0
        rotasyon_orani = 0.95
        arac_degisim_orani = 0.95
        takas_orani = 0.75
        karistir_orani = 0.85
    elif faz_no == 2:
        max_degisim = max(4, int(len(yeni) * 0.38))
        degisim = int(min_degisim + dalga_gucu * 0.55 * max_degisim)
        hedefe_yakinlas = 0.18 + 0.35 * pulse
        rotasyon_orani = 0.62 + 0.25 * loudness
        arac_degisim_orani = 0.52 + 0.22 * freq
        takas_orani = 0.42
        karistir_orani = 0.35
    else:
        max_degisim = max(3, int(len(yeni) * 0.16))
        degisim = int(min_degisim + dalga_gucu * 0.28 * max_degisim)
        hedefe_yakinlas = 0.38 + 0.45 * pulse
        rotasyon_orani = 0.42 + 0.25 * loudness
        arac_degisim_orani = 0.30 + 0.18 * freq
        takas_orani = 0.18
        karistir_orani = 0.10

    degisim = max(1, min(degisim, len(yeni)))

    if faz_no >= 2 and random.random() < hedefe_yakinlas:
        yeni = deepcopy(hedef_cozum)

    for _ in range(degisim):
        idx = random.randint(0, len(yeni) - 1)

        if random.random() < rotasyon_orani:
            yeni[idx]["koli"] = rotate(yeni[idx]["koli"])

        if random.random() < arac_degisim_orani:
            if faz_no == 1:
                uygunlar = yuksek_doluluk_arac_adaylari(yeni[idx]["koli"])
                yeni[idx]["arac"] = random.choice(uygunlar) if len(uygunlar) > 0 else random.choice(list(araclar.keys()))
            else:
                yeni[idx]["arac"] = arac_sec_bat(yeni[idx]["koli"], freq, loudness, oran)

        if random.random() < takas_orani:
            j = random.randint(0, len(yeni) - 1)
            yeni[idx], yeni[j] = yeni[j], yeni[idx]

        if faz_no >= 2 and random.random() < hedefe_yakinlas:
            hedef_idx = random.randint(0, len(hedef_cozum) - 1)
            yeni[idx]["arac"] = hedef_cozum[hedef_idx]["arac"]

    if random.random() < karistir_orani:
        random.shuffle(yeni)

    return yeni

# =====================================================
def iyilestir(cozum):
    """Bir cozumu yerel arama hamleleriyle sikilastirmaya ve duzeltmeye calisir."""
    yeni = deepcopy(cozum)
    yeni.sort(key=lambda x: x["koli"]["h"], reverse=True)
    toplam_hacim = sum(item["koli"]["h"] for item in yeni)
    plan = arac_plani_uret(toplam_hacim)
    plan_kalan = [{"tip": tip, "kalan": araclar[tip][3]} for tip in plan]

    for item in yeni:
        uygunlar = uygun_araclar(item["koli"])
        adaylar = []

        for indeks, arac in enumerate(plan_kalan):
            if arac["tip"] in uygunlar and item["koli"]["h"] <= arac["kalan"]:
                adaylar.append((-araclar[arac["tip"]][3], arac["kalan"] - item["koli"]["h"], indeks))

        if len(adaylar) > 0:
            adaylar.sort()
            secilen = adaylar[0][2]
            item["arac"] = plan_kalan[secilen]["tip"]
            plan_kalan[secilen]["kalan"] -= item["koli"]["h"]
        elif len(uygunlar) > 0:
            buyukler = [a for a in uygunlar if a in ["A-03", "A-04"]]
            item["arac"] = min(buyukler, key=lambda a: araclar[a][3]) if len(buyukler) > 0 else uygunlar[-1]

    return yeni
# =====================================================
def yarasa_algoritmasi(koliler, yarasa_sayisi=50, iterasyon=200):
    """Fazli yarasa algoritmasini calistirir, adaylari degerlendirir ve en iyi 3D cozumu arar."""
    bats = []
    grafik_iterasyon_eniyi = []
    sinyal_merkezi = None
    faz1_arsiv = []
    faz1_arsiv_hedef = max(1, int(math.ceil(iterasyon * 0.20)))

    def arsive_ekle(kayitlar):
        """Birinci fazda bulunan iyi adaylari sinirli arsivde saklar ve sirali tutar."""
        nonlocal faz1_arsiv
        faz1_arsiv.extend(deepcopy(k) for k in kayitlar)
        faz1_arsiv.sort(key=lambda x: x["fitness"])
        faz1_arsiv = faz1_arsiv[:faz1_arsiv_hedef]

    print("\nBaslangic populasyonu olusturuluyor...")

    for i in range(yarasa_sayisi):
        s = random_cozum(koliler, baslangic=True)
        pulse = random.uniform(0.03, 0.14)
        baslangic_fit, baslangic_tip, baslangic_decoded, baslangic_ceza = fazli_fitness(s, 1)
        bats.append({
            "solution": s,
            "fitness": baslangic_fit,
            "fitness_tipi": baslangic_tip,
            "decoded": baslangic_decoded,
            "decoded_ceza": baslangic_ceza,
            "velocity": random.uniform(-2, 2),
            "freq": random.uniform(0.1, 2.5),
            "loudness": random.uniform(0.9, 1.0),
            "pulse": pulse,

            "pulse0": pulse
        })






        if (i + 1) % 5 == 0 or i + 1 == yarasa_sayisi:
            print("Baslangic yarasasi:", i + 1, "/", yarasa_sayisi)

    arsive_ekle(bats)
    final_eniyi = deepcopy(bats[0])
    gercek_eniyi = None
    son_iyilesme = 0
    onceki_faz = None

    print("\nIlk kayit fitness:", round(final_eniyi["fitness"], 4), "\n")

    for t in range(iterasyon):
        faz = faz_bilgisi(t, iterasyon, yarasa_sayisi)
        oran = t / iterasyon

        if faz["no"] != onceki_faz:
            print(
                "\n", faz["ad"],
                "| toplam yarasa:", yarasa_sayisi,
                "| kesifci:", faz["kesifci_sayisi"],
                "| odaklanmaci:", faz["odaklanmaci_sayisi"]
            )

            if faz["no"] == 2 and len(faz1_arsiv) > 0:
                bats = sorted(bats, key=lambda x: x["fitness"])
                aktarim_sayisi = min(len(faz1_arsiv), len(bats))

                for i in range(aktarim_sayisi):
                    hedef_indeks = len(bats) - 1 - i
                    kayit = faz1_arsiv[i]
                    yeni_fit, yeni_tip, yeni_decoded, yeni_ceza = fazli_fitness(kayit["solution"], 2, faz_ilerleme=faz["ilerleme"])
                    bats[hedef_indeks]["solution"] = deepcopy(kayit["solution"])
                    bats[hedef_indeks]["fitness"] = yeni_fit
                    bats[hedef_indeks]["fitness_tipi"] = yeni_tip
                    bats[hedef_indeks]["decoded"] = deepcopy(yeni_decoded) if yeni_decoded is not None else None
                    bats[hedef_indeks]["decoded_ceza"] = yeni_ceza
                    bats[hedef_indeks]["velocity"] = random.uniform(-1.2, 1.2)
                    bats[hedef_indeks]["freq"] = random.uniform(0.1, 2.5)

                sinyal_merkezi = deepcopy(min(bats, key=lambda x: x["fitness"]))
                print("| faz 1 arsiv aktarimi:", aktarim_sayisi, "kayit")

            onceki_faz = faz["no"]

        sirali = sorted(bats, key=lambda x: x["fitness"])
        elite = sirali[:min(7 if faz["no"] == 2 else 5, len(sirali))]
        aktif_eniyi = elite[0]

        if (faz["no"] == 1 or aktif_eniyi["fitness_tipi"] == "gercek3d") and aktif_eniyi["fitness"] < final_eniyi["fitness"]:
            final_eniyi = deepcopy(aktif_eniyi)
            if faz["sinyal_takibi"]:
                sinyal_merkezi = deepcopy(aktif_eniyi)
            son_iyilesme = t

        if faz["sinyal_takibi"] and (sinyal_merkezi is None or aktif_eniyi["fitness"] < sinyal_merkezi["fitness"]):
            sinyal_merkezi = deepcopy(aktif_eniyi)

        indeksler = list(range(len(bats)))

        if faz["no"] == 1:
            kesifci_indeksler = indeksler
            odaklanmaci_indeksler = []
        else:
            kesifci_indeksler = set(random.sample(indeksler, faz["kesifci_sayisi"]))
            odaklanmaci_indeksler = [i for i in indeksler if i not in kesifci_indeksler]
            kesifci_indeksler = list(kesifci_indeksler)

        adaylar = []

        for idx in kesifci_indeksler:
            b = bats[idx]
            beta = random.random()
            b["freq"] = 0.10 + (2.80 - 0.10) * beta
            b["velocity"] = (
                0.72 * b["velocity"] +
                random.uniform(-2.4, 2.4) * b["loudness"] +
                random.uniform(-1.2, 1.2) * b["freq"]
            )
            b["velocity"] = max(-7, min(7, b["velocity"]))
            hedef = random.choice(bats)["solution"]
            yeni = komsu(b["solution"], t, iterasyon, b["pulse"], b["loudness"], b["velocity"], b["freq"], hedef, 1)
            hizli_fit, hizli_tip, hizli_decoded, hizli_ceza = fazli_fitness(yeni, faz["no"], faz_ilerleme=faz["ilerleme"])
            adaylar.append({
                "idx": idx,
                "rol": "kesif",
                "solution": yeni,
                "fitness": hizli_fit,
                "fitness_tipi": hizli_tip,
                "decoded": hizli_decoded,
                "decoded_ceza": hizli_ceza
            })

        for idx in odaklanmaci_indeksler:
            b = bats[idx]
            beta = random.random()
            b["freq"] = 0.10 + (2.80 - 0.10) * beta
            fark = (b["fitness"] - aktif_eniyi["fitness"]) / (abs(aktif_eniyi["fitness"]) + 1)
            b["velocity"] = (0.84 * b["velocity"] + fark * b["freq"] + random.uniform(-1.2, 1.2) * b["loudness"])
            b["velocity"] = max(-6, min(6, b["velocity"]))
            hedef = random.choice(elite)

            if faz["no"] == 3 and sinyal_merkezi is not None and random.random() < 0.72:
                hedef = sinyal_merkezi

            yeni = komsu(b["solution"], t, iterasyon, b["pulse"], b["loudness"], b["velocity"], b["freq"], hedef["solution"], faz["no"])

            if faz["yerel_arama"] and random.random() < (0.10 + b["pulse"] * 0.45):
                yeni = iyilestir(yeni)

            hizli_fit, hizli_tip, hizli_decoded, hizli_ceza = fazli_fitness(yeni, faz["no"], faz_ilerleme=faz["ilerleme"])
            adaylar.append({
                "idx": idx,
                "rol": "odak",
                "solution": yeni,
                "fitness": hizli_fit,
                "fitness_tipi": hizli_tip,
                "decoded": hizli_decoded,
                "decoded_ceza": hizli_ceza
            })

        
gercek_kontrol_indeksleri = set()

        if faz["no"] == 2 and len(adaylar) > 0:
            kontrol_sayisi = max(1, int(math.ceil(len(adaylar) * 0.20)))
            sirali_aday_indeksleri = sorted(range(len(adaylar)), key=lambda i: adaylar[i]["fitness"])
            gercek_kontrol_indeksleri.update(sirali_aday_indeksleri[:kontrol_sayisi])

        if faz["no"] == 3:
            for i, aday in enumerate(adaylar):
                if aday["rol"] == "odak":
                    gercek_kontrol_indeksleri.add(i)

        gercek_kontrol_sayisi = 0

        for i in sorted(gercek_kontrol_indeksleri):
            gercek_fit, _, decoded, decoded_ceza = fazli_fitness(adaylar[i]["solution"], faz["no"], gercek_3d=True)
            adaylar[i]["fitness"] = gercek_fit
            adaylar[i]["fitness_tipi"] = "gercek3d"
            adaylar[i]["decoded"] = decoded
            adaylar[i]["decoded_ceza"] = decoded_ceza
            gercek_kontrol_sayisi += 1

            if gercek_eniyi is None or gercek_fit < gercek_eniyi["fitness"]:
                gercek_eniyi = deepcopy(adaylar[i])
                final_eniyi = deepcopy(adaylar[i])
                if faz["sinyal_takibi"]:
                    sinyal_merkezi = deepcopy(adaylar[i])
                son_iyilesme = t

        yanki_fitnessleri = []

        for aday in adaylar:
            b = bats[aday["idx"]]
            yeni_fit = aday["fitness"]
            yanki_fitnessleri.append(yeni_fit)
            fark_fit = yeni_fit - b["fitness"]
            sicaklik = max(1, b["loudness"] * 42000 * (1 - oran))
            yanki_kabul = math.exp(-max(0, fark_fit) / sicaklik)

            if aday["rol"] == "kesif":
                rastgele_kabul = 0.70 if faz["no"] == 1 else 0.42 if faz["no"] == 2 else 0.28
            else:
                rastgele_kabul = 0.16 if faz["no"] == 2 else 0.05

            kabul_et = (
                yeni_fit < b["fitness"] or
                random.random() < b["loudness"] * yanki_kabul or
                random.random() < rastgele_kabul
            )

            if kabul_et:
                b["solution"] = deepcopy(aday["solution"])
                b["fitness"] = yeni_fit
                b["fitness_tipi"] = aday["fitness_tipi"]
                b["decoded"] = deepcopy(aday["decoded"]) if aday["decoded"] is not None else None
                b["decoded_ceza"] = aday["decoded_ceza"]

                if aday["rol"] == "odak" and yeni_fit < final_eniyi["fitness"]:
                    b["loudness"] = max(0.12, b["loudness"] * 0.94)
                    b["pulse"] = min(0.95, b["pulse"] + (1 - b["pulse"]) * 0.035)
                else:
                    b["loudness"] = min(1.0, b["loudness"] * 1.01)
                    b["pulse"] = max(0.03, b["pulse"] * 0.99)

            if (faz["no"] == 1 or b["fitness_tipi"] == "gercek3d") and b["fitness"] < final_eniyi["fitness"]:
                final_eniyi = deepcopy(b)
                if faz["sinyal_takibi"]:
                    sinyal_merkezi = deepcopy(b)
                son_iyilesme = t

        if faz["no"] == 1:
            arsive_ekle(bats)
            arsive_ekle(adaylar)

        if len(yanki_fitnessleri) == 0:
            yanki_fitnessleri = [aktif_eniyi["fitness"]]

        iterasyondaki_en_iyi = min(yanki_fitnessleri)
        grafik_iterasyon_eniyi.append(iterasyondaki_en_iyi)

        if faz["no"] >= 2 and t - son_iyilesme > 10:
            reset_sayisi = max(1, len(bats) // 5)
            bats = sorted(bats, key=lambda x: x["fitness"])

            for i in range(reset_sayisi):
                idx = len(bats) - 1 - i
                s = random_cozum(koliler, baslangic=True)
                reset_fit, reset_tip, reset_decoded, reset_ceza = fazli_fitness(s, faz["no"], faz_ilerleme=faz["ilerleme"])
                bats[idx]["solution"] = s
                bats[idx]["fitness"] = reset_fit
                bats[idx]["fitness_tipi"] = reset_tip
                bats[idx]["decoded"] = reset_decoded
                bats[idx]["decoded_ceza"] = reset_ceza
                bats[idx]["loudness"] = random.uniform(0.9, 1.0)
                bats[idx]["pulse"] = random.uniform(0.03, 0.14)
                bats[idx]["velocity"] = random.uniform(-2, 2)
                bats[idx]["freq"] = random.uniform(0.1, 2.5)

            son_iyilesme = t

        print(
            "iterasyon:", t + 1,
            "| faz:", faz["no"],
            "| kesifci:", faz["kesifci_sayisi"],
            "| odaklanmaci:", faz["odaklanmaci_sayisi"],
            "| 3D kontrol sayisi:", gercek_kontrol_sayisi,
            "|  en iyi fitness:", round(iterasyondaki_en_iyi, 4),


        )

    print("\nFinal adaylari gercek 3D ile tekrar dogrulaniyor...")
    final_adaylari = [deepcopy(final_eniyi)]
    final_adaylari.extend(deepcopy(k) for k in sorted(bats, key=lambda x: x["fitness"])[:min(7, len(bats))])
    final_adaylari.extend(deepcopy(k) for k in faz1_arsiv[:min(3, len(faz1_arsiv))])

    if gercek_eniyi is not None:
        final_adaylari.append(deepcopy(gercek_eniyi))

    for kayit in final_adaylari:
        gercek_fit, decoded, decoded_ceza = final_3d_fitness(kayit["solution"])
        kayit["fitness"] = gercek_fit
        kayit["fitness_tipi"] = "final3d"
        kayit["decoded"] = decoded
        kayit["decoded_ceza"] = decoded_ceza

        if gercek_eniyi is None or gercek_fit < gercek_eniyi["fitness"]:
            gercek_eniyi = deepcopy(kayit)

    if gercek_eniyi is not None:
        final_eniyi = deepcopy(gercek_eniyi)

    if len(grafik_iterasyon_eniyi) > 0:
        grafik_iterasyon_eniyi[-1] = final_eniyi["fitness"]

    grafikler = {
        "iterasyon_eniyi": grafik_iterasyon_eniyi
    }

    return final_eniyi, grafikler

# =====================================================
# =====================================================

def kutular_cakisiyor(a, b):
    """Iki 3D kutunun koordinat araliklarina bakarak cakisip cakismadigini kontrol eder."""
    return not (
        a["px"] + a["d"] <= b["px"] or
        b["px"] + b["d"] <= a["px"] or
        a["py"] + a["y"] <= b["py"] or
        b["py"] + b["y"] <= a["py"] or
        a["pz"] + a["g"] <= b["pz"] or
        b["pz"] + b["g"] <= a["pz"]
    )

# =====================================================
def arac_detay_olustur(tip):
    """Bir arac tipi icin kapasite, kalan hacim ve koli listesi iceren detay kaydi olusturur."""
    return {
        "tip": tip,
        "kalan": araclar[tip][3],
        "kapasite": araclar[tip][3],
        "koliler": [],
        "adaylar": {(0, 0, 0)},
        "dolu_hucreler": set()
    }

# =====================================================
def koli_orientasyonlari(koli):
    """Bir kolinin benzersiz boyut siralamalarini 3D oryantasyon adayi olarak uretir."""
    orientasyonlar = []
    gorulen = set()

    for d, y, g in [
        (koli["d"], koli["y"], koli["g"]),
        (koli["d"], koli["g"], koli["y"]),
        (koli["y"], koli["d"], koli["g"]),
        (koli["y"], koli["g"], koli["d"]),
        (koli["g"], koli["d"], koli["y"]),
        (koli["g"], koli["y"], koli["d"])
    ]:
        anahtar = (d, y, g)

        if anahtar not in gorulen:
            yeni = deepcopy(koli)
            yeni["d"] = d
            yeni["y"] = y
            yeni["g"] = g
            orientasyonlar.append(yeni)
            gorulen.add(anahtar)

    return orientasyonlar

# =====================================================
def dikdortgen_kapsar(a, b):
    """Bir serbest dikdortgenin digerini tamamen kapsayip kapsamadigini kontrol eder."""
    ax, az, ad, ag = a
    bx, bz, bd, bg = b
    return ax <= bx and az <= bz and ax + ad >= bx + bd and az + ag >= bz + bg

# =====================================================
def serbest_dikdortgenleri_temizle(dikdortgenler):
    """MaxRects icin gereksiz veya kapsanan serbest dikdortgenleri listeden temizler."""
    temiz = []

    for d in sorted(set(dikdortgenler), key=lambda r: r[2] * r[3], reverse=True):
        if d[2] <= 0 or d[3] <= 0:
            continue

        if any(dikdortgen_kapsar(t, d) for t in temiz):
            continue

        temiz.append(d)

    return temiz[:80]

# =====================================================
def dikdortgen_bol(serbest, x, z, d, g):
    """Yerlesen koli alanindan sonra kalan serbest dikdortgenleri parcalara boler."""
    sx, sz, sd, sg = serbest
    yeni = []

    if x + d < sx + sd:
        yeni.append((x + d, sz, sx + sd - (x + d), sg))

    if z + g < sz + sg:
        yeni.append((sx, z + g, sd, sz + sg - (z + g)))

    if x > sx:
        yeni.append((sx, sz, x - sx, sg))

    if z > sz:
        yeni.append((sx, sz, sd, z - sz))

    return [r for r in yeni if r[2] > 0 and r[3] > 0]

# =====================================================
def dikdortgenler_kesisiyor(a, b):
    """Iki 2D dikdortgen alaninin kesismesi olup olmadigini hesaplar."""
    ax, az, ad, ag = a
    bx, bz, bd, bg = b
    return not (
        ax + ad <= bx or
        bx + bd <= ax or
        az + ag <= bz or
        bz + bg <= az
    )

# =====================================================
def tum_serbestleri_guncelle(serbestler, x, z, d, g):
    """Yeni yerlestirme sonrasi tum serbest dikdortgenleri boler ve temizler."""
    yerlesen = (x, z, d, g)
    yeni = []

    for serbest in serbestler:
        if dikdortgenler_kesisiyor(serbest, yerlesen):
            yeni.extend(dikdortgen_bol(serbest, x, z, d, g))
        else:
            yeni.append(serbest)

    return serbest_dikdortgenleri_temizle(yeni)

# =====================================================
def arac_detay_katman_olustur(tip):
    """MaxRects katman bilgisi eklenmis arac detay yapisini hazirlar."""
    arac = arac_detay_olustur(tip)
    arac["katmanlar"] = []
    return arac

# =====================================================
def maxrects_koli_yerlestir(arac, koli):
    """Bir koliyi arac icindeki en uygun katman ve serbest alana 3D olarak yerlestirir."""
    tip = arac["tip"]
    D = araclar[tip][0]
    Y = araclar[tip][1]
    G = araclar[tip][2]
    en_iyi = None

    if koli["h"] > arac["kalan"]:
        return False

    for aday_koli in koli_orientasyonlari(koli):
        if not arac_uygun_mu(aday_koli, tip):
            continue

        for katman_indeks, katman in enumerate(arac["katmanlar"]):
            if aday_koli["y"] > katman["yukseklik"]:
                continue

            for dikdortgen_indeks, dikdortgen in enumerate(katman["serbest"]):
                px, pz, bos_d, bos_g = dikdortgen

                if aday_koli["d"] <= bos_d and aday_koli["g"] <= bos_g:
                    fire = bos_d * bos_g - aday_koli["d"] * aday_koli["g"]
                    skor = (0, fire, katman["py"], pz, px)
                    aday = (skor, katman_indeks, dikdortgen_indeks, aday_koli, px, katman["py"], pz)

                    if en_iyi is None or aday[0] < en_iyi[0]:
                        en_iyi = aday

        kullanilan_y = sum(k["yukseklik"] for k in arac["katmanlar"])

        if kullanilan_y + aday_koli["y"] <= Y:
            fire = D * G - aday_koli["d"] * aday_koli["g"]
            skor = (1, fire, kullanilan_y, 0, 0)
            aday = (skor, None, None, aday_koli, 0, kullanilan_y, 0)

            if en_iyi is None or aday[0] < en_iyi[0]:
                en_iyi = aday

    if en_iyi is None:
        return False

    _, katman_indeks, dikdortgen_indeks, secilen, px, py, pz = en_iyi

    if katman_indeks is None:
        arac["katmanlar"].append({
            "py": py,
            "yukseklik": secilen["y"],
            "serbest": [(0, 0, D, G)]
        })
        katman_indeks = len(arac["katmanlar"]) - 1
        dikdortgen_indeks = 0

    katman = arac["katmanlar"][katman_indeks]
    katman["serbest"] = tum_serbestleri_guncelle(
        katman["serbest"],
        px,
        pz,
        secilen["d"],
        secilen["g"]
    )

    arac["kalan"] -= secilen["h"]
    arac["koliler"].append({
        "id": secilen["id"],
        "hacim": secilen["h"],
        "d": secilen["d"],
        "y": secilen["y"],
        "g": secilen["g"],
        "px": px,
        "py": py,
        "pz": pz
    })

    return True

# =====================================================
def cozum_sirasi_uret(cozum, mod):
    """Yerlestirme denemesi icin cozumdeki kolileri secilen siralama moduna gore dizer."""
    if mod == "yarasa":
        return deepcopy(cozum)

    if mod == "hacim":
        return sorted(cozum, key=lambda x: (x["koli"]["h"], max(x["koli"]["d"], x["koli"]["y"], x["koli"]["g"])), reverse=True)

    if mod == "uzun":
        return sorted(cozum, key=lambda x: (max(x["koli"]["d"], x["koli"]["y"], x["koli"]["g"]), x["koli"]["h"]), reverse=True)

    return sorted(cozum, key=lambda x: (x["koli"]["y"], x["koli"]["h"]), reverse=True)

# =====================================================
def maxrects_plan_dene(cozum, plan, mod, yeni_arac_ekle=False):
    """Belirli arac plani ve siralama modu ile tum kolileri MaxRects yontemiyle yerlestirmeyi dener."""
    araclar_detay = [arac_detay_katman_olustur(tip) for tip in plan]
    ceza = 0
    yerlesmeyen = 0
    sirali_cozum = cozum_sirasi_uret(cozum, mod)

    for item in sirali_cozum:
        koli = item["koli"]
        tercih = item["arac"]
        adaylar = []

        for indeks, arac in enumerate(araclar_detay):
            if not arac_uygun_mu(koli, arac["tip"]) or koli["h"] > arac["kalan"]:
                continue

            kopya = deepcopy(arac)

            if maxrects_koli_yerlestir(kopya, koli):
                tercih_bonus = 0 if arac["tip"] == tercih else 1
                kullanilan_sonra = kopya["kapasite"] - kopya["kalan"]
                doluluk_sonra = kullanilan_sonra / kopya["kapasite"]
                adaylar.append((-doluluk_sonra, kopya["kalan"], tercih_bonus, -kopya["kapasite"], indeks, kopya))

        if len(adaylar) == 0:
            if yeni_arac_ekle:
                tip = yeni_arac_tipi_sec(koli, 0, tercih)
                yeni_arac = arac_detay_katman_olustur(tip)

                if maxrects_koli_yerlestir(yeni_arac, koli):
                    araclar_detay.append(yeni_arac)
                    ceza += 950000
                else:
                    yerlesmeyen += 1
                    ceza += 4000000 + koli["h"] * 1000
            else:
                yerlesmeyen += 1
                ceza += 4000000 + koli["h"] * 1000
        else:
            adaylar.sort()
            secilen = adaylar[0]
            araclar_detay[secilen[4]] = secilen[5]

    araclar_detay = [a for a in araclar_detay if len(a["koliler"]) > 0]
    return araclar_detay, ceza, yerlesmeyen

# =====================================================
def maxrects_skorla(araclar_detay, ceza, yerlesmeyen):
    """MaxRects yerlestirme sonucunu arac sayisi, doluluk, bosluk ve cezalara gore puanlar."""
    if len(araclar_detay) == 0:
        return 10**12

    toplam_kapasite = sum(a["kapasite"] for a in araclar_detay)
    toplam_kullanilan = sum(a["kapasite"] - a["kalan"] for a in araclar_detay)
    toplam_bos = toplam_kapasite - toplam_kullanilan
    ortalama_doluluk = toplam_kullanilan / toplam_kapasite if toplam_kapasite > 0 else 0
    doluluk_cezasi = 0
    denge_cezasi = 0
    doluluklar = []

    if ortalama_doluluk < 0.75:
        doluluk_cezasi += (0.75 - ortalama_doluluk) * 15000000

    for arac in araclar_detay:
        kullanilan = arac["kapasite"] - arac["kalan"]
        doluluk = kullanilan / arac["kapasite"]
        doluluklar.append(doluluk)

        if doluluk < 0.75:
            doluluk_cezasi += (0.75 - doluluk) * arac["kapasite"] * 320

        if doluluk < 0.50:
            doluluk_cezasi += (0.50 - doluluk) * arac["kapasite"] * 650

    if len(doluluklar) > 0:
        ort = sum(doluluklar) / len(doluluklar)

        for doluluk in doluluklar:
            denge_cezasi += abs(doluluk - ort) * 300000

    return (
        yerlesmeyen * 100000000 +
        len(araclar_detay) * 1000000 +
        toplam_bos * 45 +
        doluluk_cezasi +
        denge_cezasi +
        ceza
    )

# =====================================================
def maxrects_cozumden_arac_detay_uret(cozum):
    """Bir cozumden alternatif planlari deneyerek en iyi gercek 3D arac detaylarini uretir."""
    toplam_hacim = sum(item["koli"]["h"] for item in cozum)
    planlar = arac_plan_adaylari_uret(toplam_hacim)
    en_iyi_araclar = None
    en_iyi_ceza = None
    en_iyi_yerlesmeyen = None

    erken_bitti = False

    for plan in planlar:
        for mod in ["hacim", "uzun", "katman", "yarasa"]:
            araclar_detay, ceza, yerlesmeyen = maxrects_plan_dene(cozum, plan, mod, yeni_arac_ekle=False)
            skor = maxrects_skorla(araclar_detay, ceza, yerlesmeyen)

            if en_iyi_ceza is None or skor < en_iyi_ceza:
                en_iyi_ceza = skor
                en_iyi_araclar = araclar_detay
                en_iyi_yerlesmeyen = yerlesmeyen

            if yerlesmeyen == 0:
                toplam_kapasite = sum(a["kapasite"] for a in araclar_detay)
                toplam_kullanilan = sum(a["kapasite"] - a["kalan"] for a in araclar_detay)
                ortalama = toplam_kullanilan / toplam_kapasite if toplam_kapasite > 0 else 0

                if ortalama >= 0.75:
                    erken_bitti = True
                    break

        if erken_bitti:
            break

    if en_iyi_yerlesmeyen is None or en_iyi_yerlesmeyen > 0:
        for mod in ["hacim", "uzun", "katman", "yarasa"]:
            araclar_detay, ceza, yerlesmeyen = maxrects_plan_dene(
                cozum,
                arac_plani_uret(toplam_hacim),
                mod,
                yeni_arac_ekle=True
            )
            skor = maxrects_skorla(araclar_detay, ceza, yerlesmeyen)

            if en_iyi_ceza is None or skor < en_iyi_ceza:
                en_iyi_ceza = skor
                en_iyi_araclar = araclar_detay
                en_iyi_yerlesmeyen = yerlesmeyen

    for arac in en_iyi_araclar:
        if "katmanlar" in arac:
            del arac["katmanlar"]
        if "adaylar" in arac:
            del arac["adaylar"]
        if "dolu_hucreler" in arac:
            del arac["dolu_hucreler"]

    return en_iyi_araclar, 0 if en_iyi_yerlesmeyen == 0 else 2000000 * en_iyi_yerlesmeyen

# =====================================================
def yeni_arac_tipi_sec(koli, kalan_toplam, tercih):
    """Yerlestirilemeyen koli icin uygun ve mantikli yeni arac tipini secer."""
    uygunlar = uygun_araclar(koli)

    if len(uygunlar) == 0:
        return random.choice(list(araclar.keys()))

    if tercih in uygunlar:
        return tercih

    buyukler = [a for a in uygunlar if a in ["A-03", "A-04"]]

    if len(buyukler) > 0:
        if kalan_toplam > araclar["A-03"][3] * 1.15 and "A-04" in buyukler:
            return "A-04"
        return min(buyukler, key=lambda a: araclar[a][3])

    return max(uygunlar, key=lambda a: araclar[a][3])
# =====================================================
def cozumden_arac_detay_uret(cozum):
    """Final rapor icin cozumden gercek 3D arac detaylarini ureten sarmal fonksiyondur."""
    return maxrects_cozumden_arac_detay_uret(cozum)

# =====================================================
def yerlesim_kontrol_et(araclar_detay):
    """Final yerlestirmede sinir asimi veya koli cakismasi olup olmadigini denetler."""
    hata_sayisi = 0

    for arac_no, arac in enumerate(araclar_detay, start=1):
        tip = arac["tip"]
        D = araclar[tip][0]
        Y = araclar[tip][1]
        G = araclar[tip][2]
        koliler = arac["koliler"]

        for i, koli in enumerate(koliler):
            sinir_asimi = (
                koli["px"] < 0 or
                koli["py"] < 0 or
                koli["pz"] < 0 or
                koli["px"] + koli["d"] > D or
                koli["py"] + koli["y"] > Y or
                koli["pz"] + koli["g"] > G
            )

            if sinir_asimi:
                hata_sayisi += 1
                print("UYARI: Arac", arac_no, koli["id"], "sinir disina tasiyor.")

            for diger in koliler[i+1:]:
                if kutular_cakisiyor(koli, diger):
                    hata_sayisi += 1
                    print("UYARI: Arac", arac_no, koli["id"], "ile", diger["id"], "cakisti.")

    return hata_sayisi

# =====================================================
def sonuc_tablosu_kaydet(araclar_detay):
    """Arac ve koli koordinatlarini CSV dosyasina rapor olarak kaydeder."""
    dosya_adi = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "yerlesim_tablosu.csv"
    )

    with open(dosya_adi, "w", newline="", encoding="utf-8") as dosya:
        yazici = csv.writer(dosya)
        yazici.writerow([
            "arac_no",
            "arac_tipi",
            "koli_id",
            "x",
            "y",
            "z",
            "derinlik",
            "yukseklik",
            "genislik",
            "hacim"
        ])

        for arac_no, arac in enumerate(araclar_detay, start=1):
            for koli in arac["koliler"]:
                yazici.writerow([
                    arac_no,
                    arac["tip"],
                    koli["id"],
                    koli["px"],
                    koli["py"],
                    koli["pz"],
                    koli["d"],
                    koli["y"],
                    koli["g"],
                    koli["hacim"]
                ])

    print("Yerlesim tablosu kaydediliyor:", dosya_adi)

# =====================================================
# =====================================================

def renk_uret(etiket):
    """Ayni koli tiplerinin 3D grafikte tutarli renkle gosterilmesi icin renk uretir."""
    rng = random.Random(etiket)
    return (
        0.25 + rng.random() * 0.55,
        0.25 + rng.random() * 0.55,
        0.25 + rng.random() * 0.55
    )

# =====================================================
def kasa_ciz(ax, D, Y, G):
    """3D grafikte aracin ic hacim sinirlarini tel kafes olarak cizer."""
    kenarlar = [
        [(0, 0, 0), (D, 0, 0)],
        [(D, 0, 0), (D, Y, 0)],
        [(D, Y, 0), (0, Y, 0)],
        [(0, Y, 0), (0, 0, 0)],
        [(0, 0, G), (D, 0, G)],
        [(D, 0, G), (D, Y, G)],
        [(D, Y, G), (0, Y, G)],
        [(0, Y, G), (0, 0, G)],
        [(0, 0, 0), (0, 0, G)],
        [(D, 0, 0), (D, 0, G)],
        [(D, Y, 0), (D, Y, G)],
        [(0, Y, 0), (0, Y, G)]
    ]

    for bas, bit in kenarlar:
        ax.plot(
            [bas[0], bit[0]],
            [bas[1], bit[1]],
            [bas[2], bit[2]],
            color="black",
            linewidth=1.4
        )

# =====================================================
def kutu_ciz(ax, x, y, z, dx, dy, dz, etiket):
    """Bir koliyi 3D grafikte koordinat ve boyutlariyla prizma olarak cizer."""
    noktalar = [
        [x, y, z],
        [x+dx, y, z],
        [x+dx, y+dy, z],
        [x, y+dy, z],
        [x, y, z+dz],
        [x+dx, y, z+dz],
        [x+dx, y+dy, z+dz],
        [x, y+dy, z+dz]
    ]
    yuzeyler = [
        [noktalar[0], noktalar[1], noktalar[2], noktalar[3]],
        [noktalar[4], noktalar[5], noktalar[6], noktalar[7]],
        [noktalar[0], noktalar[1], noktalar[5], noktalar[4]],
        [noktalar[2], noktalar[3], noktalar[7], noktalar[6]],
        [noktalar[1], noktalar[2], noktalar[6], noktalar[5]],
        [noktalar[4], noktalar[7], noktalar[3], noktalar[0]]
    ]
    ax.add_collection3d(
        Poly3DCollection(
            yuzeyler,
            alpha=0.45,
            edgecolor="black",
            facecolor=renk_uret(etiket)
        )
    )
    ax.text(
        x + dx/2,
        y + dy/2,
        z + dz/2,
        etiket,
        fontsize=7
    )

# =====================================================
def arac_3d_ciz(arac, arac_no):
    """Bir aracin tum kolilerini 3D model olarak cizer ve gorsel dosyaya kaydeder."""
    tip = arac["tip"]
    D = araclar[tip][0]
    Y = araclar[tip][1]
    G = araclar[tip][2]
    fig = plt.figure(figsize=(9, 6))
    ax = fig.add_subplot(111, projection="3d")
    kasa_ciz(ax, D, Y, G)
    sirali_koliler = sorted(arac["koliler"], key=lambda k: (k["pz"], k["py"], k["px"]))

    for koli in sirali_koliler:
        kutu_ciz(
            ax,
            koli["px"],
            koli["py"],
            koli["pz"],
            koli["d"],
            koli["y"],
            koli["g"],
            koli["id"]
        )

    ax.set_xlim(0, D)
    ax.set_ylim(0, Y)
    ax.set_zlim(0, G)
    ax.set_box_aspect((D, Y, G))
    ax.set_xlabel("Derinlik")
    ax.set_ylabel("Yukseklik")
    ax.set_zlabel("Genislik")
    ax.set_title(tip + "_" + str(arac_no) + " Gercek Koordinatli 3D Yerlesim")
    ax.view_init(elev=22, azim=-55)
    kullanilan = arac["kapasite"] - arac["kalan"]
    doluluk = (kullanilan / arac["kapasite"]) * 100
    ax.text2D(
        0.03,
        0.95,
        "Doluluk: %" + str(round(doluluk, 2)),
        transform=ax.transAxes,
        fontsize=9
    )
    ax.text2D(
        0.03,
        0.90,
        "Koordinatlar gercek yerlestirme sonucundan cizildi",
        transform=ax.transAxes,
        fontsize=8
    )
    dosya_adi = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        tip + "_" + str(arac_no) + ".png"
    )
    print("3D model kaydediliyor:", dosya_adi)
    plt.savefig(dosya_adi, dpi=300, bbox_inches="tight")
    plt.close()

# =====================================================
def sonuc_yaz(eniyi, sure):
    """En iyi cozumun arac, doluluk, koordinat, dogrulama ve modelleme raporunu ekrana yazar."""
    print("\n")
    print("="*60)
    print("EN IYI COZUM")
    print("="*60)
    print("\nEn iyi cozum gercek koordinatlara yerlestiriliyor...")

    if eniyi.get("decoded") is not None:
        araclar_detay = deepcopy(eniyi["decoded"])
        yerlesim_cezasi = eniyi.get("decoded_ceza", 0)
        print("Fitness asamasinda bulunan 3D yerlesim kullaniliyor.")
    else:
        araclar_detay, yerlesim_cezasi = cozumden_arac_detay_uret(eniyi["solution"])

    dogrulama_hatasi = yerlesim_kontrol_et(araclar_detay)
    sonuc_tablosu_kaydet(araclar_detay)
    toplam_hacim = 0
    toplam_kapasite = 0
    arac_sayac = {
        "A-01": 0,
        "A-02": 0,
        "A-03": 0,
        "A-04": 0
    }

    for i, a in enumerate(araclar_detay):
        arac_sayac[a["tip"]] += 1
        kullanilan = a["kapasite"] - a["kalan"]
        toplam_hacim += kullanilan
        toplam_kapasite += a["kapasite"]
        oran = (kullanilan / a["kapasite"]) * 100

        print("\n")
        print("-"*50)
        print("Arac", i+1)
        print("Arac tipi:", a["tip"])
        print("Kullanilan Hacim:", kullanilan, "/", a["kapasite"])
        print("Doluluk Orani:", round(oran, 2), "%")
        print("\nKoli Ozeti:")
        ozet = {}

        for k in a["koliler"]:
            kid = k["id"]

            if kid not in ozet:
                ozet[kid] = 0

            ozet[kid] += 1

        for x in ozet:
            print("-", x, ":", ozet[x], "adet")

        print("\nKoli Koordinatlari:")

        for k in a["koliler"]:
            print(
                "-",
                k["id"],
                "x:", k["px"],
                "y:", k["py"],
                "z:", k["pz"],
                "boyut:", str(k["d"]) + "x" + str(k["y"]) + "x" + str(k["g"])
            )

    print("\n")
    print("="*60)
    print("ARAC TURU DAGILIMI")
    print("="*60)

    for a in arac_sayac:
        print(a, "aracindan", arac_sayac[a], "adet kullanildi")

    ortalama = 0

    if toplam_kapasite > 0:
        ortalama = (toplam_hacim / toplam_kapasite) * 100

    print("\n")
    print("="*60)
    print("Toplam Kullanilan Arac:", len(araclar_detay))
    print("Toplam Tasinan Hacim:", toplam_hacim)
    print("Ortalama Doluluk:", round(ortalama, 2), "%")
    print("En iyi fitness:", round(eniyi["fitness"], 2))

    if yerlesim_cezasi > 0:
        print("Yerlesim ceza puani:", yerlesim_cezasi)



    print("Calisma suresi:", round(sure, 2), "saniye")
    print("\n3D arac modellemeleri olusturuluyor...")
    tip_sayac = {
        "A-01": 0,
        "A-02": 0,
        "A-03": 0,
        "A-04": 0
    }

    for a in araclar_detay:
        no = tip_sayac[a["tip"]]
        arac_3d_ciz(a, no)
        tip_sayac[a["tip"]] += 1

    print("="*60)

# =====================================================
def grafik_ciz(grafikler):
    """Yarasa algoritmasinin fitness yakinsemesini grafik olarak kaydeder ve gosterir."""
    degerler = grafikler["iterasyon_eniyi"]
    iterasyonlar = list(range(1, len(degerler) + 1))

    plt.figure(figsize=(12, 6))
    plt.plot(
        iterasyonlar,
        degerler,
        linewidth=1.8,
        marker="o",
        markersize=3.5,
        label="Iterasyon Basina En Iyi Fitness"
    )
    plt.xlabel("Iterasyon")
    plt.ylabel("Fitness")
    plt.title("Yarasa Algoritmasi Iterasyon Fitness Grafigi")
    plt.grid(True, which="major", linewidth=0.7, alpha=0.75)
    plt.minorticks_on()
    plt.grid(True, which="minor", linewidth=0.35, alpha=0.30)

    if len(degerler) > 0:
        en_kucuk = min(degerler)
        en_buyuk = max(degerler)
        aralik = en_buyuk - en_kucuk
        pay = aralik * 0.08 if aralik > 0 else max(1, abs(en_kucuk) * 0.02)
        plt.ylim(en_kucuk - pay, en_buyuk + pay)
        plt.xlim(1, max(1, len(degerler)))

    plt.legend()
    dosya_adi = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "yakinsama.png"
    )
    print("Yakinsama grafigi kaydediliyor:", dosya_adi)
    plt.savefig(dosya_adi, dpi=400, bbox_inches="tight")
    plt.show()

# =====================================================
def main():
    """Program akisinin veri alma, algoritma calistirma, raporlama ve grafik adimlarini yonetir."""
    print("\n")
    print("." * 50)
    print("3D Yerlestirme & Yarasa Algoritmasi")
    print("." * 50)
    koliler = veri_al()
    koli_sayisi = len(koliler)
    iterasyon_sayisi = max(40, int(round(koli_sayisi / 6 + 16.67)))
    yarasa_sayisi = max(24, min(80, int(18 + math.sqrt(max(1, koli_sayisi)) * 2 + koli_sayisi / 200)))

    print("\nToplam koli sayisi:", koli_sayisi)
    print("Otomatik yarasa sayisi:", yarasa_sayisi)
    print("Otomatik iterasyon sayisi:", iterasyon_sayisi)

    basla = time.time()
    eniyi, grafikler = yarasa_algoritmasi(
        koliler,
        yarasa_sayisi=yarasa_sayisi,
        iterasyon=iterasyon_sayisi,
    )
    bitir = time.time()
    sonuc_yaz(eniyi, bitir - basla)
    grafik_ciz(grafikler)

# =====================================================
if __name__ == "__main__":

    main()
