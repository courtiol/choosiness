import random
import CChromosome
from Tools.usefulDecorators import printAllParameters

# constants:
ALIVE = 0
DEAD = 1
IN_LATENCY = 2
MALE = 1
FEMALE = 0

INITIAL_CHROMOSOME = [(0, False), (0.0, True), (0, False), (0.0, True)]

class CIndividual:
    """
    The class represents one individual in the simulation. Each individual has different states and
    can be created by its "parents". The inheritable information of each individual is saved in a pair of
    chromosomes.
    """
    def __init__(self, gender, latency, mutation_range, mutation_rate, survival_prob, mother=None, father=None):
        """

        :type self: object
        """
        self.state = ALIVE  # possible states: alive, dead, in_latency
        self.gender = gender
        self.s = survival_prob

        if mother is None or father is None:
            # 4 loci are needed (phi_a_male, phi_b_male, phi_a_female, phi_b_female)
            # each chromosome stores all loci
            self.ch1 = CChromosome.CChromosome(mutation_range, mutation_rate, list(INITIAL_CHROMOSOME))
            self.ch2 = CChromosome.CChromosome(mutation_range, mutation_rate, list(INITIAL_CHROMOSOME))
        else:
            # random segregation as if loci where independent (on different chromosomes)
            self.ch1 = mother.ch1 + mother.ch2
            self.ch2 = father.ch1 + father.ch2
            self.ch1.mutate()
            self.ch2.mutate()
        self.l = latency  # latency #change
        self.q = random.uniform(0, 1)  # ToDo: correct?
        self._express_genes()

    def _express_genes(self):
        """
        computes the parameter phi
        :return:
        """
        if self.gender == MALE:
            phi_a_ch1 = self.ch1.loci[0][0]  # extract first element of the tuple (so not the "evolve" information)
            phi_a_ch2 = self.ch2.loci[0][0]
            phi_b_ch1 = self.ch1.loci[1][0]
            phi_b_ch2 = self.ch2.loci[1][0]
        else:
            phi_a_ch1 = self.ch1.loci[2][0]
            phi_a_ch2 = self.ch2.loci[2][0]
            phi_b_ch1 = self.ch1.loci[3][0]
            phi_b_ch2 = self.ch2.loci[3][0]
        self.phi = ((phi_a_ch1 + phi_a_ch2) * self.q + phi_b_ch1 + phi_b_ch2) / 2

    def update_state(self):
        """
         Changes the states of the individuals according to their transition probabilities.
        :param s: survival probability
        :return:
        """
        if random.random() > self.s:  # 1-s is the probability to die in one time step
            self.state = DEAD
        elif self.state == IN_LATENCY and random.random() > self.l:
            self.state = ALIVE

    def accepts_for_mating(self, other_sex):
        """
        Check if an individual accepts an opposite sex individual as mating partner.
        :param other_sex:
        :return: True/False
        """
        if self.state == IN_LATENCY:
            return False
        if self.phi > other_sex.q:
            return False
        else:
            return True

    def mate(self):
        # In latency after mating but latency can be remove by update so latency probability
        # is the same at the mating step as for other states
        self.state = IN_LATENCY

    @printAllParameters
    def __str__(self):
        return ""
