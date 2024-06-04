from __future__ import print_function
import time
import feedparser
import datetime
import calendar


try:
    from Tkinter import *
    import Tkinter as tk
except ImportError:
    from tkinter import *
    import tkinter as tk
import requests
import pprint

from PIL import Image, ImageTk

time_format = 24  # 12 or 24
date_format = "%b %d, %Y"
news_country_code = 'IN:hi'
weather_api_token = '36ce6f9f9405ff60e8ff4b8717448d45'
weather_city_id = '1252758'
weather_unit = 'metric'

xlarge_text_size = 94
large_text_size = 48
medium_text_size = 28
small_text_size = 18
xsmall_text_size = 14
text_font = "Calibri"
text_color = "white"
background_color = 'black'
icon_lookup = {
    '01d': "assets/01d.png",
    '01n': "assets/01n.png",
    '02d': "assets/02d.png",
    '02n': "assets/02n.png",
    '03d': "assets/03d.png",
    '03n': "assets/03n.png",
    '04d': "assets/04d.png",
    '04n': "assets/04n.png",
    '09d': "assets/09d.png",
    '09n': "assets/09n.png",
    '10d': "assets/10d.png",
    '10n': "assets/10n.png",
    '11d': "assets/11d.png",
    '11n': "assets/11n.png",
    '13d': "assets/13d.png",
    '13n': "assets/13n.png",
    '50d': "assets/50d.png",
    '50n': "assets/50n.png",
}

class Clock(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent, bg=background_color)
        self.time1 = ''
        self.timeLbl = Label(self, font=(text_font, xlarge_text_size), fg=text_color, bg=background_color)
        self.timeLbl.pack(side=tk.TOP, anchor=tk.W)
        self.day_of_week1 = ''
        self.dayOWLbl = Label(self, text=self.day_of_week1, font=(text_font, medium_text_size), fg=text_color,
                              bg=background_color)
        self.dayOWLbl.pack(side=tk.TOP, anchor=tk.W)
        self.date1 = ''
        self.dateLbl = Label(self, text=self.date1, font=(text_font, medium_text_size), fg=text_color,
                             bg=background_color)
        self.dateLbl.pack(side=tk.TOP, anchor=tk.W)
        self.tick()

    def tick(self):
        global time_format, date_format
        if time_format == 12:
            time2 = time.strftime('%I:%M:%S %p')  
        else:
            current_hour = int(time.strftime('%H'))  
            am_pm = "AM" if current_hour < 12 else "PM"
            time2 = f"{time.strftime('%H:%M:%S')} {am_pm}"  

        day_of_week2 = time.strftime('%A')
        date2 = time.strftime(date_format)

        if time2!= self.time1:
            self.time1 = time2
            self.timeLbl.config(text=time2)
        if day_of_week2!= self.day_of_week1:
            self.day_of_week1 = day_of_week2
            self.dayOWLbl.config(text=day_of_week2)
        if date2!= self.date1:
            self.date1 = date2
            self.dateLbl.config(text=date2)
        self.timeLbl.after(200, self.tick)





