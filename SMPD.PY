import math
import numpy as np
from itertools import combinations
from random import randrange


# Klasa przedstawiająca punkty
# Każdy punkt zawiera kategorię oraz zbiór cech
class Pkt:

    def __init__(self, klasa, cechy):
        self.cecha = {}
        self.klasa = klasa
        for i in range(len(cechy)):
            self.cecha[i + 1] = float(cechy[i])


# # Listy zawierające punkty klasy
# klasaA = []
# klasaB = []
# klasaTest = []


# czytanie pliku i dodawanie do klas punktów
def odczyt_pliku(sciezka):
    try:
        plik = open(sciezka)
        for linia in plik:
            x = randrange(5)
            kategoria = linia[0:linia.index(" ")]
            if kategoria == "A" or kategoria == "Acer":
                if x == 0 and len(klasaTest)<156:
                    klasaTest.append(Pkt('acer', linia[linia.index(",") + 1:].split(',')))
                else:
                    klasaA.append(Pkt('acer', linia[linia.index(",") + 1:].split(',')))
            else:
                if x == 0 and len(klasaTest)<156:
                    klasaTest.append(Pkt('quercus', linia[linia.index(",") + 1:].split(',')))
                else:
                    klasaB.append(Pkt('quercus', linia[linia.index(",") + 1:].split(',')))
            # print(linia)
        print("Ilośc elementów w klasie A: ", len(klasaA))
        print("Ilośc elementów w klasie B: ", len(klasaB))
        print("Ilośc elementów w klasie test: ", len(klasaTest))

    finally:
        plik.close()


# funkcja zwracająca odległość euklidesową pomiędzy 2 punktami
def odleglosc(pkt1, pkt2):
    odleglosc = 0
    # print(pkt1.cecha)
    for i in range(len(pkt1.cecha)):
        odleglosc += (list(pkt1.cecha.values())[i] - list(pkt2.cecha.values())[i]) ** 2
    return math.sqrt(odleglosc)

def odleglosc2(pkt1, pkt2):
    odleglosc = 0
    for keys in pkt1.cecha:
        odleglosc += (pkt1.cecha[keys] - pkt2.cecha[keys]) ** 2
    return math.sqrt(odleglosc)

# NN-algorytm, Przyjmuje sprawdzany punkt i ilość k. Zwracqa klasę do której należy punkt
def k_nn_algorytm(k, test, *klasy):
    dobry_wynik = 0
    zly_wynik = 0
    for pkt in test:
        odleglosci = []
        for klasa in klasy:
            for punkcik in klasa:
                odleglosci.append({'klasa': punkcik.klasa, 'odleglosc': odleglosc(punkcik, pkt)})
                # print(punkcik.klasa, odleglosc(punkcik,pkt))
        # for i in odleglosci:
        #     if i['klasa'] == "acer":
        #         print("YEP")
        najblizsze_pkt = []
        for i in range(k):
            najblizsze_pkt.append(sorted(odleglosci, key=lambda i: i['odleglosc'], reverse=False)[i]['klasa'])
        # print(najblizsze_pkt)
        if najblizsze_pkt.count(klasaA[0].klasa) > najblizsze_pkt.count(klasaB[0].klasa):
            klasyfikacja = klasaA[0].klasa
        else:
            klasyfikacja = klasaB[0].klasa
        if klasyfikacja == pkt.klasa:
            dobry_wynik += 1
        else:
            # print("Not OK")
            zly_wynik += 1
    print("liczba zlych klasyfikacji: ", zly_wynik)
    print("Liczba dobrych klasyfikacji ", dobry_wynik)
    print("policzyłem dobrze na poziomie: ", round((dobry_wynik / (dobry_wynik + zly_wynik)) * 100, 2), "%")



# funkcja zwracająca punkt który jest środkiem danej listy punktów
def srednie(lista_pkt):
    same_cechy = []
    for punkt in lista_pkt:
        same_cechy.append(punkt.cecha)
    wynik = []
    # print(len(same_cechy))
    for key in same_cechy[0].keys():
        wynik.append((sum(item[key] for item in same_cechy)) / len(same_cechy))
    # print(wynik)
    return Pkt(lista_pkt[0].klasa, wynik)


