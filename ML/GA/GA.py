import random
from datetime import datetime, timedelta

class Exam:
    def __init__(self, course_name, teacher_name, duration):
        self.course_name = course_name
        self.teacher_name = teacher_name
        self.duration = duration
        self.time_slot = None  # Assigned later

class GA:
    def __init__(self, exams, start_date, max_days, slots_per_day, max_hours_per_day, population_size, crossover_rate, mutation_rate, max_generations):
        self.exams = exams
        self.start_date = start_date
        self.max_days = max_days
        self.slots_per_day = slots_per_day
        self.max_hours_per_day = max_hours_per_day
        self.population_size = population_size
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.max_generations = max_generations
        self.population = []
        self.best_schedule = None

    def initialize_population(self):
        for _ in range(self.population_size):
            schedule = []
            for exam in self.exams:
                day = random.randint(1, self.max_days)
                slot = random.randint(1, self.slots_per_day)
                schedule.append((exam, day, slot))
            self.population.append(schedule)

    def fitness(self, schedule):
        conflicts = 0
        hours_used = [0] * self.max_days

        for exam, day, slot in schedule:
            # Check daily hour constraints
            if hours_used[day - 1] + exam.duration > self.max_hours_per_day:
                conflicts += 1  # Exceeding daily hours adds a penalty
            else:
                hours_used[day - 1] += exam.duration

        # Check for slot conflicts
        time_slots = {}
        for exam, day, slot in schedule:
            if (day, slot) not in time_slots:
                time_slots[(day, slot)] = [exam]
            else:
                time_slots[(day, slot)].append(exam)
                conflicts += 1

        return 1 / (1 + conflicts)

    def select_parent(self):
        total_fitness = sum(self.fitness(schedule) for schedule in self.population)
        pick = random.uniform(0, total_fitness)
        current = 0
        for schedule in self.population:
            current += self.fitness(schedule)
            if current >= pick:
                return schedule

    def crossover(self, parent1, parent2):
        if random.random() < self.crossover_rate:
            point = random.randint(0, len(parent1) - 1)
            child1 = parent1[:point] + parent2[point:]
            child2 = parent2[:point] + parent1[point:]
            return child1, child2
        return parent1, parent2

    def mutate(self, schedule):
        if random.random() < self.mutation_rate:
            idx = random.randint(0, len(schedule) - 1)
            day = random.randint(1, self.max_days)
            slot = random.randint(1, self.slots_per_day)
            schedule[idx] = (schedule[idx][0], day, slot)
        return schedule

    def run(self):
        self.initialize_population()
        for generation in range(self.max_generations):
            new_population = []
            for _ in range(self.population_size // 2):
                parent1 = self.select_parent()
                parent2 = self.select_parent()
                child1, child2 = self.crossover(parent1, parent2)
                child1 = self.mutate(child1)
                child2 = self.mutate(child2)
                new_population.extend([child1, child2])
            self.population = new_population
            self.best_schedule = max(self.population, key=self.fitness)

    def display_schedule(self):
        schedule = sorted(self.best_schedule, key=lambda x: (x[1], x[2]))
        start_date = datetime.strptime(self.start_date, "%Y-%m-%d")
        day_hours = [0] * self.max_days  # Tracks hours used per day

        for exam, day, slot in schedule:
            exam_date = start_date + timedelta(days=day - 1)
            day_hours[day - 1] += exam.duration

            print(
                f"Date: {exam_date.strftime('%Y-%m-%d')}, Slot: {slot}, "
                f"Exam: {exam.course_name} by {exam.teacher_name}, Duration: {exam.duration} hours"
            )
        
        # Display total hours used per day
        print("\nDaily Hours Used:")
        for day, hours in enumerate(day_hours, start=1):
            exam_date = start_date + timedelta(days=day - 1)
            print(f"Date: {exam_date.strftime('%Y-%m-%d')}, Total Hours: {hours}/{self.max_hours_per_day}")


exams = [
    Exam("Math", "Dr. Smith", 2),
    Exam("Physics", "Dr. Brown", 3),
    Exam("Chemistry", "Dr. White", 2),
    Exam("Biology", "Dr. Green", 1),
    Exam("English", "Dr. Black", 1.5),
    Exam("History", "Dr. Gray", 2),
    Exam("Geography", "Dr. Blue", 1),
    Exam("Economics", "Dr. Red", 2),
    Exam("Computer Science", "Dr. Purple", 3),
    Exam("Art", "Dr. Pink", 1),
    Exam("Music", "Dr. Orange", 2),
]

ga = GA(
    exams=exams,
    start_date="2024-12-18",  # Start date for the schedule
    max_days=5,              # Maximum days for the exams
    slots_per_day=4,         # Number of slots per day
    max_hours_per_day=6,     # Maximum hours per day
    population_size=50,
    crossover_rate=0.8,
    mutation_rate=0.1,
    max_generations=100
)

ga.run()
ga.display_schedule()