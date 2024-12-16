import random
import copy
import matplotlib.pyplot as plt

# تعریف کلاس امتحان
class Exam:
    def __init__(self, course_name, teacher_name, duration):
        self.course_name = course_name
        self.teacher_name = teacher_name
        self.duration = duration
        self.time_slot = None  # تعیین زمان امتحان

# تعریف کلاس الگوریتم ژنتیک
class GA:
    def __init__(self, exams, max_days, slots_per_day, population_size, crossover_rate, mutation_rate, max_generations):
        self.exams = exams
        self.max_days = max_days
        self.slots_per_day = slots_per_day
        self.population_size = population_size
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.max_generations = max_generations
        self.population = []
        self.best_schedule = None

    # ایجاد جمعیت اولیه
    def initialize_population(self):
        for _ in range(self.population_size):
            schedule = []
            for exam in self.exams:
                day = random.randint(1, self.max_days)
                slot = random.randint(1, self.slots_per_day)
                schedule.append((exam, day, slot))
            self.population.append(schedule)

    # محاسبه فیتنس
    def fitness(self, schedule):
        conflicts = 0
        time_slots = {}
        for exam, day, slot in schedule:
            if (day, slot) not in time_slots:
                time_slots[(day, slot)] = [exam]
            else:
                time_slots[(day, slot)].append(exam)
                conflicts += 1  # هر امتحان اضافی در یک اسلات زمانی به عنوان تداخل محاسبه می‌شود
        return 1 / (1 + conflicts)  # هرچه تعداد تداخل کمتر باشد فیتنس بیشتر است

    # انتخاب بر اساس فیتنس
    def select_parent(self):
        total_fitness = sum(self.fitness(schedule) for schedule in self.population)
        pick = random.uniform(0, total_fitness)
        current = 0
        for schedule in self.population:
            current += self.fitness(schedule)
            if current >= pick:
                return schedule

    # اعمال کراس‌اور
    def crossover(self, parent1, parent2):
        if random.random() < self.crossover_rate:
            point = random.randint(0, len(parent1) - 1)
            child1 = parent1[:point] + parent2[point:]
            child2 = parent2[:point] + parent1[point:]
            return child1, child2
        return parent1, parent2

    # اعمال جهش
    def mutate(self, schedule):
        if random.random() < self.mutation_rate:
            idx = random.randint(0, len(schedule) - 1)
            day = random.randint(1, self.max_days)
            slot = random.randint(1, self.slots_per_day)
            schedule[idx] = (schedule[idx][0], day, slot)
        return schedule

    # اجرای الگوریتم ژنتیک
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
            # بروزرسانی بهترین برنامه
            self.best_schedule = max(self.population, key=self.fitness)

    # نمایش برنامه نهایی
    def display_schedule(self):
        schedule = sorted(self.best_schedule, key=lambda x: (x[1], x[2]))
        for exam, day, slot in schedule:
            print(f"Day {day}, Slot {slot}: {exam.course_name} by {exam.teacher_name}, Duration: {exam.duration} hours")


# تعریف امتحانات    
exams = [
    Exam("Math", "Dr. Smith", 2),
    Exam("Physics", "Dr. Brown", 3),
    Exam("Chemistry", "Dr. White", 2),
    Exam("Biology", "Dr. Green", 1),
    Exam("English", "Dr. Black", 1.5),
]

ga = GA(
    exams=exams,
    max_days=5,
    slots_per_day=4,
    population_size=50,
    crossover_rate=0.8,
    mutation_rate=0.1,
    max_generations=100
)
ga.run()
ga.display_schedule()