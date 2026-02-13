import random

class hemsida:
    def __init__(self, nr, namn, länkningar,d,N): 
        self.namn = namn
        self.nr = nr
        self.pageRankVärde = (1-d)/N
        self.GammaltPageRankVärde = (1-d)/N
        self.länkningar = länkningar
        self.d = d
        self.N = N

    def __str__(self):
        string = f'{self.namn} har PageRank-Värdet: {round(self.GammaltPageRankVärde,5)} och länkar till {len(self.länkningar)} andra sidor'
        return string

        
#Länkningar är bara en lista med massa nummer som korresponderar till sidor den är länkad till
    def länkning(self,sidlista): 
        for i in self.länkningar:
            sidlista[i-1].pageRankVärde += (self.GammaltPageRankVärde/len(self.länkningar))*self.d

    def nollställning(self):
        self.GammaltPageRankVärde = self.pageRankVärde
        self.pageRankVärde = (1-self.d)/self.N

def LasInFil(filnamn, d):
    sidlista = []
    antalsidor = 0
    print("läs in från fil startad")
    with open(str(filnamn),'r',encoding='utf-8',) as f:
        f.readline()
        while True:
            try:
                line = f.readline()
                linelist = line.split(',')
                if len(linelist) < 3:
                    break
                
                linelist[2] = linelist[2].replace('\n','')
                länkningar = linelist[2].split(':')
                länkningar = [int(länkning) for länkning in länkningar]
                sidlista.append(hemsida(int(linelist[0]),str(linelist[1]),länkningar,d,1))

                antalsidor += 1

            except Exception as e:
                print(e)
                break

    for i in sidlista:
        i.N = antalsidor
        i.nollställning()
        i.nollställning()
        
    return sidlista

def skapaRandomSidor(d, N):
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
    
    sidlista = LasInFil("test.txt",d)

    for i in range(1000):
        for i in sidlista:
            i.länkning(sidlista)
        for i in sidlista:
            i.nollställning()

    for i in sidlista:
        print(i)
    print("Summan av alla PageRank-Värden är: ",kontrollSumma(sidlista))

main()
