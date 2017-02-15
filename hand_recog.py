from math import sqrt, pow
import numpy
import cv2 as opencv

#klasa zbierajaca cala logike przetwarzania obrazu i obliczania charakterystyki dloni
class RozpoznawanieDloni(object):
    def __init__(self, sciezka_bazowa, pliki_dloni, plik_wynikowy):
        self.pliki_dloni = pliki_dloni
        self.plik_wynikowy = plik_wynikowy
        self.sciezka_bazowa = sciezka_bazowa

    #wykonywanie obliczen koncowych
    def wykonaj_obliczenia(self):
        kontury = []
        punkty = []
        dlugosci = []
        stosunek = []
        with open(plik_wynikowy, "w") as plk_wyn:
            for i in range(0,len(pliki_dloni)):
                sciezka = self.sciezka_bazowa + pliki_dloni[i] 
                obraz = opencv.imread(sciezka) 
                kontury.append(self.wykryj_kontur(obraz))
                punkty.append(self.wykryj_punkty_skrajne(kontury[i]))
                dlugosci.append(self.oblicz_dlugosci(punkty[i]))
                if i > 0:
                    stosunek.append(self.porownaj_dlugosci(dlugosci[0], dlugosci[i]))
                print pliki_dloni[i], ' ', '%s\n' % dlugosci[i]
            
            #plk_wyn.write('Podobienstwo pliku %s\n' % pliki_dloni[0])
            for i in range(0, len(stosunek)):
                plk_wyn.write('Plik %s jest podobny do pliku %s w %s%%\n' % (pliki_dloni[0], pliki_dloni[i+1], stosunek[i]))

            obraz1 = opencv.imread(self.sciezka_bazowa + pliki_dloni[0])
            self.rysuj_kontur(kontury[0], obraz1)
            self.rysuj_linie(obraz1, punkty)

            opencv.imshow("Obraz z konturem", obraz1)


    #wykrywanie konturu dloni
    def wykryj_kontur(self, obraz):
        ycrcb_obraz = opencv.cvtColor(obraz, opencv.COLOR_BGR2YCR_CB)
        ycrcb_min_skora = numpy.array((0, 145, 80)) #wartosci sprawdzone w internecie i skorygowane, aby pasowaly do wykonanych zdjec
        ycrcb_max_skora = numpy.array((255, 170, 130)) #jak wyzej^
        ycrcb_skora = opencv.inRange(ycrcb_obraz, ycrcb_min_skora, ycrcb_max_skora)
        _, kontury, _ = opencv.findContours(ycrcb_skora, opencv.RETR_EXTERNAL, opencv.CHAIN_APPROX_SIMPLE)
        
        return kontury

    #rysowanie konturu na zdjeciu
    def rysuj_kontur(self, kontury, obraz):
        for i, c in enumerate(kontury):
            powierzchnia = opencv.contourArea(c)
            if powierzchnia > 1000:
                opencv.drawContours(obraz, kontury, i, (255, 0, 0), 5)

    #rysowanie linii laczacych punkty skrajne
    def rysuj_linie(self, obraz, punkty):
        for i in range(1, len(punkty[0])):
            opencv.line(obraz, tuple(punkty[0][i-1]), tuple(punkty[0][i]), (0, 0, 255), 4)
                
         
    #wykrywanie punktow skrajnych na rece
    def wykryj_punkty_skrajne(self, kontury):     
        punkty = []
        kierunek = {'gdzie': 'gora'}

        def przelicz_kontur(kontur, kierunek):
            for i, punkt in enumerate(kontur):
                x,y = punkt
                if i < len(kontur) - 3:
                    x1, y1 = kontur[i + 1]
                    x2, y2 = kontur[i + 2]
                    if y > max(y1, y2) and kierunek['gdzie'] == 'gora':
                        punkty.append([x,y])
                        kierunek['gdzie'] = 'dol'
                    elif y < min(y1, y2) and kierunek['gdzie'] == 'dol':
                        punkty.append([x,y])
                        kierunek['gdzie'] = 'gora'
        
        [przelicz_kontur(kontur.reshape(-1, 2), kierunek) for kontur in kontury]
                        
        return punkty

                    
    #obliczanie proporcji
    def oblicz_dlugosci(self, punkty):
        dlugosci = []
        for wart, wart_nast in zip(punkty, punkty[1:]+[punkty[0]]):
            dlugosci.append(sqrt(pow(wart_nast[0]-wart[0], 2) + pow(wart_nast[1]-wart[1], 2)))
            
        return dlugosci

                
    #porownanie konturow
    def porownaj_dlugosci(self, dlugosci1, dlugosci2):
        stosunek = 1;
        for i in range(0, 8):
            if dlugosci1[i] >= dlugosci2[i]:
                stosunek += dlugosci2[i]/dlugosci1[i]
            else:
                stosunek += dlugosci1[i]/dlugosci2[i]
                
        return int(stosunek * 100 / 9)


#main
if __name__ == "__main__":
    pliki_dloni = ['adam1.png', 'adam2.png', 'adam3.png', 'pawel1.png', 'pawel2.png', 'pawel3.png',
                   'maciej1.png', 'maciej2.png', 'norbi1.png', 'norbi2.png', 'norbi3.png', 'oli1.png', 'oli2.png', 'oli3.png'] 

    plik_wynikowy = "D:\\PythonProjects\\rozpoznawanie_dloni\\wyniki.txt"
    sciezka_bazowa = "D:\\PythonProjects\\rozpoznawanie_dloni\\rece\\"
    
    rozpoznawacz = RozpoznawanieDloni(sciezka_bazowa, pliki_dloni, plik_wynikowy)

    rozpoznawacz.wykonaj_obliczenia()
    
    opencv.waitKey(0)
    opencv.destroyAllWindows()
