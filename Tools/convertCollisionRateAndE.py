__author__ = 'robert'

from gmpy2 import comb

def convert_collision_rate_to_e(collisions_per_time_step, population_size, proportion_males):
    """
    Converts the average number of collisions for one timestep to the encounter rate e
    """
    proportion_females = 1-proportion_males
    half_of_population = population_size/2
    sum = 0
    for m in range(0,population_size):
        prob_m_males = comb(population_size,m)*proportion_males**m*proportion_females**(population_size-m)
        sum += prob_m_males*abs(half_of_population-m)
    expected_number_of_min_of_males_and_females = half_of_population-sum
    e = collisions_per_time_step/expected_number_of_min_of_males_and_females
    return e


def convert_e_to_collision_rate(e, population_size, proportion_males):
    """
    Converts the the encounter rate e to average number of collisions for one timestep
    """
    proportion_females = 1-proportion_males
    half_of_population = population_size/2
    sum = 0
    for m in range(0,population_size):
        prob_m_males = comb(population_size,m)*proportion_males**m*proportion_females**(population_size-m)
        sum += prob_m_males*abs(half_of_population-m)
    expected_number_of_min_of_males_and_females = half_of_population-sum
    collisions_per_time_step = e*expected_number_of_min_of_males_and_females
    return collisions_per_time_step
"""
Example:

# population_size = 100
# proportion_males = 0.5
# proportion_females = 0.5
# sum = 0
# expected_collisions_per_time_step = 40
# e = 0.86917714622218833

print(convert_collision_rate_to_e(40, 100, 0.5))
print(convert_e_to_collision_rate(0.86917714622218833, 100, 0.5))
"""
#print(convert_collision_rate_to_e(18.759,100,0.8))
