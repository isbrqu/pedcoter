from datetime import datetime
import telegram
from telegram.utils.helpers import escape_markdown as escape


class Resource(object):

    def __init__(self, resource):
        self.name = resource.get('name')
        self.fileurl = resource.get('contentfiles')[0].get('fileurl')
        self.fileurl = self.fileurl.replace('https://', '')
        self.fileurl = self.fileurl.replace('webservice/', '')
        self.timemodified = resource.get('timemodified')
        self.datetime = str(datetime.fromtimestamp(self.timemodified))

    @property
    def as_message(self):
        return (
            self.name + '\n\n' +
            self.fileurl + '\n\n' +
            self.datetime
        )

