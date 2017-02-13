#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import cgi
import re
import os
import jinja2

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(template_dir),
    autoescape=True)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)
    
    def render_str(self, templates, **params):
        t = jinja_env.get_template(templates)
        return t.render(params)
    
    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))


class BlogsDB(db.Model):
    blogtitle = db.StringProperty(required = True)
    blogpost = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)

class MainHandler(Handler):
    def render_index(self, blogtitle="", blogpost="", error=""):
        blogs = db.GqlQuery("SELECT * from BlogsDB ORDER BY created Desc")

    def get(self):
        #self.response.write('Hello world!')
        self.render("index.html")
    
    def post(self):
        blogtitle = self.request.get("blogtitle")
        blogpost = self.request.get("blogpost")

        if blogtitle and blogpost:
            blogs = BlogsDB(blogtitle=blogtitle, blogpost=blogpost)
            blogs.put()
            self.redirect("/")
        else:
            error = "Excuse me, but something seems to be missing"
            self.render_index(blogtitle, blogpost, error)

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
