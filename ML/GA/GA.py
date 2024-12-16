import random
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
class Exam:
    def __init__(self, course_name, teacher_name, duration):
        self.course_name = course_name
        self.teacher_name = teacher_name
        self.duration = duration
        self.time_slot = None  # Assigned later


# GA Class
class GA:
    def __init__(self, exams, start_date, end_date, slots_per_day, max_hours_per_day, population_size, crossover_rate, mutation_rate, max_generations):
        self.exams = exams
        self.start_date = datetime.strptime(start_date, "%Y-%m-%d")
        self.end_date = datetime.strptime(end_date, "%Y-%m-%d")
        self.slots_per_day = slots_per_day
        self.max_hours_per_day = max_hours_per_day
        self.population_size = population_size
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.max_generations = max_generations
        self.population = []
        self.best_schedule = None
        self.max_days = (self.end_date - self.start_date).days + 1

    # Initialize population
    def initialize_population(self):
        for _ in range(self.population_size):
            schedule = []
            for exam in self.exams:
                day = random.randint(1, self.max_days)
                slot = random.randint(1, self.slots_per_day)
                schedule.append((exam, day, slot))
            self.population.append(schedule)

    # Fitness function
    def fitness(self, schedule):
        conflicts = 0
        hours_used = [0] * self.max_days

        for exam, day, slot in schedule:
            if hours_used[day - 1] + exam.duration > self.max_hours_per_day:
                conflicts += 1  # Daily hours exceeded
            else:
                hours_used[day - 1] += exam.duration

        # Check for teacher conflicts in the same time slot
        time_slots = {}
        for exam, day, slot in schedule:
            if (day, slot) not in time_slots:
                time_slots[(day, slot)] = [exam]
            else:
                # Check if teachers conflict
                if any(e.teacher_name == exam.teacher_name for e in time_slots[(day, slot)]):
                    conflicts += 1
                else:
                    time_slots[(day, slot)].append(exam)

        return 1 / (1 + conflicts)

    # Select parent
    def select_parent(self):
        total_fitness = sum(self.fitness(schedule) for schedule in self.population)
        pick = random.uniform(0, total_fitness)
        current = 0
        for schedule in self.population:
            current += self.fitness(schedule)
            if current >= pick:
                return schedule

    # Crossover
    def crossover(self, parent1, parent2):
        if random.random() < self.crossover_rate:
            point = random.randint(0, len(parent1) - 1)
            child1 = parent1[:point] + parent2[point:]
            child2 = parent2[:point] + parent1[point:]
            return child1, child2
        return parent1, parent2

    # Mutation
    def mutate(self, schedule):
        if random.random() < self.mutation_rate:
            idx = random.randint(0, len(schedule) - 1)
            day = random.randint(1, self.max_days)
            slot = random.randint(1, self.slots_per_day)
            schedule[idx] = (schedule[idx][0], day, slot)
        return schedule

    # Run the GA
    def run(self):
        self.initialize_population()
        for _ in range(self.max_generations):
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

    # Display schedule and visualize it on a Gantt Chart
    def display_schedule(self):
        schedule = sorted(self.best_schedule, key=lambda x: (x[1], x[2]))
        gantt_data = []

        for exam, day, slot in schedule:
            exam_date = self.start_date + timedelta(days=day - 1)
            start_time = slot * (self.max_hours_per_day / self.slots_per_day)  # Convert slot to hours
            end_time = start_time + exam.duration
            gantt_data.append((exam.course_name, exam_date, start_time, end_time))

            print(
                f"Date: {exam_date.strftime('%Y-%m-%d')}, Slot: {slot}, "
                f"Exam: {exam.course_name} by {exam.teacher_name}, Duration: {exam.duration} hours"
            )

        self.visualize_gantt_chart(gantt_data)

    # Gantt Chart Visualization
    def visualize_gantt_chart(self, gantt_data):
        plt.figure(figsize=(12, 8))
        for i, (course_name, exam_date, start_time, end_time) in enumerate(gantt_data):
            plt.barh(
                y=exam_date.strftime("%Y-%m-%d"),
                width=end_time - start_time,
                left=start_time,
                label=course_name
            )
            plt.text(
                x=start_time + (end_time - start_time) / 2,
                y=exam_date.strftime("%Y-%m-%d"),
                s=course_name,
                va='center',
                ha='center',
                color='white',
                fontsize=8,
                fontweight='bold'
            )

        plt.xlabel("Hours")
        plt.ylabel("Dates")
        plt.title("Exam Schedule Gantt Chart")
        plt.grid(axis='x', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.show()

exams = [
    Exam("Math", "Dr. Smith", 2),
    Exam("Physics", "Dr. Brown", 3),
    Exam("Chemistry", "Dr. White", 2),
    Exam("Biology", "Dr. Green", 1),
    Exam("English", "Dr. Black", 1.5),
    Exam("History", "Dr. Black", 1),
    # Exam("History", "Dr. Gray", 2),
    # Exam("Geography", "Dr. Blue", 1),
    # Exam("Economics", "Dr. Red", 2),
    # Exam("Computer Science", "Dr. Purple", 3),
    # Exam("Art", "Dr. Pink", 1),
    # Exam("Music", "Dr. Orange", 2),
]

ga = GA(
    exams=exams,
    start_date="2024-12-18",
    end_date="2024-12-28",
    slots_per_day=4,
    max_hours_per_day=6,
    population_size=50,
    crossover_rate=0.8,
    mutation_rate=0.1,
    max_generations=100
)

ga.run()
ga.display_schedule()