def nm_algorytm(test):
    dobry_wynik = 0
    zly_wynik = 0
    for punkt in test:
        odlegloscA = odleglosc(punkt, srednie(klasaA))
        odlegloscB = odleglosc(punkt, srednie(klasaB))
        if odlegloscA < odlegloscB:
            klasyfikacja = klasaA[0].klasa
        else:
            klasyfikacja = klasaB[0].klasa
        if klasyfikacja == punkt.klasa:
            # print("OK")
            dobry_wynik += 1
        else:
            # print("Not OK")
            zly_wynik += 1
    print("liczba zlych klasyfikacji: ", zly_wynik)
    print("Liczba dobrych klasyfikacji ", dobry_wynik)
    print("policzyłem dobrze na poziomie: ", round((dobry_wynik / (dobry_wynik + zly_wynik)) * 100,2), "%")


def podzialNaPodklasy(k, listaPkt):
    srodki = []
    listaPodKlas = []
    for i in range(k):
        nowaPodKlasa = []
        listaPodKlas.append(nowaPodKlasa)
        # listaPkt[i].klasa += " " +str(i)
        srodki.append(listaPkt[i])
        listaPodKlas[i].append(listaPkt[i])
    # print(listaPodKlas[1][0].klasa)

    for z in range(20):
        for i in range(len(listaPkt)):
            odlegloscOdSrodka = []
            # print("licze odległosć dla :", listaPkt[i].klasa, listaPkt[i].cecha)
            for j in range(k):
                odlegloscOdSrodka.append(odleglosc(srodki[j], listaPkt[i]))
            listaPodKlas[odlegloscOdSrodka.index(min(odlegloscOdSrodka))].append(listaPkt[i])

        # for i in range(k):
        #     print("Klasa: ", i)
        #     for punkcik in listaPodKlas[i]:
        #         print(punkcik.klasa, punkcik.cecha)

        noweSrodki = []
        checkpoint = True
        for i in range(k):
            noweSrodki.append(srednie(listaPodKlas[i]))
            # print('Nowy srodek: ', noweSrodki[i].cecha)
            # print('Srodek: ', srodki[i].cecha)
            # print('Srodek: ', srodki[i].klasa)
            if odleglosc(noweSrodki[i], srodki[i]) != 0:
                checkpoint = False
            listaPodKlas[i].clear()
        if checkpoint:
            print("Wykonałem tyle powtórzeń: ", z)
            break
        else:
            srodki.clear()
            srodki = noweSrodki[:]

    # print("srodki: ", srodki)
    # print(srodki[0].klasa, srodki[0].cecha)
    return srodki


def podzialNaPodklasy2(k, listaPkt):
    srodki = []
    listaPodKlas = []
    for i in range(k):
        nowaPodKlasa = []
        listaPodKlas.append(nowaPodKlasa)
        srodki.append(listaPkt[i])
        listaPodKlas[i].append(listaPkt[i])
    for z in range(20):
        for i in range(len(listaPkt)):
            odlegloscOdSrodka = []
            for j in range(k):
                odlegloscOdSrodka.append(odleglosc(srodki[j], listaPkt[i]))
            listaPodKlas[odlegloscOdSrodka.index(min(odlegloscOdSrodka))].append(listaPkt[i])
        noweSrodki = []
        checkpoint = True
        for i in range(k):
            noweSrodki.append(srednie(listaPodKlas[i]))
            if odleglosc(noweSrodki[i], srodki[i]) != 0:
                checkpoint = False
            listaPodKlas[i].clear()
        if checkpoint:
            print("Wykonałem tyle powtórzeń: ", z)
            break
        else:
            srodki.clear()
            srodki = noweSrodki[:]
    return srodki


def k_nm_algorytm(k, test, *klasy):
    nowe_srodki = []
    for klasa in klasy:
        nowe_srodki.extend(podzialNaPodklasy(k, klasa))
    # print("to są środki :", nowe_srodki)
    k_nn_algorytm(1, test, nowe_srodki)

