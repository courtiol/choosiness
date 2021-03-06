import random
import CIndividual
import alias
from Tools.usefulDecorators import measure_percentage_of_time

ARITHMETIC_MEAN = 0
GEOMETRIC_MEAN = 1

class CBasePopulation():
    """
    The following methods need to be implemented, in order to ensure compatibility with the simulation.
    """
    def update_states(self):
        pass

    def check_for_mating(self, male_parent, female_parent):
        pass

    @property
    def current_population_size(self):
        return len(self.males)+len(self.females)

    @property
    def current_number_of_males(self):
        return len(self.males)

    @property
    def current_number_of_females(self):
        return len(self.females)

# --------------------------------------------------------------------------------------------------------------


class CPopulation(CBasePopulation):
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
    def __init__(self, population_size, sex_ratio, a, type_of_average,  maximal_number_of_saved_couples,
                 set_initial_position_in_the_environment,
                 classType_of_male_individual : CIndividual.CBaseIndividual,
                 classType_of_female_individual : CIndividual.CBaseIndividual, classType_settings):
        """
        Initializes a population.
        :param population_size: Integer which is the maximal number of the population
        :param sex_ratio: ratio between the sexes
        :param female_individual_settings: settings of female individuals in the population
        :param male_individual_settings: settings of male individuals in the population
        :param set_initial_position_in_the_environment: function handler for a function which determines the initial
        position of a new individual in the environment
        :return:
        """
        self.males = []
        self.females = []
        # potential parents for offspring
        # [...(male_parent, female_parent, quality_of_couple)...]
        self.couples = []
        self.maximal_number_of_saved_couples = maximal_number_of_saved_couples
        self.sex_ratio = sex_ratio

        self.male_settings = classType_settings['classType_of_male_individual']
        self.female_settings = classType_settings['classType_of_female_individual']
        self.classType_of_female_individual = classType_of_male_individual
        self.classType_of_male_individual = classType_of_female_individual

        self.populationSize = population_size
        self.set_initial_position_in_the_environment = set_initial_position_in_the_environment
        self.a = a  # weighted average for the quality of the offspring
        self.type_of_average = type_of_average  # ARITHMETIC_MEAN / GEOMETRIC_MEAN

        # Add individuals to population
        # Set in_initialization to True to allow creating individuals from couples of the form (None, None)
        # For details look in the method "_create_individual"
        self.in_initialization = True
        self.alias_method = None  # initialize alias method
        self._add_individuals(self.populationSize)
        self.in_initialization = False

    # choose for get_position_in_the_Environment any function that returns a tuple of coordinates in the environment
    def _add_individuals(self, n):
        """
        ToDo: add
        Adds n individuals on positions given by get_position_in_the_Environment
        :param n: number of individuals which should be added
        :return:
        """
        # Add n individuals
        for _ in range(n):
            individual = self._create_individual()
            # if for whatever reason there could no individual be created (e.g. no couple in the queue), skip the step
            # This happens if the queue of couples is empty and the class is not anymore in the initialization mode
            if individual is None:
                # Here could be also written return. However for future use if the filling of the couples array runs
                # parallel it is more reasonable to use continue, since the couples array could be filled up during
                # execution of this step.
                # print("Couples array was empty. No individual added.")
                continue
            if individual.gender == CIndividual.MALE:
                self.males.append(individual)
            else:
                self.females.append(individual)

    @property
    def current_population_size(self):
        return len(self.males)+len(self.females)

    @property
    def current_number_of_males(self):
        return len(self.males)

    @property
    def current_number_of_females(self):
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
        # if no couple could be found and we are not anymore in the initialization step return none
        if not self.in_initialization and father is None and mother is None:
            return None
        if random.random() >= self.sex_ratio:
            self.male_settings['mother'] = mother
            self.male_settings['father'] = father
            new_individual = self.classType_of_male_individual(**self.male_settings)
        else:
            self.female_settings['mother'] = mother
            self.female_settings['father'] = father
            new_individual = self.classType_of_female_individual(**self.female_settings)
        self.set_initial_position_in_the_environment(new_individual)
        return new_individual

    @measure_percentage_of_time
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
        for i, female in enumerate(self.females):
            female.update_state()
            if female.state == CIndividual.DEAD:
                del self.females[i]
        # Fill up the population again
        number_of_new_individuals = self.populationSize-self.current_population_size
        # update alias method since since the last call the couples changed
        if len(self.couples) > 0:
            self.alias_method = alias.Alias(self.couples)
        else:
            self.alias_method = None
        self._add_individuals(number_of_new_individuals)

        # check if there are still individuals alive
        if self.current_population_size == 0:
            raise Exception("The population died out")

    def _choose_couple(self):
        """
        The method chooses randomly a couple with the alias method. This means couples with higher quality are more
        likely to be selected. The method is called when an individual is created.
        :return: element of "couples"
        """
        if len(self.couples) == 0:
            return None, None
        else:
            return self.alias_method.get()
       
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
                raise Exception("Unknown type of average")
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
               current number of couple in que: {4}\n""".format(self.current_population_size,
               self.current_number_of_females, self.current_number_of_males, self.maximal_number_of_saved_couples,
               len(self.couples))


# -------------------------------------slightly different implementation---------------------------------------------------------
class CPopulationImmediateFlush(CPopulation, CBasePopulation):
    """
    The couples array is not kept over several birth cycles here. After each refilling of the males and females it is
    set again to an emtpy list. This corresponds to the reference implementation.
    Keep care that the

    """
    def update_states(self):
        CPopulation.update_states(self)
        self.couples = []  # empty couples array

    def _update_couple_list(self):
        pass  # this method is not necessary anymore