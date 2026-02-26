import random
import statistics

class hemsida:
    def __init__(self,nr,namn,trusted,länkningar,d,N): 
        self.namn = namn
        self.nr = nr #Unikt nr id
        self.Trusted = trusted
        self.trustRankVärde = 0
        self.pageRankVärded1 = 0 #Sparar pagerankvärde med en dämpningsfaktor
        self.pageRankVärded2 = 0 #Sparar pagerankvärde med annan dämpningsfaktor (för att upptäcka länkningsloops)
        self.ökningsFaktor = 0
        self.pageRankVärde = (1-d)/N
        self.GammaltPageRankVärde = (1-d)/N
        self.länkningar = länkningar #Lista med sidor den länkar till
        self.d = d # Dämpningsfaktor, asigneras i mainfunktionen vid initiering av varje objekt
        self.N = N #Totala antalet sidor

        #Metrik för att veta hur många av hemsidorna som länkar till den är "farm"-sidor
        #(alltså bara länkar till en hemsida för att boosta dessa PageRank-Värde)
        self.NrLänkningarFrånSidor = []
        self.TommaLänkningarMedian = 0
        self.TommaLänkningarMedelvärde = 0

    def __str__(self):
        string = f'{self.namn} har PageRank-Värdet: {round(self.GammaltPageRankVärde,7)} och länkar till {len(self.länkningar)} andra sidor och har faktorn {self.pageRankVärded2/self.pageRankVärded1}'
        return string
        
    #Länkningar är bara en lista med massa nummer som korresponderar till sidor den är länkad till
    #(från dokumentet med alla hemsidor)
    def länkning(self,sidlista):
        länkVärde = (self.GammaltPageRankVärde/len(self.länkningar))*self.d #Beräknar värdet av varje av sidans länkning
        for i in self.länkningar:
            sidlista[i-1].pageRankVärde += länkVärde #i-1 efterssom python har 0-indexering

    def nollställning(self,baraTrusted): #Funktion för att nollställa mellan iterationerna
        self.GammaltPageRankVärde = self.pageRankVärde
        if (not self.Trusted) and baraTrusted:
            self.pageRankVärde = 0
        else:
            self.pageRankVärde = (1-self.d)/self.N

    def LänkningsRäknare(self,sidlista):
        for i in self.länkningar:
            sidlista[i-1].NrLänkningarFrånSidor.append(len(self.länkningar))

    def StatistikTommaLänkningar(self):
        if len(self.NrLänkningarFrånSidor) > 0:
            self.TommaLänkningarMedelvärde = statistics.mean(self.NrLänkningarFrånSidor)
            self.TommaLänkningarMedian = statistics.median(self.NrLänkningarFrånSidor)
        print(self.namn, " har Medelvärde: ",self.TommaLänkningarMedelvärde,"  Median: ",self.TommaLänkningarMedian)


def LasInFil(filnamn, d): #Funktion för att läsa in ett "nät" från en text-fil för att köra page-rank på
    sidlista = []
    antalsidor = 0
    with open(str(filnamn),'r',encoding='utf-8',) as f:
        f.readline()
        while True: #Körs tills listan tar slut, inte jättebra sätNrLänkningarFrånSidort men fungerar
            try:
                line = f.readline()
                linelist = line.split(',')
                if len(linelist) < 4:
                    break
                
                if linelist[2]=="True":
                    trusted = True
                else:
                    trusted = False

                linelist[3] = linelist[3].replace('\n','')
                länkningar = linelist[3].split(':')
                länkningar = [int(länkning) for länkning in länkningar] #Konverterar länkningar till lista av intigers
                sidlista.append(hemsida(int(linelist[0]),str(linelist[1]),trusted,länkningar,d,1))

                antalsidor += 1

            except Exception as e:
                print(e)
                break

    for sida in sidlista: #Nollställer varje sida 2 gånger för att de ska räkna med korrekt värde för N
        sida.N = antalsidor
        sida.nollställning(False)
        sida.nollställning(False)
        
    return sidlista

def main():

    N = 10
    d = 0.85

    sidlista = LasInFil("SidorExempel.txt",d)

    for i in range(10000): #Kör 1000 iterationer av PageRank med vanlig dämpningsfaktor (ex. 0.85)
        for i in sidlista:
            i.länkning(sidlista)
        for i in sidlista:
            i.nollställning(False)
    
    for i in sidlista: #Förbereder för "anti-fusk" loopen
        i.d = 0.99
        i.pageRankVärded1 = i.GammaltPageRankVärde
        i.nollställning(False)
        i.nollställning(False)
    for i in range(10000): #Kör 1000 iterationer av PageRank med dämpningsfaktorn 0.99
        for i in sidlista:
            i.länkning(sidlista)
        for i in sidlista:
            i.nollställning(False)

    for i in sidlista:
        i.pageRankVärded2 = i.GammaltPageRankVärde

        i.ökningsFaktor = (lambda f: max(f, 1/f) if f > 0 else float('inf'))(i.pageRankVärded2 / i.pageRankVärded1) #Hittar faktorn som pagerankvärdet ökade/sänktes med när dämpningen höjdes

    antalTrusted = sum([int(sida.Trusted) for sida in sidlista]) #Returnerar antalet sidor som är trusted
    for i in sidlista:#
        i.N = antalTrusted #Nu är N de trusted sidorna
        i.nollställning(True)
        i.nollställning(True)
        i.d = 0.85

    for i in range(10000): #Kör 1000 iterationer av PageRank med dämpningsfaktorn 0.99
        for i in sidlista:
            i.länkning(sidlista)
        for i in sidlista:
            i.nollställning(True)

    for i in sidlista:
        i.trustRankVärde = i.GammaltPageRankVärde
    
    """
        **Teori:**
        Dämpningsfaktor finns för att "The Random Surfer" inte ska fastna i en loop med hemsidor som länkar till varandra. Den beskriver
        oddsen att surfaren byter till en helt slumpad hemsida (15% för d=0.85). Alltså, om man ökar dämpningsfaktorn till ex. 0.99
        är det bara 1% chans för surfaren att byta till en slumpad sida och därmed får "loop-kluster" (eventuella fusksidor) betydligt högre
        pagerank score efterssom "kraften" inte läker ut till andra ställen i systemet.
        
        Hur synns detta i data:
        Relativt till sitt PageRank-Värde bör faktorn för klusterhemsidorna visa att de sjunker, medan sidan de boostar ökar mycket
        relativt sätt. Man kan förfina resultaten genom att använda trustrank där man kollar vilket PageRank-Värde sidor får räknat
        utrifrån "Trusted" sidor, ex. Wikipedia, Google, Internet Archive etc.
        
    """
    sidlista.sort(key=lambda sida: sida.ökningsFaktor, reverse=True)
    
    """
    for i in sidlista:
        print(i)
    print("Summan av alla PageRank-Värden är: ",sum([sida.pageRankVärded1 for sida in sidlista])," (differansen från 1 pga. flyttalsfel)")
    print("Summan av alla 099dPageRank-Värden är: ",sum([sida.pageRankVärded2 for sida in sidlista])," (differansen från 1 pga. flyttalsfel)")
    """
    #for i in sidlista:
    #    i.StatistikTommaLänkningar()
    #    i.SurferController(sidlista,5)
main()
