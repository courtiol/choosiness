import random
import CIndividual
import alias

# Parameters of environment:

ARITHMETIC_MEAN = 0
GEOMETRIC_MEAN = 1

class CPopulation:
    """
    The class consists basically of two arrays: males and females
    The constructor of the class initializes these arrays with as many individuals as given by the allowed size of
    the population.
    The method check_for_mating is called when two individuals could mate in principle. When mating is possible the
    participating male and female are saved in the array couples.
    In each time step the method update_states should be called. The method changes the states of all individuals. The
    method replaces dead individuals randomly with children of the couples array. The decision is based on luck and the
     quality of the individuals.
    """

    def __init__(self, population_size, sex_ratio, s_males, s_females, latency_males,
                 latency_females, mutation_range, mutation_rate, a, type_of_average, set_initial_position_in_the_environment):
        """
        Initializes a population.
        :param population_size: Integer which is the maximal number of the population
        :param s_males: survival prob. of males for a time step
        :param s_females: survival prob. of females for a time step
        :param sex_ratio: ratio between the sexes
        :param latency_males: prob. to remain in latency of males after reproduction
        :param latency_females: prob. to remain in latency of females after reproduction
        :param mutation_range: effect of one mutation / possible range of change in one mutation
        :param mutation_rate: frequency of mutations
        :param set_initial_position_in_the_environment: function handler for a function which determines the initial
        position of a new individual in the environment
        :return:
        """
        self.males = []
        self.females = []
        # potential parents for offspring
        # [...(male_parent, female_parent, quality_of_couple)...]
        self.couples = []
        self.maximal_number_of_saved_couples = 1000
        self.sex_ratio = sex_ratio
        self.s_males = s_males  # survival rate of males
        self.s_females = s_females  # survival rate of males
        self.latency_males = latency_males
        self.latency_females = latency_females
        self.populationSize = population_size
        self.set_initial_position_in_the_environment = set_initial_position_in_the_environment
        self.mutation_range = mutation_range
        self.mutation_rate = mutation_rate
        self._add_individuals(self.populationSize)
        self.a = a #weighted average for the quality of the offspring
        self.type_of_average = type_of_average # ARITHMETIC_MEAN / GEOMETRIC_MEAN

    # choose for get_position_in_the_Environment any function that returns a tuple of coordinates in the environment
    def _add_individuals(self, n):
        """
        ToDo: add
        Adds n individuals on positions given by get_position_in_the_Environment
        :param n: number of individuals which should be added
        :return:
        """
        # Add n individuals
        for i in range(n):
            individual = self._create_individual()
            if individual.gender == CIndividual.MALE:
                self.males.append(individual)
            else:
                self.females.append(individual)

    @property
    def current_population_size(self):
        return len(self.males)+len(self.females)

    @property
    def current_males_size(self):
        return len(self.males)

    @property
    def current_females_size(self):
        return len(self.females)

    def _create_individual(self):
        """
        Creates an individuals of random gender. The individual has always "mother" and "father". However they can also
        be set to "None" to circumvent problems at the beginning of the simulation.
        Two kinds of events trigger a call of this method:
        1) The populations is created
        2) Dead individuals need to be replaced
        :return: created individuals (an instance of CIndividual)
        """
        (father, mother) = self._choose_couple()
        if random.random() >= self.sex_ratio:
            new_individual = CIndividual.CIndividual(gender=CIndividual.MALE, latency=self.latency_males,
                                                     mutation_range=self.mutation_range,
                                                     mutation_rate=self.mutation_rate, survival_prob=self.s_males,
                                                     mother=mother, father=father)
        else:
            new_individual = CIndividual.CIndividual(gender=CIndividual.FEMALE, latency=self.latency_females,
                                                     mutation_range=self.mutation_range,
                                                     mutation_rate=self.mutation_rate, survival_prob=self.s_females,
                                                     mother=mother, father=father)
        self.set_initial_position_in_the_environment(new_individual)
        return new_individual

    def update_states(self):
        """
        Updates the states of all individuals. Dead individuals are replaced with children obtained from the couples
        array.
        :return:
        """
        for i, male in enumerate(self.males):
            male.update_state()
            if male.state == CIndividual.DEAD:
                del self.males[i]
                self._add_individual_of_next_generation()
        for i, female in enumerate(self.females):
            female.update_state()
            if female.state == CIndividual.DEAD:
                del self.females[i]
                self._add_individual_of_next_generation()

    # Creates a new individual and appends it to "males" or "females"
    def _add_individual_of_next_generation(self):
        """
        Creates a new individual with the method "createIndividual". If the newly created individual is male it is
        appended to "males" otherwise it is appended to "females"
        :return:
        """
        individual = self._create_individual()
        if individual.gender == CIndividual.MALE:
            self.males.append(individual)
        else:
            self.females.append(individual)

    def _choose_couple(self):
        """
        The method chooses randomly a couple with the alias method. This means couples with higher quality are more
        likely to be selected. The method is called when an individual is created.
        :return: element of "couples"
        """
        if len(self.couples) == 0:
            print("No couple in queue => Create individual with initial values")
            return None, None  # ToDo: Better possible //
            #  ToDo ALEX: No, you should keep these places free and fill them up later on!!
        else:
            # most stupid implementation since Alias is created every time even when "couples"
            # doesn't change => ToDo. Change
            alias_method = alias.Alias(self.couples)
            return alias_method.get()
       
    # checks if two individuals mate and computes the quality of their (potential) offspring
    # The result is appended to couples
    def check_for_mating(self, male_parent, female_parent):
        """
        Checks if two individuals mate and computes the quality of their (potential) offspring
        The result is appended to couples.

        In detail: Whenever a collision occurs or in general a mating is possible, this method is called.
        The method checks if the male accepts the female as mating partner and vice versa. If this is the case
        the couple is saved together with the quality of their offspring in the array self.couples.
        :param male_parent: male of class CIndividual
        :param female_parent: female of class CIndividual
        :return:
        """
        if male_parent.accepts_for_mating(female_parent) and female_parent.accepts_for_mating(male_parent):
            male_parent.mate()
            female_parent.mate()
            # Compute quality of possible offspring
            if self.type_of_average == ARITHMETIC_MEAN:
                quality_of_couple = male_parent.q*self.a+female_parent.q*(1-self.a)
            elif self.type_of_average == GEOMETRIC_MEAN:
                quality_of_couple = male_parent.q**self.a * female_parent.q**(1-self.a)
            else:
                print("You did not choose a correct value for the type of average in the constructor.")
            if len(self.couples) > self.maximal_number_of_saved_couples:
                self._update_couple_list()
            self.couples.append(((male_parent, female_parent), quality_of_couple))

    def _update_couple_list(self):
        """
        This method is a placeholder for the case that the size of self.couples exceeds its maximal size

        In Detail: Every time a mating occurs the participating male and female are appended to the couples array.
        Therefore the array can only grow. To prevent the array from unlimited grow every time the size of couples
        exceeds the value "maximal_number_of_saved_couples" (see constructor for the assigned value) this method is
        called to prevent it from further growing.
        :return:
        """
        # self.couples = []
        self.couples = self.couples[1:]  # kick oldest element

    def __str__(self):
        return """total population: {0}\nfemales: {1}\nmales: {2}\nmaximal number of saved couples: {3}\n
        current number of couple in que: {4}\n""".format(self.current_population_size(),
        self.current_females_size(), self.current_males_size(), self.maximal_number_of_saved_couples(),
        len(self.couples))