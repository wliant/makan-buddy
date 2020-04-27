# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 20:42:33 2020

@author: darry
"""

import tagui as t

#Sample Values
reservation_date = "16/07/2020"
reservation_time = "1730"
party_size = "2"
restaurant_name ='Yujin Izakaya'
first_name = 'John'
last_name='Tan'
email_address = 'test@gmail.com'
phone_number = '98769876'
    
def make_reservation(reservation_date,reservation_time,party_size,restaurant_name,first_name,last_name,email_address,phone_number):
    try:
        #Convert User Defined Values to System Usable Values
        reservation_day=reservation_date.split('/')[0]
        reservation_month =reservation_date.split('/')[1]
        reservation_month=int(reservation_month)-1
        reservation_year =reservation_date.split('/')[2]
        reservation_time_int=int(reservation_time)
        start_time_hr= reservation_time[:2]
        if reservation_time_int>1159:
            if start_time_hr!="12":
                start_time_hr=int(start_time_hr)-12
            start_time_option = str(start_time_hr)+":"+reservation_time[2:4]+" pm"
        else:
            start_time_option = str(start_time_hr)+":"+reservation_time[2:4]+" am"
            
        #Booking Parameters
        chope_url ='https://www.chope.co/singapore-restaurants/category/restaurant/'
        t.init()
        t.url(chope_url)
        t.wait(10)
        #Date Field
        t.click(f"(//span[contains(@class,'input-group-addon icon-calendar')])[1]")
        t.wait(10)
        t.click('//a[@title="Next"]')
        t.wait(5)
        t.click('//a[@title="Next"]')
        t.click(f"//td[@data-handler='selectDay'and @data-month='{reservation_month}']/a[text()='{reservation_day}']")
        #Time Field
        t.select(f"//select[contains(@id,'time-field')]",start_time_option)
        #Number of Diners Field
        t.click(f"(//span[contains(@class,'input-group-addon icon-person')])[1]")
        t.select(f"//select[contains(@id,'adults')]",party_size)
        #Restaurant Field
        t.type(f"//select[contains(@id,'sb-sel-restaurant')]",restaurant_name)
        t.click('//button[@id="btn-search"]')
        t.wait(5)
        
        #Secondary Page to Confirm Timing
        t.click(f"//a[contains(@rname,'{restaurant_name}') and text()='{start_time_option}']")
        t.wait(5)
        t.click(f"//input[@id='btn_sub' and @value='Book Now']")
        t.wait(5)
        
        #Booking Confirmation
        t.popup('https://book.chope.co/')
        #First Name
        t.type('//input[@id="forename"]',first_name)
        #Last Name
        t.type('//input[@id="surname"]',last_name)
        #Email
        t.type('//input[@id="email"]',email_address)
        #Phone Number
        t.type('//input[@id="telephone"]',phone_number)
        #Agree Terms & Conditions
        t.click(f"//input[@name='agree_term_conditions']")
        #Confirm Booking
        t.click(f"//button[@id='check_book_now']")
        t.wait(5)
        t.close()
        print('Success')
        
    except:
        print('Error')
        
        
make_reservation(reservation_date,reservation_time,party_size,restaurant_name,first_name,last_name,email_address,phone_number)