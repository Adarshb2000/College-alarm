from selenium.webdriver import Firefox
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from credentials import username, password
from datetime import datetime as dt, timedelta as td

class CollegeAlarm:
    def __init__(self, username, password):
        # Initialize
        self.base_url = 'https://hello.iitk.ac.in/'
        self.driver = Firefox()
        self.driver.get(self.base_url + 'user/login')

        # Login
        self.login(username, password)

        # Find Courses
        self.courses_code = []
        self.get_courses()

        
        # Getting assignments
        assignments = {}
        for course in self.courses_code[ -1 : 5 : -1]:
            assignments[course] = self.get_assignments(course)
        
        self.driver.quit()
        
        print(assignments)

    def login(self, username, password):
        self.driver.find_element_by_id('edit-name').send_keys(username)
        self.driver.find_element_by_id('edit-pass').send_keys(password)
        self.driver.find_element_by_id('edit-submit').click()

    def get_courses(self):
        self.driver.get(self.base_url + 'courses')
        courses = self.driver.find_elements_by_tag_name('h3')
        self.courses_code = [course.text.split(':')[0].lower() for course in courses]

    def get_assignments(self, course):
        self.driver.get(self.base_url + course + '/#/home')
        class_name = 'assignmentItemNotSubmitted'
        ignored_exceptions = (NoSuchElementException, StaleElementReferenceException)
        assignments_elem = WebDriverWait(self.driver, 5, ignored_exceptions=ignored_exceptions)\
                                .until(expected_conditions.presence_of_all_elements_located((By.CLASS_NAME, class_name)))
        assignments = []
        for assignment in assignments_elem:
            type_, date = assignment.text.split('\n')
            if type_.startswith('Tutorial'): continue
            date = dt.strptime(date[7 :].strip(), '%d/%m/%Y %H:%M')
            if dt.today() + td(7) > date > dt.today():
                assignments.append(type_)
        assignments_elem = None
        return assignments


CollegeAlarm(username, password)