class News(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.config(bg=background_color)
        self.categories = [
            "Technology",
            "World",
            "Local",
            "Business",
            "Entertainment",
            "Sports",
            "Science",
            "Health"
        ]
        self.current_category_index = 0

        self.titleLbl = Label(self, text=f' ▤ {self.categories[self.current_category_index]} News ▤ ', font=(text_font, medium_text_size), fg=text_color, bg=background_color)
        self.titleLbl.pack(side=TOP, anchor=W)
        self.headlinesContainer = Frame(self, bg=background_color)
        self.headlinesContainer.pack(side=TOP)

        self.update_category()

    def update_category(self):
        self.titleLbl.config(text=f' ▤ {self.categories[self.current_category_index]} News ▤ ')
        self.get_headlines()

    def get_headlines(self):
        try:
            for widget in self.headlinesContainer.winfo_children():
                widget.destroy()

            feed = feedparser.parse(self.get_category_url())
            for post in feed.entries[0:7]:
                headline = NewsHeadline(self.headlinesContainer, post.title)
                headline.pack(side=TOP, anchor=W)
        except Exception as e:
            print(f"Error: Cannot get news. {e}")

        # Switch to the next category
        self.current_category_index = (self.current_category_index + 1) % len(self.categories)

        # Schedule next update
        self.after(6000, self.update_category)

    def get_category_url(self):
        category_urls = {
            "Technology": "https://news.google.com/rss/topics/CAAqKggKIiRDQkFTRlFvSUwyMHZNRGRqTVhZU0JXVnVMVWRDR2dKSlRpZ0FQAQ?hl=en-IN&gl=IN&ceid=IN%3Aen&oc=11",
            "World": "https://news.google.com/rss/topics/CAAqKggKIiRDQkFTRlFvSUwyMHZNRGx1YlY4U0JXVnVMVWRDR2dKSlRpZ0FQAQ?hl=en-IN&gl=IN&ceid=IN%3Aen&oc=11",
            "Local": "https://news.google.com/rss/topics/CAAqHAgKIhZDQklTQ2pvSWJHOWpZV3hmZGpJb0FBUAE/sections/CAQiTkNCSVNORG9JYkc5allXeGZkakpDRUd4dlkyRnNYM1l5WDNObFkzUnBiMjV5Q2hJSUwyMHZNRGxqTVRkNkNnb0lMMjB2TURsak1UY29BQSowCAAqLAgKIiZDQklTRmpvSWJHOWpZV3hmZGpKNkNnb0lMMjB2TURsak1UY29BQVABUAE?hl=en-IN&gl=IN&ceid=IN%3Aen&oc=11",
            "Business": "https://news.google.com/atom/topics/CAAqKggKIiRDQkFTRlFvSUwyMHZNRGx6TVdZU0JXVnVMVWRDR2dKSlRpZ0FQAQ?hl=en-IN&gl=IN&ceid=IN%3Aen&oc=11",
            "Entertainment": "https://news.google.com/rss/topics/CAAqKggKIiRDQkFTRlFvSUwyMHZNREpxYW5RU0JXVnVMVWRDR2dKSlRpZ0FQAQ?hl=en-IN&gl=IN&ceid=IN%3Aen&oc=11",
            "Sports": "https://news.google.com/rss/topics/CAAqKggKIiRDQkFTRlFvSUwyMHZNRFp1ZEdvU0JXVnVMVWRDR2dKSlRpZ0FQAQ?hl=en-IN&gl=IN&ceid=IN%3Aen&oc=11",
            "Science": "https://news.google.com/rss/topics/CAAqKggKIiRDQkFTRlFvSUwyMHZNRFp0Y1RjU0JXVnVMVWRDR2dKSlRpZ0FQAQ?hl=en-IN&gl=IN&ceid=IN%3Aen&oc=11",
            "Health": "https://news.google.com/rss/topics/CAAqJQgKIh9DQkFTRVFvSUwyMHZNR3QwTlRFU0JXVnVMVWRDS0FBUAE?hl=en-IN&gl=IN&ceid=IN%3Aen&oc=11",
        }
        return category_urls[self.categories[self.current_category_index]]


class NewsHeadline(Frame):
    def __init__(self, parent, event_name="", *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.config(bg=background_color)
        try:
            image = Image.open("assets/Newspaper.png")
            image = image.resize((25, 25), Image.BICUBIC)
            image = image.convert('RGB')
            photo = ImageTk.PhotoImage(image)

            self.iconLbl = Label(self, bg=background_color, image=photo)
            self.iconLbl.image = photo
            self.iconLbl.pack(side=LEFT, anchor=N)
        except Exception as e:
            print(f"Error loading news icon: {e}")

        self.eventName = event_name
        self.eventNameLbl = Label(self, text=self.eventName, font=(text_font, small_text_size), fg=text_color,
                                  bg=background_color)
        self.eventNameLbl.pack(side=LEFT, anchor=N)

class CalendarFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.config(bg='black')

        # Initialize current month and year
        self.current_month = datetime.datetime.now().month
        self.current_year = datetime.datetime.now().year

        # Displayed month and year
        self.display_month = self.current_month
        self.display_year = self.current_year

        self.calendar_frame = tk.Frame(self, bg='black')
        self.calendar_frame.pack()

        self.update_calendar()

    def update_calendar(self):
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()

        now = datetime.datetime.now()
        cal = calendar.Calendar()
        cal_content = cal.monthdayscalendar(self.display_year, self.display_month)
        cal_header = calendar.month_name[self.display_month] + " " + str(self.display_year)

        header_frame = tk.Frame(self.calendar_frame, bg='black')
        header_frame.grid(row=0, column=0, columnspan=7)

        prev_button = tk.Button(header_frame, text="<", font=("Helvetica", 12), fg="white", bg="black", command=self.prev_month, relief="flat", bd=0)
        prev_button.pack(side="left")

        header_label = tk.Label(header_frame, text=cal_header, font=("Helvetica", 14), fg="white", bg="black")
        header_label.pack(side="left", padx=(10, 10))

        next_button = tk.Button(header_frame, text=">", font=("Helvetica", 12), fg="white", bg="black", command=self.next_month, relief="flat", bd=0)
        next_button.pack(side="left")

        days = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]
        for idx, day in enumerate(days):
            day_label = tk.Label(self.calendar_frame, text=day, font=("Helvetica", 12), fg="white", bg="black")
            day_label.grid(row=1, column=idx, padx=5)

        for week_idx, week in enumerate(cal_content):
            for day_idx, day in enumerate(week):
                if day == 0:
                    day_label = tk.Label(self.calendar_frame, text="  ", font=("Helvetica", 12), fg="white", bg="black")
                elif day == now.day and self.display_month == now.month and self.display_year == now.year:
                    day_label = tk.Label(self.calendar_frame, text=f"{day:2}", font=("Helvetica", 12), fg="white", bg="red")
                else:
                    day_label = tk.Label(self.calendar_frame, text=f"{day:2}", font=("Helvetica", 12), fg="white", bg="black")
                day_label.grid(row=week_idx + 2, column=day_idx, padx=5, pady=5)

        if self.display_month != self.current_month or self.display_year != self.current_year:
            reset_button = tk.Button(self.calendar_frame, text="Reset to Current Month", font=("Helvetica", 12), fg="white", bg="black", command=self.reset_calendar, relief="flat", bd=0)
            reset_button.grid(row=len(cal_content) + 2, column=0, columnspan=7, pady=(10, 0))

    def prev_month(self):
        if self.display_month == 1:
            self.display_month = 12
            self.display_year -= 1
        else:
            self.display_month -= 1
        self.update_calendar()

    def next_month(self):
        if self.display_month == 12:
            self.display_month = 1
            self.display_year += 1
        else:
            self.display_month += 1
        self.update_calendar()

    def reset_calendar(self):
        self.display_month = self.current_month
        self.display_year = self.current_year
        self.update_calendar()


class Reminders(Frame):
    def __init__(self, parent, reminders_data, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.config(bg=background_color)
        self.reminders_data = reminders_data
        self.title = 'Reminders'
        self.titleLbl = Label(self, text=self.title, font=(text_font, medium_text_size), fg=text_color, bg=background_color)
        self.titleLbl.pack(side=TOP, anchor=W)

        self.remindersContainer = Frame(self, bg=background_color)
        self.remindersContainer.pack(side=TOP)

        self.update_reminders()

    def update_reminders(self):
        for widget in self.remindersContainer.winfo_children():
            widget.destroy()

        for reminder in self.reminders_data:
            reminder_text = reminder["text"]
            reminder_date = reminder["date"]
            reminder_label_text = f"{reminder_text}: {reminder_date}"

            reminder_label = Label(self.remindersContainer, text=reminder_label_text, font=(text_font, small_text_size), fg=text_color, bg=background_color)
            reminder_label.pack(side=TOP, anchor=W)

class Reminders(Frame):
    def __init__(self, parent, reminders_data, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.config(bg=background_color)
        self.reminders_data = reminders_data
        self.title = 'Reminders'
        self.titleLbl = Label(self, text=self.title, font=(text_font, medium_text_size), fg=text_color, bg=background_color)
        self.titleLbl.pack(side=TOP, anchor=W)

        self.remindersContainer = Frame(self, bg=background_color)
        self.remindersContainer.pack(side=TOP)

        self.update_reminders()

    def update_reminders(self):
        for widget in self.remindersContainer.winfo_children():
            widget.destroy()

        for reminder in self.reminders_data:
            reminder_text = reminder["text"]
            reminder_date = reminder["date"]
            reminder_label_text = f"{reminder_text}: {reminder_date}"

            reminder_label = Label(self.remindersContainer, text=reminder_label_text, font=(text_font, small_text_size), fg=text_color, bg=background_color)
            reminder_label.pack(side=TOP, anchor=NW)



class FullscreenWindow:
    def __init__(self):
        self.tk = tk.Tk()
        self.tk.configure(background=background_color)
        self.topFrame = tk.Frame(self.tk, background=background_color)
        self.bottomFrame = tk.Frame(self.tk, background=background_color)
        self.topFrame.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.YES)
        self.bottomFrame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=tk.YES)
        self.state = True
        self.tk.bind("<F11>", self.toggle_fullscreen)
        self.tk.attributes("-fullscreen", self.state)
        self.tk.config(cursor='none')
        
        # Clock and Reminders frame
        self.clock_reminders_frame = tk.Frame(self.topFrame, background=background_color)
        self.clock_reminders_frame.pack(side=tk.LEFT, anchor=tk.NW, padx=0, pady=0)

        # clock
        self.clock = Clock(self.clock_reminders_frame)
        self.clock.pack(side=tk.TOP, anchor=tk.NW, padx=20, pady=20)

        # reminders
        self.reminders_data = [
            {"text": "IPR Phase3 (Level2) scheduled on", "date": "4th June"},
            {"text": "End term exams starts from", "date": "6th June"}
        ]
        self.reminders = Reminders(self.clock_reminders_frame, self.reminders_data)
        self.reminders.pack(side=tk.BOTTOM, anchor=tk.W, padx=20, pady=20)

        # Weather and Calendar frame
        self.weather_calendar_frame = tk.Frame(self.topFrame, background=background_color)
        self.weather_calendar_frame.pack(side=tk.TOP, anchor=tk.NE, padx=20, pady=20)

        # weather
        self.weather = Weather(self.weather_calendar_frame)
        self.weather.pack(side=tk.TOP, anchor=tk.NE, padx=20, pady=20)

        # calendar
        self.calendar = CalendarFrame(self.weather_calendar_frame)
        self.calendar.pack(side=tk.TOP, anchor=tk.NE, padx=20, pady=(10, 0))

        # Create a new frame to hold both the greeting and news frames
        self.bottomContentFrame = tk.Frame(self.bottomFrame, background=background_color)
        self.bottomContentFrame.pack(side=tk.BOTTOM, fill=tk.X, padx=20)

        # Add the greeting frame
        self.greeting_frame = tk.Frame(self.bottomContentFrame, background=background_color)
        self.greeting_frame.pack(side=tk.TOP, fill=tk.X) 

        # Add the greeting label
        self.greeting_label = tk.Label(self.greeting_frame, font=(text_font, medium_text_size), fg=text_color, bg=background_color)
        self.greeting_label.pack(side=tk.TOP, anchor=tk.CENTER)
        self.update_greeting()

        # news
        self.news = News(self.bottomContentFrame)
        self.news.pack(side=tk.LEFT, anchor=tk.SW, padx=20)  
        
    def toggle_fullscreen(self, event=None):
        self.state = not self.state  
        self.tk.attributes("-fullscreen", self.state)
        return "break"
    
    def update_greeting(self):
        current_time = datetime.datetime.now()
        hour = current_time.hour

        if 5 <= hour < 12:
            greeting = "Good morning!"
            compliment = "Hope you have a wonderful day."
        elif 12 <= hour < 18:
            greeting = "Good afternoon!"
            compliment = "You're doing great!"
        elif 18 <= hour < 22:
            greeting = "Good evening!"
            compliment = "You're amazing!"
        else:
            greeting = "Good night!"
            compliment = "Sweet dreams!"
        
        full_greeting = f"Hi\n{greeting} \n{compliment}"
        self.greeting_label.config(text=full_greeting)
        self.tk.after(60000, self.update_greeting)  # Update every minute


class Weather(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, bg=background_color)
        self.temperature = ''
        self.currently = ''
        self.icon = ''
        self.name = ''
        
        # Icon and label
        self.iconLbl = tk.Label(self, bg=background_color)
        self.iconLbl.grid(row=0, column=0, sticky="e", padx=20, pady=10) 
        
        self.currentlyLbl = tk.Label(self, font=(text_font, medium_text_size), fg=text_color, bg=background_color)
        self.currentlyLbl.grid(row=0, column=1, sticky="w", padx=20, pady=10)  
        
        # Temperature
        self.degreeFrm = tk.Frame(self, bg=background_color)
        self.degreeFrm.grid(row=1, column=0, columnspan=2, sticky="e", pady=10)  
        self.temperatureLbl = tk.Label(self.degreeFrm, font=(text_font, large_text_size), fg=text_color,
                                       bg=background_color)
        self.temperatureLbl.pack(side=tk.RIGHT, anchor=tk.E)
        
        # Create a frame to hold additional weather information labels
        self.weather_info_frame = tk.Frame(self, bg=background_color)
        self.weather_info_frame.grid(row=2, column=0, columnspan=2, sticky="e", padx=20, pady=10)  

        # Additional Labels for new data
        self.sunriseLbl = tk.Label(self.weather_info_frame, font=(text_font, small_text_size), fg=text_color, bg=background_color)
        self.sunriseLbl.pack(side=tk.TOP, anchor=tk.E, padx=20)
        self.sunsetLbl = tk.Label(self.weather_info_frame, font=(text_font, small_text_size), fg=text_color, bg=background_color)
        self.sunsetLbl.pack(side=tk.TOP, anchor=tk.E, padx=20)
        self.windLbl = tk.Label(self.weather_info_frame, font=(text_font, small_text_size), fg=text_color, bg=background_color)
        self.windLbl.pack(side=tk.TOP, anchor=tk.E, padx=20)
        self.uvLbl = tk.Label(self.weather_info_frame, font=(text_font, small_text_size), fg=text_color, bg=background_color)
        self.uvLbl.pack(side=tk.TOP, anchor=tk.E, padx=20)
        
        self.get_weather()




    def get_weather(self):
        try:
            url = f'https://api.openweathermap.org/data/2.5/weather?id={weather_city_id}&units={weather_unit}&appid={weather_api_token}'
            print(f"Requesting weather data from: {url}")
            resp = requests.get(url)
            temp = resp.json()
            pprint.PrettyPrinter(indent=4).pprint(temp)

            self.degree_sign = u"\N{DEGREE SIGN}" + 'C'
            temperature = f"{temp['main']['temp']} {self.degree_sign}"
            current = temp['weather'][0]['description']
            icon = temp['weather'][0]['icon']

            icon_path = icon_lookup.get(icon, None)
            if icon_path:
                print(f"Looking for weather icon at: {icon_path}")
                image = Image.open(icon_path)
                image = image.resize((100, 100), Image.BICUBIC)
                photo = ImageTk.PhotoImage(image)
                self.iconLbl.config(image=photo)
                self.iconLbl.image = photo
            else:
                print(f"No icon found for: {icon}")

            self.temperatureLbl.config(text=temperature)
            self.currentlyLbl.config(text=current.upper())

            # New data extraction
            sunrise = time.strftime('%H:%M', time.gmtime(temp['sys']['sunrise'] + temp['timezone'])) 
            sunset = time.strftime('%H:%M', time.gmtime(temp['sys']['sunset'] + temp['timezone'])) 
            wind_speed = f"{temp['wind']['speed']} m/s"
            uv_url = f'https://api.openweathermap.org/data/2.5/uvi?lat={temp["coord"]["lat"]}&lon={temp["coord"]["lon"]}&appid={weather_api_token}'
            uv_resp = requests.get(uv_url)
            uv_data = uv_resp.json()
            uv_index = uv_data['value']

            self.sunriseLbl.config(text=f"Sunrise: {sunrise}")
            self.sunsetLbl.config(text=f"Sunset: {sunset}")
            self.windLbl.config(text=f"Wind Speed: {wind_speed}")
            self.uvLbl.config(text=f"UV Index: {uv_index}")


        except Exception as e:
            print(f"No internet, cannot get weather. {e}")

        self.after(600000, self.get_weather)

if __name__ == '__main__':
    w = FullscreenWindow()
    w.tk.mainloop()
