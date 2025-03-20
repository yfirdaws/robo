import csv
import random

# Sample lists of names
first_names = [
    # Nigerian/Christian names
    "Chinedu", "Emeka", "Ngozi", "Ifeoma", "Uche", "Amaka", "Obi", "Ifeanyi", "Nkechi", "Ada",
    # Islamic names
    "Muhammad", "Abdulrahman", "Ibrahim", "Aisha", "Fatima", "Khadijah", "Mustapha", "Hassan", "Yusuf", "Bilqis",
    # Generic Nigerian names
    "Tunde", "Segun", "Bola", "Kemi", "Funke", "Ade", "Sola", "Femi", "Chioma", "Esther","Ufedojo"
]

last_names = [
    "Adeyemi", "Balogun", "Okafor", "Abubakar", "Ibrahim", "Oluwaseun", "Ogunleye", "Eze", "Bello", "Lawal", "Okafor","Osarime"
    "Adebayo", "Osagie", "Uzochukwu", "Mustapha", "Danladi", "Akinola", "Chukwu", "Jibril", "Ojo", "Olufemi", "Musa","Adamu"
]

# Possible categorical responses
reaction_options = ["Panic", "Hold", "Buy More"]
goal_options = ["Preserve Capital", "Steady Growth", "Maximize Returns"]
risk_categories = ["Conservative", "Moderate", "Aggressive"]

# Function to generate a random full name
def random_full_name():
    return f"{random.choice(first_names)} {random.choice(last_names)}"

# Generate 100 rows of sample data
data = [["Full Name", "Age", "Income", "Investment Experience (years)", "Time Horizon (years)",
         "Self-Reported Risk Score", "Reaction to Losses", "Investment Goal", "Risk Category"]]

for _ in range(100):
    full_name = random_full_name()
    age = random.randint(18, 65)
    # Income in Naira based on ranges from our earlier discussion (0 - 50M+)
    income_choice = random.choices(
        population=["0-500k", "501k-1M", "1M-3M", "3M-5M", "5M-10M", "10M-50M", "50M+"],
        weights=[10, 15, 20, 20, 15, 10, 5], k=1
    )[0]
    # Map the income_choice to a random value within the range
    if income_choice == "0-500k":
        income = random.randint(0, 500_000)
    elif income_choice == "501k-1M":
        income = random.randint(501_000, 1_000_000)
    elif income_choice == "1M-3M":
        income = random.randint(1_000_001, 3_000_000)
    elif income_choice == "3M-5M":
        income = random.randint(3_000_001, 5_000_000)
    elif income_choice == "5M-10M":
        income = random.randint(5_000_001, 10_000_000)
    elif income_choice == "10M-50M":
        income = random.randint(10_000_001, 50_000_000)
    else:  # "50M+"
        income = random.randint(50_000_001, 100_000_000)
        
    experience = random.randint(0, min(age - 18, 30))  # assuming max experience is age-18
    time_horizon = random.randint(1, 15)
    risk_score = random.randint(1, 10)
    reaction = random.choice(reaction_options)
    goal = random.choice(goal_options)
    risk_category = random.choice(risk_categories)
    
    data.append([full_name, age, income, experience, time_horizon, risk_score, reaction, goal, risk_category])

# Write to CSV file
filename = "investor_risk_profile.csv"
with open(filename, "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerows(data)

print(f"CSV file '{filename}' with 100 rows created successfully.")
