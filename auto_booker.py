from selenium import webdriver
from person import Person
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

import selenium
import datetime
import calendar
import csv


book_date = datetime.date.today() + datetime.timedelta(days=3)
book_day = book_date.day


def main():
    people = read_csv_to_list("people.csv")
    driver = webdriver.Firefox()
    driver.implicitly_wait(10)
    print("Loading library website...")
    driver.get('https://booking.lib.buffalo.edu/reserve/silverman')
    make_booking(driver, people)
    print("Bookings completed.")
    driver.quit()


# Function that reads .csv file of names and emails. Function stores that
# information in a list of Persons and returns the list.
#
# @params - filename: a string containing the name of a .csv file for reading
# @returns - people: a list of Persons containing necessary information for making bookings


def read_csv_to_list(filename):
    people = []
    with open(filename, encoding='utf-8-sig') as csv_file:  # Sets encoding standard to UTF-8 codec with BOM signature
        csv_reader = csv.reader(csv_file, delimiter=',')  # Creates csv reader with comma delimiter
        for row in csv_reader:
            people.append(Person(row[0], row[1], row[2], row[3]))  # Adds Persons to people
    return people


# Function that selects the proper date for room booking.
# Function will open up booking calendar and select the day
# three days after the current date. If the date rolls over to
# the next month, (i.e. it is from 1-3) the next month will be
# selected.
#
# @params - driver: webdriver containing current website information
# @returns - none


def select_date(driver):
    xpath_to_arrow = "//*[@id='eq-time-grid']/div[1]/div[1]/div/button[2]/span"
    driver.find_element_by_xpath(xpath_to_arrow).click()  # Selects arrow button


# Function that goes through the process of booking a library room.
# Function finds and submits desired times for booking, fills out
# booking form, and submits the form until no more Persons are in people.
#
# @params - driver: a webdriver containing current website information
#         - people: a list containing Person objects
# @returns - none


def make_booking(driver, people):

    weekday = calendar.day_name[book_date.weekday()]
    month = calendar.month_name[book_date.month]
    day = str(book_day)
    year = str(book_date.year)

    for person in people:

        select_date(driver)  # Selects desired date (3 days in advance)

        t = person.time

        try:
            xpath_book = "//a[@title='" + t + " " + weekday + ", " + month + " " + day + ", " + year + " - Room 06']"
            element = WebDriverWait(driver, 2.5).until(
                ec.element_to_be_clickable((By.XPATH, xpath_book)))
            element.click()  # Finds appropriate booking time and selects

            xpath_button = "//button[@id='submit_times']"
            element = WebDriverWait(driver, 1).until(ec.element_to_be_clickable((By.XPATH, xpath_button)))
            element.click()  # Clicks submit times
            print("Booking Room 6 on " + weekday + ", " + month + " " + day + ", " + year +
                  " for " + person.first + " " + person.last)

        except selenium.common.exceptions.TimeoutException:  # If Room 6 is already booked, book Room 7
            xpath_book = "//a[@title='" + t + " " + weekday + ", " + month + " " + day + ", " + year + " - Room 07']"
            element = WebDriverWait(driver, 2.5).until(ec.presence_of_element_located((By.XPATH, xpath_book)))
            element.click()

            xpath_button = "//button[@id='submit_times']"
            element = WebDriverWait(driver, 10).until(
                ec.element_to_be_clickable((By.XPATH, xpath_button)))
            element.click()

            print("Booking Room 7 on " + weekday + ", " + month + " " + day + ", " + year +
                  " for " + person.first + " " + person.last)

        driver.find_element_by_xpath("//button[@id='terms_accept']").click()  # Clicks button to accept terms

        driver.find_element_by_id("fname").send_keys(person.first)  # Fills out first name field
        driver.find_element_by_id("lname").send_keys(person.last)  # Fills out last name field
        driver.find_element_by_id("email").send_keys(person.email)  # Fills out email field
        driver.find_element_by_id("btn-form-submit").click()  # Submits form

        driver.get('https://booking.lib.buffalo.edu/reserve/silverman')  # Redirects to library reserve page


if __name__ == '__main__':
    main()
