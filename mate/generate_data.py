import csv
import random

female_names = [
    "Aditi","Riya","Priya","Sneha","Pooja","Anjali","Neha","Kavya","Meera","Divya",
    "Sana","Fatima","Zara","Aisha","Noor","Simran","Harpreet","Gurpreet","Manpreet","Jasleen",
    "Lakshmi","Radha","Geetha","Sunita","Rekha","Usha","Anita","Smita","Jyoti","Shweta",
    "Tanvi","Shruti","Swati","Pallavi","Madhuri","Namrata","Aparna","Bhavna","Chitra","Deepa",
    "Leela","Mala","Nandini","Pari","Renu","Seema","Tara","Uma"
]

male_names = [
    "Rahul","Arjun","Rohan","Vikram","Amit","Suresh","Karan","Nikhil","Raj","Dev",
    "Arun","Deepak","Manoj","Sanjay","Vijay","Ramesh","Sunil","Anil","Pankaj","Gaurav",
    "Akash","Vishal","Tushar","Sachin","Rohit","Mohit","Sumit","Ankit","Vivek","Abhishek",
    "Farhan","Imran","Salman","Zaid","Asif","Bilal","Hamid","Irfan","Junaid","Khalid",
    "Omi","Qureshi"
]

cities = ["Mumbai","Delhi","Bangalore","Hyderabad","Chennai","Pune","Kolkata","Ahmedabad","Jaipur","Lucknow"]
food_options = ["Veg","Non-Veg","Both"]
sleep_options = ["Early Sleeper","Night Owl"]
cleanliness_options = ["Low","Medium","High"]
yes_no = ["Yes","No"]
study_habits = ["Quiet","Moderate","Flexible"]
sharing_options = ["Single Room","Shared Room"]

rows = []
for i in range(1000):
    gender = random.choice(["Male", "Female"])
    name = random.choice(male_names if gender == "Male" else female_names) + str(random.randint(1, 999))
    rows.append({
        "Name": name,
        "Age": random.randint(18, 35),
        "Gender": gender,
        "City": random.choice(cities),
        "Budget": random.randrange(3000, 30001, 500),
        "Food": random.choice(food_options),
        "Sleep": random.choice(sleep_options),
        "Cleanliness": random.choice(cleanliness_options),
        "Smoking": random.choice(yes_no),
        "Drinking": random.choice(yes_no),
        "StudyHabit": random.choice(study_habits),
        "SharingPreference": random.choice(sharing_options),
    })

with open("users.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)

print("Generated 1000 records in users.csv")
