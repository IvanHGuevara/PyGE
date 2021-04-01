from utils_.cythonFunctions.mapper import Mapper
#from utils_.mapper import Mapper
from utils_.grammarWrapper import GrammarWrapper
from utils_.general_functions import General_functions
from .search_operators.ga import GA
from .fitness_functions.fitness_functions import FitnessFunctions
import numpy as np

class Algorithms:

    def __init__(self, grammarPath, initBNF=1,debug=False) -> None:
        self.mapper = Mapper(GrammarWrapper.createFromFile(grammarPath))
        self.mapper.toMatrixBNF()
        self.initBNF=initBNF
        self.debug=debug
        self.gen=0

        
    def evolveWithGE(self, population):
        for _ in range(self.gen):
            evolvedIndividuals =  list(General_functions.async_map_g((lambda ind: self.mapper.mapBNF(ind.genotype,self.initBNF-1,debug=self.debug)[0]), population))
            for idx, ind in enumerate(population):
                ind.phenotype = evolvedIndividuals[idx]
        return population

    def evolveWithGE_FitnesFunction(self, population,fitness_function, gen = 1, initBNF=1,porcentSelect=0.5,estaticSelect=0):
        self.gen=gen
        evolvedIndividuals = []

        for generationNumber in range(gen):
            print("Generation: ", generationNumber)
            print("===================================================================")

            for ind in population:
                ind.phenotype=self.mapper.mapBNF(ind.genotype, initBNF - 1)[0]
                evolvedIndividuals.append(ind)
            if estaticSelect<=0:
                print("selecting individuals with a probability of: ", porcentSelect)
            else:
                print("selecting individuals : ", estaticSelect)
            individualBatch = GA.select(evolvedIndividuals,porcentSelect,estaticSelect)
            print("Grabbing a batch of: ", len(individualBatch))
            print("mutating individuals.......")
            individualBatch = list(map(lambda indG: GA.mutateInd(indG), individualBatch))
            print("generating crossover.......")
            individualBatch = GA.crossover(individualBatch, self)
            newPopulation = np.concatenate((individualBatch, population))
            print("reevaluate new population")
            newPopulation = list(map(lambda ind: GA.evaluate(ind, fitness_function), newPopulation))
            #individualBatch = sorted(enumerate(individualBatch), key= lambda ind: (fitness_function(ind[1],ind[0]+1,len(individualBatch)).fitness_score,len(ind[1].phenotype)), reverse=True)
            newPopulation = sorted(newPopulation, key=lambda ind: ind.fitness_score, reverse=True)

            print("===================================================================")
            population = newPopulation

        return population