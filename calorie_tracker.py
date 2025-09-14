from datetime import datetime
import smtplib
import pandas as pd
import requests
from email.message import EmailMessage
from dotenv import load_dotenv
import os
load_dotenv()
APP_ID=os.getenv("APP_ID_NUTRIENTS")
API_KEY=os.getenv("API_KEY_NUTRIENTS")
GENDER="Male"
AGE=19
HEIGHT=172
WEIGHT=40
nutrients_endpoint='https://trackapi.nutritionix.com/v2/natural/nutrients'
exercise_endpoint="https://trackapi.nutritionix.com/v2/natural/exercise"
sheet_endpoint="https://api.sheety.co/6682f01f3a8cf44442624b4fbe16dc1a/copyOfMyWorkouts/workouts"
today_date = datetime.now().strftime("%d/%m/%Y")
now_time = datetime.now().strftime("%X")
headers={
    'x-app-id':APP_ID,
    'x-app-key':API_KEY
}
option=input("Enter 1 for log or 2 for send detail of Net Calories: ")
if option == "1":
    should_continue=True
    while should_continue:
        choice = input("What would you like to log? Type 'exercise' or 'eating': ").strip().lower()

        if choice == "exercise":
            query = input("Describe your exercise (e.g., 'ran 3km in 20 minutes'): ")
            ex_parameters = {
                "query": query,
                "weight_kg":WEIGHT,
                "height_cm":HEIGHT,
                "age":AGE,
            }
            ex_response = requests.post(url=exercise_endpoint, json=ex_parameters, headers=headers)
            if ex_response.status_code == 200:
                ex_result = ex_response.json()
                for exercise in ex_result["exercises"]:
                    sheet_inputs = {
                        "workout": {
                            "date": today_date,
                            "time": now_time,
                            "type": exercise["name"].title(),
                             "details": f"{exercise['name'].title()} for {exercise['duration_min']} mins",
                            "calories": "-"+str(exercise["nf_calories"])
                        }
                    }
                    sheet_response = requests.post(sheet_endpoint, json=sheet_inputs)
            else:
                print("Error in food API:", ex_response.text)

        elif choice == "eating":
            query = input("What did you eat? (e.g., '2 eggs and a coffee'): ")
            nut_parameters={
                "query": query,
            }
            nut_response=requests.post(url=nutrients_endpoint, json=nut_parameters, headers=headers)
            if nut_response.status_code == 200:
                nut_result = nut_response.json()
                for food in nut_result["foods"]:
                    sheet_inputs = {
                        "workout": {
                            "date": today_date,
                            "time": now_time,
                            "type":"Eating",
                            "details": f"{food['serving_qty']} {food['serving_unit']} {food['food_name']}",
                            "calories": "+"+str(food["nf_calories"])
                        }
                    }
                    sheet_response = requests.post(sheet_endpoint, json=sheet_inputs)

            else:
                print("Error in food API:", nut_response.text)
        else:
            print("Invalid choice. Please type 'exercise' or 'eating'.")
        to_continue = input("Do you want to enter  more detail (yes/no): ")
        if to_continue.lower() == "no":
            should_continue=False

elif option == "2":

    response = requests.get(sheet_endpoint)
    data = response.json()
    workouts = data["workouts"]
    df = pd.DataFrame(workouts)
    today = datetime.now().strftime("%d/%m/%Y")
    df_today = df[df["date"] == today]
    df_today["type"] = df_today["type"].str.lower()
    df_today["calories"] = df_today["calories"].str.replace("+", "").astype(float)
    calories_eaten = df_today[df_today["type"] == "eating"]["calories"].sum()
    calories_burned = df_today[df_today["type"] != "eating"]["calories"].abs().sum()
    net_calories = calories_eaten - calories_burned
    msg_body = (
        f"🧾 Daily Calorie Summary:\n\n"
        f"🍽️ Calories Eaten: {round(calories_eaten, 2)} kcal\n"
        f"🔥 Calories Burned: {round(calories_burned, 2)} kcal\n"
        f"⚖️ Net Calories: {round(net_calories, 2)} kcal\n\n"
        "Stay consistent and keep tracking! 💪"
    )
    MY_EMAIL =os.getenv("MY_EMAIL")
    MY_PASSWORD =os.getenv("MY_PASSWORD")
    with smtplib.SMTP('smtp.gmail.com') as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL,password=MY_PASSWORD)

        msg = EmailMessage()
        msg.set_content(msg_body)
        msg['Subject'] = "Your Daily Calorie Summary"
        msg['From'] = MY_EMAIL
        msg['To'] = "abdulh56778@gmail.com"

        connection.send_message(msg)
        print("Message sent successfully.")


