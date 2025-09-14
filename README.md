# Calories-Counter
A Python CLI tool to log food and workouts using Nutritionix, store in Google Sheets via Sheety, and get daily net calorie summaries by email.
## Features

- Log exercises and meals using natural language input
- Calculate net calories (calories consumed minus calories burned)
- Store logs in Google Sheets via Sheety API
- Send daily summary emails with calorie details
- Secure API key and credential management using `.env`

## Prerequisites

- Python 3.x installed
- A Nutritionix developer account (for API keys)
- Sheety account and Google Sheets set up
- Gmail account with SMTP access enabled (app password recommended)

## Installation & Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/AbdulHadi640/Calories-Counter.git
   cd Calories-Counter
