import random

class hemsida:
    def __init__(self, nr, namn, initPageRankVärde, länkningar,d,N): 
        self.namn = namn
        self.nr = nr
        self.pageRankVärde = 0
        self.GammaltPageRankVärde = initPageRankVärde
        self.länkningar = länkningar
        self.d = d
        self.N = N

    def __str__(self):
        return str(self.GammaltPageRankVärde)

        
#Länkningar är bara en lista med massa nummer som korresponderar till sidor den är länkad till
    def länkning(self,sidlista): 
        for i in self.länkningar:
            sidlista[i].pageRankVärde += (self.GammaltPageRankVärde/len(self.länkningar))*self.d

    def nollställning(self):
        self.GammaltPageRankVärde = self.pageRankVärde
        #print(self.GammaltPageRankVärde)
        self.pageRankVärde = (1-self.d)/self.N


def main():

    N = 100
    d = 0.85
    
    sidlista = []
    for i in range(N):
        sidlista.append(hemsida(i,"lebronjames.com",(1-d)/N,[random.randint(1,N-1),random.randint(1,N-1),random.randint(1,N-1)],d,N))


    for i in range(100):
        for i in sidlista:
            i.länkning(sidlista)
        for i in sidlista:
            i.nollställning()

    for i in sidlista:
        print(i)

main()
