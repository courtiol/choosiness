import math, random
import CIndividual
import alias

#Parameters of environment:

class CPopulation:
    """
    The class consists basically of two arrays: males and females
    The constructor of the class initializes these arrays with as many individuals as given by the allowed size of
    the population.
    The method check_for_mating is called when two individuals could mate in principle. When mating is possible the
    participating male and female are saved in the array couples.
    In each timestep the method update_states should be called. The method changes the states of all individuals. The
    method replaces dead individuals randomly with children of the couples array. The decision is based on luck and the
     quality of the individuals.
    """

    def __init__(self, populationSize, sex_ratio, s, latency_males, latency_females, mutation_range, mutation_rate, set_initial_position_in_the_Environment):
        """

        :param populationSize: Integer which is the maximal number of the population
        :param get_initial_position_in_the_Environment: function pointer for computing the initial positions of the
        individuals
        :return:
        """
        self.males = []
        self.females = []
        #potential parents for offspring
        #[...(male_parent, female_parent, quality_of_couple)...]
        self.couples = []
        self.maximal_number_of_saved_couples = 1000
        self.sex_ratio = sex_ratio
        self.s = s #survival rate
        self.latency_males = latency_males
        self.latency_females = latency_females
        self.populationSize = populationSize
        self.set_initial_position_in_the_Environment = set_initial_position_in_the_Environment
        self.mutation_range = mutation_range
        self.mutation_rate = mutation_rate

        self.__addIndividuals(self.populationSize)

    #choose for get_position_in_the_Environment any function that returns a touple of coordinates in the environment
    def __addIndividuals(self, n):
        """
        Adds n individuals on positions given by get_position_in_the_Environment
        :param n: number of individuals which should be added
        :param get_position_in_the_Environment: function pointer to a function that returns a position for each
         individual, i.e. has return value (x,y)
        :return:
        """
        #Add n individuals
        for i in range(n):
            individual = self.__createIndividual()
            if individual.get_gender() == CIndividual.MALE:
                self.males.append(individual)
            else:
                self.females.append(individual)


    def get_current_population_size(self):
        return len(self.males)+len(self.females)

    def get_current_males_size(self):
        return len(self.males)

    def get_current_females_size(self):
        return len(self.females)

    def __createIndividual(self):
        """
        Creates an individuals of random gender. The individual has always "mother" and "father". However they can also
        be set to "None" to circumvent problems at the beginning of the simulation.
        Two kinds of events trigger a call of this method:
        1) The populations is created
        2) Dead individuals need to be replaced
        :param get_position_in_the_Environment: Method which returns a (x,y) position
        :return: created individuals (an instance of CIndividual)
        """
        (father, mother) = self.__choose_couple()
        gender = random.random()
        if (random.random() >= self.sex_ratio):
            newIndividual = CIndividual.CIndividual(CIndividual.MALE, self.latency_males, self.mutation_range, self.mutation_rate, mother, father)
        else:
            newIndividual =  CIndividual.CIndividual(CIndividual.FEMALE, self.latency_females, self.mutation_range, self.mutation_rate, mother, father)
        self.set_initial_position_in_the_Environment(newIndividual)
        return newIndividual

    def update_states(self):
        """
        Updates the states of all individuals. Dead individuals are replaced with children obtained from the couples
        array.
        :return:
        """
        for i, male in enumerate(self.males):
            male.update_state(self.s)
            if male.state == CIndividual.DEAD:
                del self.males[i]
                self.__add_individual_of_next_generation()
        for i, female in enumerate(self.females):
            female.update_state(self.s)
            if female.state == CIndividual.DEAD:
                del self.females[i]
                self.__add_individual_of_next_generation()

    #Creates a new individual and appends it to "males" or "females"
    def __add_individual_of_next_generation(self):
        """
        Creates a new individual with the method "createIndividual". If the newly created individual is male it is
        appended to "males" otherwise it is appended to "females"
        :return:
        """
        individual = self.__createIndividual()
        if individual.get_gender() == CIndividual.MALE:
            self.males.append(individual)
        else:
            self.females.append(individual)

    def __choose_couple(self):
        """
        The method chooses randomly a couple with the alias method. This means couples with higher quality are more
        likely to be selected. The method is called when an individual is created.
        :return: element of "couples"
        """
        if len(self.couples)==0:
            print("No couple in queue => Create individual with initial values")
            return (None,None) #Vllt nochmal schauen, ob das hier wirklich so gemacht werden sollte
        else:
            #most stupid implementation since Alias is created every time even when "couples" doesn't change => ToDo. Change
            aliasMethod = alias.Alias(self.couples)
            return aliasMethod.get()
       
    #checks if two individuals mate and computes the quality of their (potential) offspring
    #The result is appended to couples
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
            a = 1/2 #weighted average of quality of the male and female
            #Compute quality of possible offspring
            quality_of_couple = male_parent.q*a+female_parent.q*(1-a)
            if len(self.couples) > self.maximal_number_of_saved_couples:
                self.__update_couple_list()
            self.couples.append(((male_parent, female_parent), quality_of_couple))

    def __update_couple_list(self):
        """
        placeholder for the case that the size of self.couples exceeds its maximal size

        In Detail: Every time a mating occurs the participating male and female are appended to the couples array.
        Therefore the array can only grow. To prevent the array from unlimited grow every time the size of couples
        exceeds the value "maximal_number_of_saved_couples" (see constructor for the assigned value) this method is
        called to prevent it from further growing.
        :return:
        """
        #self.couples = []
        self.couples = self.couples[1:] #kick oldest element

    def __str__(self):
        z = "total population: "+str(self.get_current_population_size())+"\n"
        z += "females: "+str(self.get_current_females_size())+"\n"
        z += "males: "+str(self.get_current_males_size())+"\n"
        z += "maximal number of saved couples: "+str(self.maximal_number_of_saved_couples)+"\n"
        z += "current number of couple in que: "+str(len(self.couples))+"\n"
        return z