def wybor_cech(k):
    sredniaA = srednie(klasaA)
    sredniaB = srednie(klasaB)
    najlepsze_cechy = []
    ilosc_cech = list(range(1, len(klasaA[0].cecha) + 1))
    # print(ilosc_cech)
    comb = combinations(ilosc_cech, k)
    for i in list(comb):
        macierzA = np.zeros(shape=(k, len(klasaA)))
        macierzB = np.zeros(shape=(k, len(klasaB)))
        licznik = 0.0
        # print(i)
        for j in range(k):
            # licznik[j]=[sredniaA.cecha[j+1],sredniaB.cecha[j+1]]
            licznik = licznik + (sredniaA.cecha[i[j]] - sredniaB.cecha[i[j]]) ** 2
            wierszA = []
            wierszB = []
            for punkcikA in klasaA:
                wierszA.append(punkcikA.cecha[i[j]] - sredniaA.cecha[i[j]])
            for punkcikB in klasaB:
                wierszB.append(punkcikB.cecha[i[j]] - sredniaB.cecha[i[j]])
            macierzA[j] = wierszA
            macierzB[j] = wierszB
        licznik = math.sqrt(licznik)
        macierzA = np.dot(macierzA, macierzA.T)
        macierzB = np.dot(macierzB, macierzB.T)
        if k == 1:
            mianownik = math.sqrt(macierzA) + math.sqrt(macierzB)
        else:
            mianownik = np.linalg.det(macierzA) + np.linalg.det(macierzB)
        fisher = math.fabs(licznik) / mianownik
        najlepsze_cechy.append({'cechy': i, 'wartosc': fisher})
        # print(fisher)
    print("Oto najlepsze cechy: ", sorted(najlepsze_cechy, key=lambda i: i['wartosc'], reverse=True)[0]['cechy'], "\n")
    zapisz_nowe_cechy(sorted(najlepsze_cechy, key=lambda i: i['wartosc'], reverse=True)[0]['cechy'], klasaA, klasaB,
                      klasaTest)


def sfs_algorytm(k):
    sredniaA = srednie(klasaA)
    sredniaB = srednie(klasaB)
    ilosc_cech = list(range(1, len(klasaA[0].cecha) + 1))
    najlepsze_cechy = []
    for iteracja in range(k):
        # comb = combinations(ilosc_cech, iteracja + 1)
        cechy = []
        for thing in najlepsze_cechy:
            if thing in ilosc_cech: ilosc_cech.remove(thing)
        for i in combinations(ilosc_cech, 1):
            kombinacje = najlepsze_cechy[:]
            for element in i:
                if element not in kombinacje:
                    kombinacje.append(element)
            # print(kombinacje)

            macierzA = np.zeros(shape=(iteracja + 1, len(klasaA)))
            macierzB = np.zeros(shape=(iteracja + 1, len(klasaB)))
            licznik = 0.0
            # print(i)
            for j in range(len(kombinacje)):
                # licznik[j]=[sredniaA.cecha[j+1],sredniaB.cecha[j+1]]
                licznik = licznik + (sredniaA.cecha[kombinacje[j]] - sredniaB.cecha[kombinacje[j]]) ** 2
                wierszA = []
                wierszB = []
                # print(kombinacje[j])
                for punkcikA in klasaA:
                    wierszA.append(punkcikA.cecha[kombinacje[j]] - sredniaA.cecha[kombinacje[j]])
                for punkcikB in klasaB:
                    wierszB.append(punkcikB.cecha[kombinacje[j]] - sredniaB.cecha[kombinacje[j]])
                macierzA[j] = wierszA
                macierzB[j] = wierszB
            licznik = math.sqrt(licznik)
            macierzA = np.dot(macierzA, macierzA.T)
            macierzB = np.dot(macierzB, macierzB.T)
            if iteracja + 1 == 1:
                mianownik = math.sqrt(macierzA) + math.sqrt(macierzB)
            else:
                mianownik = np.linalg.det(macierzA) + np.linalg.det(macierzB)
            fisher = math.fabs(licznik) / mianownik
            # print("elo: ", kombinacje)
            cechy.append({'cechy': kombinacje[-1], 'wartosc': fisher})
            # print(fisher)
        najlepsze_cechy.append(sorted(cechy, key=lambda i: i['wartosc'], reverse=True)[0]['cechy'])
    print("Oto najlepsze cechy: ", sorted(najlepsze_cechy), "\n")
    zapisz_nowe_cechy(sorted(najlepsze_cechy), klasaA, klasaB, klasaTest)


