from decorator import lazy_with_validation
from utilurl import level_to_one
from collections import namedtuple
import requests

class Moodle(object):
    
    resources_ = {
        'books': ('book', True),
        'chats': ('chat', True),
        'choices': ('choice', True),
        'databases': ('data', True),
        'feedbacks': ('feedback', True),
        'folders': ('folder', True),
        'forums': ('forum', False),
        'glossaries': ('glossary', True),
        'imscps': ('imscp', True),
        'labels': ('label', True),
        'lessons': ('lesson', True),
        'ltis': ('lti', True),
        'pages': ('page', True),
        'quizzes': ('quiz', True),
        'resources': ('resource', True),
        'scorms': ('scorm', True),
        'surveys': ('survey', True),
        'urls': ('url', True),
        'wikis': ('wiki', True),
        'workshops': ('workshop', True),
    }

    def __init__(self, url, token=None, username=None, password=None):
        super().__init__()
        self.url = url
        self.__token = token
        self.__privatetoken = None
        self.__username = username
        self.__password = password
        self.__login()

    def __getattr__(self, attr):
        env, sub = Moodle.resources_.get(attr, (None, None))
        if env and isinstance(sub, bool):
            wsf = 'mod_' + env + '_get_' + attr + '_by_courses'
            value = self.call(wsf)[attr] if sub else self.call(wsf)
            setattr(self, attr, value)
            return value
        cname = self.__class__.__name__
        raise AttributeError("'" + cname + "' object has no attribute '" + attr + "'")

    def __getattribute__(self, attr):
        env, sub = Moodle.resources_.get(attr, (None, None))
        value = super().__getattribute__(attr)
        if env and isinstance(sub, bool) and value == None:
            wsf = 'mod_' + env + '_get_' + attr + '_by_courses'
            value = self.call(wsf)[attr] if sub else self.call(wsf)
            setattr(self, attr, value)
        return value

    def __login(self):
        if not self.__token:
            if self.__username and self.__password:
                params = {
                    'username': self.__username,
                    'password': self.__password,
                    'service': 'moodle_mobile_app',
                }
                response = requests.get(self.url_login, params=params)
                response.raise_for_status()
                response = response.json()
                if response.get('error'):
                    errorcode = response['errorcode']
                    errormsg = response['error']
                    raise Exception(errorcode + ':' + errormsg)
                self.__token = response['token']
                self.__privatetoken = response['privatetoken']
            else:
                raise Exception('you must provide a user token and password')

    # reinventar si se logra hacer funcionar __getattribute__
    def __clear_lazy_properties(self):
        for attr in Moodle.resources_.keys():
            setattr(self, attr, None)

    @property
    def url_login(self):
        return self.url + '/login/token.php'

    @property
    def url_server(self):
        return self.url + '/webservice/rest/server.php'

    def login(self, username, password):
        self.__clear_lazy_properties()
        self.__username = username
        self.__password = password
        self.__token = None
        self.__login()

    @property
    def token(self):
        return self.__token

    @token.setter
    def token(self, value):
        self.__clear_lazy_properties()
        self.__username = None
        self.__password = None
        self.__token = value

    def params(self, wsfunction, moodlewsrestformat='json'):
        params = {
            'wstoken': self.__token,
            'wsfunction': wsfunction,
            'moodlewsrestformat': moodlewsrestformat
        }
        return params

    def call(self, wsfunction, **kwargs):
        """Calls moodle API function with function name wsfunction and keyword
           arguments.
        Example:
        >>> moodle.call('core_course_update_courses',
               courses=[{'id': 1, 'fullname': 'My favorite course'}])
        """
        params = self.params(wsfunction)
        params.update(level_to_one(kwargs))
        response = requests.get(self.url_server, params=params)
        response.raise_for_status()
        response = response.json()
        if isinstance(response, dict) and response.get('exception'):
            raise SystemError("Error calling Moodle API\n", response)
        return response

    @property
    @lazy_with_validation
    def info(self):
        response = self.call('core_webservice_get_site_info')
        Info = namedtuple('Info', response.keys())
        info = Info(**response)
        return info

    @property
    @lazy_with_validation
    def courses(self):
        userid = self.info.userid
        wsfunction = 'core_enrol_get_users_courses'
        return self.call(wsfunction, userid=userid)

    def resources_by_course(self, course):
        courseids = [course.get('id')]
        wsfunction = 'mod_resource_get_resources_by_courses'
        return self.call(wsfunction, courseids=courseids)
    
    def get_user_by_id(self, userid):
        values = [userid]
        wsfunction = 'core_user_get_users_by_field'
        users = self.call(wsfunction, field='id', values=values)
        user = users[0] if users else None
        return user

