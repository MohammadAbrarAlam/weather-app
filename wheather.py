import requests
import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime

API_Key = "edabeb81d712caefbaebef2743db3184"   # Your API key
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def get_weather():
    city = city_entry.get().strip()

    if not city:
        messagebox.showerror("Error", "Please enter a city name.")
        return

    result_label.config(text="Fetching weather...")
    
    # Clear previous results
    clear_results()

    params = {
        "q": f"{city},IN",  # Restricts search to India
        "appid": API_Key,
        "units": "metric"
    }

    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        data = response.json()

        if response.status_code != 200:
            error_msg = data.get("message", "City not found in India")
            messagebox.showerror("Error", f"{error_msg}\nPlease enter a valid Indian city name.")
            result_label.config(text="")
            return

        # Extract weather data
        city_name = data['name']
        state = data.get('sys', {}).get('state', 'India')
        temperature = data['main']['temp']
        feels_like = data['main']['feels_like']
        description = data['weather'][0]['description'].title()
        humidity = data['main']['humidity']
        pressure = data['main']['pressure']
        wind_speed = data['wind']['speed']
        visibility = data.get('visibility', 0) / 1000  # Convert to km
        
        # Get current time
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Display weather information
        display_weather_info(city_name, state, temperature, feels_like, 
                           description, humidity, pressure, wind_speed, 
                           visibility, current_time)

    except requests.exceptions.Timeout:
        messagebox.showerror("Error", "Request timed out. Please check your internet connection.")
        result_label.config(text="")
    except requests.exceptions.ConnectionError:
        messagebox.showerror("Error", "Connection error. Please check your internet connection.")
        result_label.config(text="")
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")
        result_label.config(text="")
    except KeyError as e:
        messagebox.showerror("Error", "Invalid response from weather service.")
        result_label.config(text="")

def display_weather_info(city, state, temp, feels_like, desc, humidity, 
                        pressure, wind, visibility, time):
    weather_info = f"""
🌍 City: {city}, {state}
🌡️  Temperature: {temp}°C (Feels like {feels_like}°C)
☁️  Weather: {desc}
💧 Humidity: {humidity}%
🌬️  Wind Speed: {wind} m/s
📊 Pressure: {pressure} hPa
👁️  Visibility: {visibility:.1f} km
🕒 Last Updated: {time}
    """
    result_label.config(text=weather_info.strip())

def clear_results():
    result_label.config(text="")

def on_enter_key(event):
    get_weather()

def clear_entry():
    city_entry.delete(0, tk.END)
    clear_results()

# GUI Window
root = tk.Tk()
root.title("Indian Cities Weather App")
root.geometry("450x400")
root.resizable(False, False)
root.configure(bg='#f0f0f0')

# Title
title_label = tk.Label(root, text="🇮🇳 Indian Weather App", 
                      font=("Arial", 18, "bold"), 
                      bg='#f0f0f0', fg='#2c3e50')
title_label.pack(pady=15)

# Input frame
input_frame = tk.Frame(root, bg='#f0f0f0')
input_frame.pack(pady=10)

tk.Label(input_frame, text="Enter Indian City Name:", 
         font=("Arial", 12), bg='#f0f0f0').pack()

city_entry = tk.Entry(input_frame, font=("Arial", 14), width=25, 
                     relief="solid", bd=1)
city_entry.pack(pady=5)
city_entry.bind('<Return>', on_enter_key)  # Enter key binding

# Button frame
button_frame = tk.Frame(root, bg='#f0f0f0')
button_frame.pack(pady=10)

get_weather_btn = tk.Button(button_frame, text="🌤️ Get Weather", 
                           font=("Arial", 12, "bold"), 
                           command=get_weather,
                           bg='#3498db', fg='white',
                           relief="raised", bd=2,
                           cursor="hand2")
get_weather_btn.pack(side=tk.LEFT, padx=5)

clear_btn = tk.Button(button_frame, text="🗑️ Clear", 
                     font=("Arial", 12), 
                     command=clear_entry,
                     bg='#e74c3c', fg='white',
                     relief="raised", bd=2,
                     cursor="hand2")
clear_btn.pack(side=tk.LEFT, padx=5)

# Result label with scrollable text
result_frame = tk.Frame(root, bg='#f0f0f0')
result_frame.pack(pady=15, padx=20, fill='both', expand=True)

result_label = tk.Label(result_frame, text="", 
                       font=("Courier", 11), 
                       justify="left", 
                       bg='white', 
                       relief="solid", 
                       bd=1,
                       anchor='nw',
                       padx=10, pady=10)
result_label.pack(fill='both', expand=True)

# Instructions
instruction_label = tk.Label(root, 
                           text="💡 Tip: Press Enter after typing city name", 
                           font=("Arial", 9), 
                           bg='#f0f0f0', fg='#7f8c8d')
instruction_label.pack(pady=5)

# Focus on entry field
city_entry.focus()

root.mainloop()