def zapisz_nowe_cechy(nowe_cechy, *klasy):
    for klasa in klasy:
        for punkt in klasa:
            ceszki = {}
            for cecha in nowe_cechy:
                ceszki[cecha] = punkt.cecha[cecha]
            punkt.cecha = ceszki


def main():
    global klasaA
    global klasaB
    global klasaTest
    klasaA = []
    klasaB = []
    klasaTest = []
    mniej_cech = False
    # odczyt_pliku("k-NM.txt")
    # podzialNaPodklasy(3, klasaA)
    odczyt_pliku("Maple_Oak.txt")
    switcher = {
        1: wybor_cech,
        2: sfs_algorytm,
        3: k_nn_algorytm,
        4: k_nn_algorytm,
        5: nm_algorytm,
        6: k_nm_algorytm}
    wybor = 0
    while True:
        wybor = int(input("Co chcesz zrobić?\n"
                          "1. Policz najlepsze cechy - Fisher\n"
                          "2. Policz najlepsze cechy - SFS\n"
                          "3. Policz przynależność do klasy - NN\n"
                          "4. Policz przynależność do klasy - k-NN\n"
                          "5. Policz przynależność do klasy - NM\n"
                          "6. Policz przynależność do klasy - k-NM\n"
                          "7. Losuj raz jescze\n"
                          "8. Rzucić to wszystko i wyjechać w Bieszczady\n\n"
                          "WYBÓR: "))
        if wybor == 1:
            k = int(input("Podaj dla ilu cech mam policzyć: "))
            wybor_cech(k)
            mniej_cech=True
        if wybor == 2:
            k = int(input("Podaj dla ilu cech mam policzyć: "))
            sfs_algorytm(k)
            mniej_cech = True
        if wybor == 3:
            k_nn_algorytm(1, klasaTest, klasaA, klasaB)
        if wybor == 4:
            k = int(input("Podaj dla jakiego K mam policzyć: "))
            k_nn_algorytm(k, klasaTest, klasaA, klasaB)
        if wybor == 5:
            nm_algorytm(klasaTest)
        if wybor == 6:
            k = int(input("Podaj dla jakiego K mam policzyć: "))
            # podzialNaPodklasy(k,klasaA)
            k_nm_algorytm(k, klasaTest, klasaA, klasaB)
        if wybor == 7:
            klasaA.clear()
            klasaB.clear()
            klasaTest.clear()
            odczyt_pliku("Maple_Oak.txt")
        if wybor not in range(1, 8):
            print(""
                  "       /\\  /\\  /\\       \n"
                  "      /\\/\\/\\/\\/\\/\\      /\    /\  \n"
                  "     /    \\   \\   \\    /__\\  /__\\\n"
                  "    /      \\   \\   \\    ||    ||")
            print("Rzucam studia, jadę w Bieszczady")

            break

    #
    #
    # # print(odleglosc(klasaA[0], nowyPunkt))
    # # print(odleglosc(klasaB[0], nowyPunkt))
    # # print(nowyPunkt.cecha)
    # # print(odleglosc(klasaB[0], klasaA[0]))
    # # print(k_nn_algorytm(3, nowyPunkt, klasaA, klasaB))
    # # print(k_nn_algorytm(1, nowyPunkt, klasaA, klasaB))
    # # podzialNaPodklasy(4, klasaB)
    # # k_nm_algorytm(2,nowyPunkt, klasaA, klasaB)
    # # wybor_cech(3)
    # sfs_algorytm(6)
    # print(kl5
    #asaA[0].cecha)


if __name__ == "__main__":
    main()
0
