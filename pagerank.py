import random

class hemsida:
    def __init__(self, nr, namn, länkningar,d,N): 
        self.namn = namn
        self.nr = nr #Unikt nr id
        self.pageRankVärde = (1-d)/N
        self.GammaltPageRankVärde = (1-d)/N
        self.länkningar = länkningar #Lista med sidor den länkar till
        self.d = d # Dämpningsfaktor, asigneras i mainfunktionen vid initiering av varje objekt
        self.N = N #Totala antalet sidor

    def __str__(self):
        string = f'{self.namn} har PageRank-Värdet: {round(self.GammaltPageRankVärde,7)} och länkar till {len(self.länkningar)} andra sidor'
        return string
        
#Länkningar är bara en lista med massa nummer som korresponderar till sidor den är länkad till
    def länkning(self,sidlista):
        länkVärde = (self.GammaltPageRankVärde/len(self.länkningar))*self.d #Beräknar värdet av varje av sidans länkning
        for i in self.länkningar:
            sidlista[i-1].pageRankVärde += länkVärde #i-1 efterssom python har 0-indexering

    def nollställning(self): #Funktion för att nollställa mellan iterationerna
        self.GammaltPageRankVärde = self.pageRankVärde
        self.pageRankVärde = (1-self.d)/self.N


def LasInFil(filnamn, d): #Funktion för att läsa in ett "nät" från en text-fil för att köra page-rank på
    sidlista = []
    antalsidor = 0
    with open(str(filnamn),'r',encoding='utf-8',) as f:
        f.readline()
        while True: #Körs tills listan tar slut, inte jättebra sätt men fungerar
            try:
                line = f.readline()
                linelist = line.split(',')
                if len(linelist) < 3:
                    break
                
                linelist[2] = linelist[2].replace('\n','')
                länkningar = linelist[2].split(':')
                länkningar = [int(länkning) for länkning in länkningar] #Konverterar länkningar till lista av intigers
                sidlista.append(hemsida(int(linelist[0]),str(linelist[1]),länkningar,d,1))

                antalsidor += 1

            except Exception as e:
                print(e)
                break

    for sida in sidlista: #Nollställer varje sida 2 gånger för att de ska räkna med korrekt värde för N
        sida.N = antalsidor
        sida.nollställning()
        sida.nollställning()
        
    return sidlista


def skapaRandomSidor(d, N): #Fungerar knappt, rekomenderas inte
    sidlista = []
    for i in range(N):
        sidlista.append(hemsida(i,"lebronjames.com",[random.randint(1,N),random.randint(1,N),random.randint(1,N)],d,N))
    return sidlista


def kontrollSumma(sidlista):
    summa = 0
    for i in sidlista:
        summa += i.GammaltPageRankVärde
    return summa


def main():

    N = 10
    d = 0.85
    SorteraLista = True #Om True kommer sidorna med högst PageRank-Värde hamna högst upp
    
    sidlista = LasInFil("SidorExempel.txt",d)

    for i in range(1000): #Kör 1000 iterationer
        for i in sidlista:
            i.länkning(sidlista)
        for i in sidlista:
            i.nollställning()

    if SorteraLista == True:
        sidlista.sort(key=lambda sida: sida.GammaltPageRankVärde, reverse=True)
    
    for i in sidlista:
        print(i)
    print("Summan av alla PageRank-Värden är: ",kontrollSumma(sidlista)," (differansen från 1 pga. flyttalsfel)")

main()
