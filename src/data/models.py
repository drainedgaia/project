class User:
    def __init__(self, first_name, last_name, email):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.gpa = None
        self.courses = []

class Course:
    def __init__(self, name, grade):
        self.name = name
        self.grade = grade
