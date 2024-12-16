# create GA algrithm to solve the problem of scheduling the exam of the students for the university with multiple constraints

import random
import numpy as np
import copy
import math
import matplotlib.pyplot as plt
import time
import csv
import seaborn as sns
import pandas as pd


# define the class of the exam
class Exam:
    def __init__(self, id, time, students):
        self.id = id
        self.time = time
        self.students = students

# define the class of the chromosome
class Chromosome:
    def __init__(self, exams, conflicts):
        self.exams = exams
        self.conflicts = conflicts
        self.fitness = 0

# define the class of the GA

class GA:
    def __init__(self, population_size, crossover_rate, mutation_rate, max_generation, data):
        self.population_size = population_size
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.max_generation = max_generation
        self.data = data
        self.exams = []
        self.students = []
        self.conflicts = []
        self.population = []
        self.best_chromosome = None
        self.best_fitness = 0
        self.avg_fitness = []
        self.best_fitnesses = []
        self.avg_fitnesses = []
        self.conflict_rate = []
        self.conflict_rates = []
        self.time = 0

    # read the data from the file
    def read_data(self):
        with open(self.data, 'r') as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip().split()
                print(line)
                # print(line[0])
                if line[0] == 'Exam':
                    id = int(line[1])
                    time = int(line[2])
                    students = list(map(int, line[3:]))
                    exam = Exam(id, time, students)
                    self.exams.append(exam)
                elif line[0] == 'Student':
                    student = list(map(int, line[1:]))
                    self.students.append(student)
                elif line[0] == 'Conflict':
                    conflict = list(map(int, line[1:]))
                    self.conflicts.append(conflict)

    def visualize_schedule_ga(best_chromosome, conflicts, num_time_slots=10):
        # Extract exam schedule and conflicts
        exam_schedule = [exam.time for exam in best_chromosome.exams]  # Extract assigned time slots
        num_exams = len(exam_schedule)
        
        # Gantt Chart for Scheduling
        plt.figure(figsize=(12, 8))
        for i, exam_time in enumerate(exam_schedule):
            plt.barh(i, 1, left=exam_time - 1, color="skyblue")  # Subtract 1 to align time slots with 0-indexed axis
        
        plt.title("Exam Scheduling Gantt Chart", fontsize=16)
        plt.xlabel("Time Slots", fontsize=12)
        plt.ylabel("Exams", fontsize=12)
        plt.yticks(range(num_exams), [f"Exam {i + 1}" for i in range(num_exams)])
        plt.grid(axis="x", linestyle="--", alpha=0.7)
        plt.show()

        # Conflict Heatmap
        # Create a matrix to represent conflicts
        conflict_matrix = np.zeros((num_exams, num_exams))
        for conflict in conflicts:
            conflict_matrix[conflict[0] - 1][conflict[1] - 1] = 1
            conflict_matrix[conflict[1] - 1][conflict[0] - 1] = 1  # Symmetric
        
        plt.figure(figsize=(10, 8))
        sns.heatmap(conflict_matrix, cmap="Reds", annot=True, cbar=False, linewidths=0.5)
        plt.title("Conflict Heatmap", fontsize=16)
        plt.xlabel("Exams", fontsize=12)
        plt.ylabel("Exams", fontsize=12)
        plt.show()

    
    # create the initial population
    def create_population(self):
        for i in range(self.population_size):
            exams = []
            for exam in self.exams:
                exams.append(random.randint(1, 10))
            chromosome = Chromosome(exams, self.conflicts)
            self.population.append(chromosome)

    # calculate the fitness of the chromosome
    def calculate_fitness(self, chromosome):
        conflicts = 0
        for conflict in chromosome.conflicts:
            if chromosome.exams[conflict[0] - 1] == chromosome.exams[conflict[1] - 1]:
                conflicts += 1
        chromosome.fitness = 1 / (1 + conflicts)
        return chromosome.fitness
    
    # calculate the fitness of the population
    def calculate_population_fitness(self):
        for chromosome in self.population:
            self.calculate_fitness(chromosome)

    # select the chromosome based on the roulette wheel selection
    def roulette_wheel_selection(self):
        fitness_sum = sum([chromosome.fitness for chromosome in self.population])
        rand = random.uniform(0, fitness_sum)
        current_sum = 0
        for chromosome in self.population:
            current_sum += chromosome.fitness
            if current_sum >= rand:
                return chromosome
            
    # crossover the chromosome
    def crossover(self, parent1, parent2):
        if random.random() < self.crossover_rate:
            crossover_point = random.randint(0, len(parent1.exams) - 1)
            child1 = copy.deepcopy(parent1)
            child2 = copy.deepcopy(parent2)
            for i in range(crossover_point):
                child1.exams[i] = parent2.exams[i]
                child2.exams[i] = parent1.exams[i]
            return child1, child2
        else:
            return parent1, parent2
        
    # mutation the chromosome
    def mutation(self, chromosome):
        if random.random() < self.mutation_rate:
            mutation_point = random.randint(0, len(chromosome.exams) - 1)
            chromosome.exams[mutation_point] = random.randint(1, 10)
        return chromosome
    
    # create the next generation
    def create_next_generation(self):
        next_generation = []
        while len(next_generation) < self.population_size:
            parent1 = self.roulette_wheel_selection()
            parent2 = self.roulette_wheel_selection()
            child1, child2 = self.crossover(parent1, parent2)
            child1 = self.mutation(child1)
            child2 = self.mutation(child2)
            next_generation.append(child1)
            next_generation.append(child2)
        self.population = next_generation

    # find the best chromosome
    def find_best_chromosome(self):
        for chromosome in self.population:
            if chromosome.fitness > self.best_fitness:
                self.best_chromosome = chromosome
                self.best_fitness = chromosome.fitness

    # find the average fitness of the population
    def find_avg_fitness(self):
        avg_fitness = sum([chromosome.fitness for chromosome in self.population]) / len(self.population)
        self.avg_fitness.append(avg_fitness)

    # find the conflict rate of the population
    def find_conflict_rate(self):
        conflict_rate = 1 - self.best_fitness
        self.conflict_rate.append(conflict_rate)

    # run the GA
    def run(self):
        self.read_data()
        self.create_population()
        self.calculate_population_fitness()
        self.find_best_chromosome()
        self.find_avg_fitness()
        self.find_conflict_rate()
        for i in range(self.max_generation):
            self.create_next_generation()
            self.calculate_population_fitness()
            self.find_best_chromosome()
            self.find_avg_fitness()
            self.find_conflict_rate()
        self.time = time.time()

        # Visualize Results
        self.visualize_schedule_ga(self.best_chromosome, self.conflicts)

    # plot the fitness of the population
    def plot_fitness(self):
        plt.plot(range(self.max_generation + 1), self.avg_fitness, label='Average Fitness')
        plt.plot(range(self.max_generation + 1), self.conflict_rate, label='Conflict Rate')
        plt.xlabel('Generation')
        plt.ylabel('Fitness')
        plt.legend()
        plt.show()

    # write the result to the file
    def write_result(self):
        with open('result.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Exam', 'Time'])
            for i in range(len(self.best_chromosome.exams)):
                writer.writerow([i + 1, self.best_chromosome.exams[i]])
            writer.writerow(['Time', self.time])


# visualize of scheduling the exam of the students for the university with multiple constraints 

# run the main function
if __name__ == '__main__':
    ga = GA(100, 0.8, 0.01, 100, 'data.txt')
    ga.run()
    ga.plot_fitness()
    ga.write_result()