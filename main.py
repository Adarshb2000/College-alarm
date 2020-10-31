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
        
        course_codes, course_names = self.get_courses()

        
        # Getting assignments
        assignments = {}
        for course in course_codes:
            assignments[course] = self.get_assignments(course)
            
        
        
        print(assignments)

    def login(self, username, password):
        self.driver.find_element_by_id('edit-name').send_keys(username)
        self.driver.find_element_by_id('edit-pass').send_keys(password)
        self.driver.find_element_by_id('edit-submit').click()

    def get_courses(self):
        self.driver.get(self.base_url + 'courses')
        courses = self.driver.find_elements_by_tag_name('h3')
        courses = [course.text.split(':') for course in courses]
        return [course[0].strip().lower() for course in courses], [course[1].strip() for course in courses]

    def get_assignments(self, course):
        self.driver.get(self.base_url + course + '/#/home')
        self.driver.implicitly_wait(10)
        class_name = 'assignmentItemNotSubmitted'
        assignments_elem = self.driver.find_elements_by_class_name(class_name)
        if not len(assignments_elem): return []
        else:
            for assignment in assignments_elem: print(assignment.text)
            return []
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


