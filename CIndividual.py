import math, random
import CChromosome

#constants:
ALIVE = True #We try to code states as boolean using "None" as the third state (ternary coding)
DEAD = False
IN_LATENCY = None
MALE = True
FEMALE = False

class CIndividual:
    """
    The class represents one individual in the simulation. Each individual has different states and
    can be created by its "parents". The inheritable information of each individual is saved in a pair of
    chromosomes.
    """
    
    def __init__(self, gender, latency, mutation_range, mutation_rate, mother=None, father=None):
        self.state = ALIVE #possible states: alive, dead, in_latency
        self.gender = gender

        if mother == None or father == None:
            #4 loci are needed
            self.ch1 = CChromosome.CChromosome(mutation_range, mutation_rate, [(0,False),(0.5,True),(0,False),(0.5,True)]) #each chromosome stores all loci
            self.ch2 = CChromosome.CChromosome(mutation_range, mutation_rate, [(0,False),(0.5,True),(0,False),(0.5,True)])
        else:
            self.ch1 = mother.ch1+mother.ch2 #random segregation as if loci where independent (on different chromosomes)
            self.ch2 = father.ch1+father.ch2
        
        self.l = latency #latency #change
        self.q = random.uniform(0,1) #correct?
        self.__expressGenes()

    def __expressGenes(self):
        """
        computes the parameter phi
        :return:
        """
        if self.gender == MALE:
            phi_a_ch1 = self.ch1.loci[0][0] #extract first element of the tuple (so not the "evolve" information)
            phi_a_ch2 = self.ch2.loci[0][0]
            phi_b_ch1 = self.ch1.loci[1][0]
            phi_b_ch2 = self.ch2.loci[1][0]
        else:
            phi_a_ch1 = self.ch1.loci[2][0]
            phi_a_ch2 = self.ch2.loci[2][0]
            phi_b_ch1 = self.ch1.loci[3][0]
            phi_b_ch2 = self.ch2.loci[3][0]
        self.phi = ((phi_a_ch1+phi_a_ch2)*self.q+phi_b_ch1+phi_b_ch2)/2

    def getGender(self):
        return self.gender

    def update_state(self, s):
        """
         Changes the states of the individuals according to their transition probabilities.
        :param s: survival probability
        :return:
        """
        if random.random() > s: #1-s is the probability to die in one timestep
            self.state = DEAD
        elif self.state == IN_LATENCY and random.random() > self.l:
            self.state = ALIVE

    def accepts_for_mating(self, other_sex):
        """
        Check if an individual accepts an opposite sex individual as mating partiner.
        :param other_sex:
        :return: True/False
        """
        if self.state == IN_LATENCY:
            return False
        if self.phi > other_sex.q:
            return False
        else:
            return True

    def mate(self, other_sex):
        self.state = IN_LATENCY #In latency after mating but latency can be remove by update so latency proba is the same at the mating step as for other states

    def __str__(self):
        str_n = "Chromosome 1:\n"+str(self.ch1)
        str_n += "Chromosome 2:\n"+str(self.ch2)
        str_n += "choosiness: "+str(self.phi)+"\n"
        str_n += "quality: "+str(self.q)+"\n"
        return str_n

