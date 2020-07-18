import time
import json
import subprocess
import os

# Root directory of Exported Facebook data
export_dir = '/Users/ezrahill/Downloads/facebook-ezrahills/'

os.chdir(export_dir)

# Target DayOne Journal
journal = 'Facebook'

class fb_post():
    def __init__(self):
        self.date = ""
        self.data = ""
        self.title = ""
        self.uri = ""
        self.tags = ""
        self.loc = ""

    def update_dayone (self):
        dayone_params = ["dayone2",
                        "new", self.title, self.data,
                        "-t", self.tags,
                        "-d", self.date]  # "-j", journal
        if not self.uri == "":
            dayone_params.append("--photos")
            dayone_params.append(self.uri)

        if not self.loc == "":
            dayone_params.append("--coordinate")
            dayone_params.append(self.loc)
        # dayone_params.append("new")
        # if not self.title == "":
        #     dayone_params.append(self.title)
        # dayone_params.append(self.data)
        subprocess.run(args=dayone_params)
    def get_date(self, timestamp):
        self.date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))

    # with open('posts/notes.json', 'r') as f:
    #     notes_dict = json.load(f)
    #     for note in notes_dict['notes']:
    #         print(note['title'])

    def get_tags(self, post):
        if 'tags' in post:
            tags = post['tags']
            tag_data = ""
            for tag in tags:
                tag_data += tag + " "
            self.tags = tag_data

    def get_title(self, post):
        if 'title' in post:
            self.title = post['title']

    def get_attachment(self, post):
        attachments = post['attachments']
        for attachment in attachments:
            # print(attachment)
            data = attachment['data'][0]
            if not 'external_context' in data:
                timestamp = post['timestamp']
                self.get_date(timestamp)
                self.get_title(post)
            #print(data)
            if 'media' in data:
                self.uri = data['media']['uri']
            # if 'external_context' in data:
            #     if 'title' in post:
            #         print('Title = ' + post['title'])
            if 'place' in data:
                self.get_location(data)

            if not 'external_context' in data:
                if 'data' in post:
                    self.get_post(post)
        # for attchment in post['attachment']:
        #     print(attchment['post'])

    def get_post(self, post):
        data = post['data']
        timestamp = post['timestamp']
        for post in data:
            if 'post' in post:
                obj.get_date(timestamp)
                obj.data = post['post']

    def get_location(self, data):
        place = data['place']
        if 'coordinate' in place:
            loc = place['coordinate']
            loc_data = []
            for val in loc.values():
                r_val = round(val, 3)
                loc_data.append(str(r_val))
            self.loc = loc_data[0] + " " + loc_data[1]
        # if 'name' in place:
        #     print(place['name'])


with open(f'{export_dir}posts/your_posts_1.json', 'r') as f:
    posts_dict = json.load(f)
    for post in posts_dict:
        obj = fb_post()
        if 'attachments' in post:
            obj.get_attachment(post)
        elif 'data' in post:
            obj.get_post(post)
        obj.get_tags(post)
        if obj.date:
            print(obj.__dict__)
            obj.update_dayone()