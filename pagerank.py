import statistics

class hemsida:
    def __init__(self,nr,namn,trusted,länkningar): 
        self.namn = namn
        self.nr = nr #Unikt nr id
        self.Trusted = trusted

        #Temporära värden som används vid beräkningen av pagerank
        self.pageRankVärde = 0
        self.GammaltPageRankVärde = 0


        self.länkningar = länkningar #Lista med sidor den länkar till


        #Värdena som används för att lista ut om en sida är "sussy" eller inte (om det är en fuskhemsida)
        self.pageRankVärded1 = 0
        self.pageRankVärded2 = 0
        self.ökningsFaktor = 0
        self.trustRankVärde = 0
        self.susVärde = 0
        
    #Länkningar är bara en lista med massa nummer som korresponderar till sidor den är länkad till
    #(från dokumentet med alla hemsidor)
    def länkning(self,sidlista,d):
        länkVärde = (self.GammaltPageRankVärde/len(self.länkningar))*d #Beräknar värdet av varje av sidans länkning
        for i in self.länkningar:
            sidlista[i-1].pageRankVärde += länkVärde #i-1 efterssom python har 0-indexering

    def nollställning(self,baraTrusted,d,N): #Funktion för att nollställa mellan iterationerna
        self.GammaltPageRankVärde = self.pageRankVärde
        if (not self.Trusted) and baraTrusted:
            self.pageRankVärde = 0
        else:
            self.pageRankVärde = (1-d)/N

def iteration(iterationer,sidlista,d,baraTrusted):
    if baraTrusted:
        N = sum([int(sida.Trusted) for sida in sidlista])
    else:
        N = len(sidlista)
    for sida in sidlista:
        sida.nollställning(baraTrusted,d,N)
        sida.nollställning(baraTrusted,d,N)
    for i in range(iterationer):
        for sida in sidlista:
            sida.länkning(sidlista,d)
        for sida in sidlista:
            sida.nollställning(baraTrusted,d,N)

    returnLista = []
    for sida in sidlista:
        returnLista.append([sida.namn,sida.GammaltPageRankVärde])
    return returnLista


def ökningsfaktor(pageRankVärded1, pageRankVärded2):
    returnLista = []
    for n in range(len(pageRankVärded1)):
        returnLista.append([pageRankVärded1[0],(lambda f: max(f, 1/f) if f > 0 else float('inf'))(pageRankVärded1[n][1] / pageRankVärded2[n][1])])
        #Hittar faktorn som pagerankvärdet ökade/sänktes med när dämpningen höjdes
    return returnLista

def susVärde(ökningsFaktorLista,trustRankVärdeLista,golv):
    returnLista = []
    medelTrustRank = statistics.mean([sida[1] for sida in trustRankVärdeLista])

    for n in range(len(ökningsFaktorLista)):
        returnLista.append([ökningsFaktorLista[0],medelTrustRank/(trustRankVärdeLista[n][1] + golv)*ökningsFaktorLista[n][1]])
    return returnLista


def LasInFil(filnamn): #Funktion för att läsa in ett "nät" från en text-fil för att köra page-rank på
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
                sidlista.append(hemsida(int(linelist[0]),str(linelist[1]),trusted,länkningar))

                antalsidor += 1

            except Exception as e:
                print(e)
                break
        
    return sidlista

def main():
    sidlista = LasInFil("SidorExempel.txt")
    
    #Får alla nödvändiga värden för varje sida
    pageRankd085 = iteration(200,sidlista,0.85,False)
    pageRankd099 = iteration(200,sidlista,0.99,False)
    ökningsFaktorLista = ökningsfaktor(pageRankd085,pageRankd099)
    trustRankVärdeLista = iteration(200,sidlista,0.85,True)

    #Beräknar sus-värdet, golvet beslutar hur mycket trustrank-värdet påverkar värdet
    #Ju lägre golv, desto mer påverkar trustrank-värdet för en sida
    golv = 0.00001
    susVärdeLista = susVärde(ökningsFaktorLista,trustRankVärdeLista,golv)

    #Assignerar alla värdena till objekten i sidlista
    for n in range(len(sidlista)):
        sida = sidlista[n]
        sida.pageRankVärded1 = pageRankd085[n][1]
        sida.pageRankVärded2 = pageRankd099[n][1]
        sida.trustRankVärde = trustRankVärdeLista[n][1]
        sida.ökningsFaktor = ökningsFaktorLista[n][1]
        sida.susVärde = susVärdeLista[n][1]
    
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
    sidlista.sort(key=lambda sida: sida.susVärde, reverse=True)

    for sida in sidlista:
        print(f'{sida.namn} har Sus-Värdet: {sida.susVärde} och har faktorn {sida.ökningsFaktor} och har trustrankvärdet {sida.trustRankVärde}')  
main()