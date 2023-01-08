from datetime import datetime

class Course(object):

    def __init__(self, course):
        self.id = course.get('id')
        self.fullname = course.get('fullname')
        self.shortname = course.get('shortname')

    def __str__(self):
        return (
            'id: ' + str(self.id) + ', ' +
            'fullname: ' + self.fullname + ', ' +
            'shortname: ' + self.shortname
        )

