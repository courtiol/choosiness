import random


# -------------------------------Class CChromosome-------------------------------------
class CChromosome:
    """
    Saves the inheritable information of individuals. This information is saved in an array "loci", which has the form
    [..., (locus,locus_evolves), ...]
    """

    def __init__(self, mutation_range, mutation_rate, loci=None):
        if loci is None:
            loci = []
        self.loci = loci  # has the form (locus, locus_evolves), locus is a value in [0,1]
        self.mutation_range = mutation_range  # mutation range: for details go to the method mutate
        self.mutation_rate = mutation_rate  # mutation rate: for details go to the method mutate

    def mutate(self):
        """
        Changes all genes randomly whose evolve parameter is set to true
        :return:
        """
        for i, (locus, locus_evolves) in enumerate(self.loci):
            if locus_evolves and (random.random() < self.mutation_rate):
                locus = locus + random.uniform(-1, 1) * self.mutation_range
                self.loci[i] = (locus, locus_evolves)

    # Creates a new chromosome by randomly assigning either a locus from "self" or from "other_chromosome"
    def __add__(self, other_chromosome):
        """
        Defines a + operator for chromosomes.The operator is not deterministic! The operator realizes a random
        recombination of two chromosomes.
        :param other_chromosome:
        :return:result of recombination
        """
        novi_loci = []
        for i, (locus_a, locus_a_evolves) in enumerate(self.loci):
            (locus_b, locus_b_evolves) = other_chromosome.loci[i]
            if random.random() < 0.5:
                novi_loci.append((
                    # *1 ensures that a copy of the value is made and not just a reference
                    locus_a * 1, locus_a_evolves))
            else:
                novi_loci.append((locus_b * 1, locus_b_evolves))
        new_chromosome = CChromosome(self.mutation_range, self.mutation_rate, novi_loci)
        return new_chromosome

    def __str__(self):
        n_str = ""
        for (locus, locus_evolves) in self.loci:
            n_str += str(locus) + " locus evolves? " + str(locus_evolves) + "\n"
        return n_str

# -------------------------------End of class CChromosome-------------------------------------