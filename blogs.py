import os
import cgi
import webapp2
import jinja2
from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(template_dir),
    autoescape=True)

class BlogHandler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **parms):
        t = jinja_env.get_template(template)
        return t.render(parms)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class BlogsDB(db.Model):
    blogtitle=db.StringProperty(required=True)
    blogpost=db.TextProperty(required=True)
    created=db.DateTimeProperty(auto_now_add=True)

class MainPage(BlogHandler):
    def render_front(self, blogtitle="", blogpost="", error=""):
        dbpost=db.GqlQuery("SELECT * FROM BlogsDB ORDER BY created DESC LIMIT 5")
        self.render("index.html", blogtitle=blogtitle, blogpost=blogpost, error=error, dbpost=dbpost)

    def get(self):
        self.render_front()

class NewPost(BlogHandler):
    def render_newpost(self, blogtitle="", blogpost="", error=""):
        self.render("post.html", blogtitle=blogtitle, blogpost=blogpost, error=error)

    def get(self):
        self.render_newpost()

    def post(self):
        blogtitle=self.request.get("blogtitle")
        blogpost=self.request.get("blogpost")

        if blogtitle and blogpost:
            a=BlogsDB(blogtitle=blogtitle, blogpost=blogpost)
            a.put()
            self.redirect('/blog/$s' % str(a.key().id()))
        else:
            error="We need bth a title and a post, please"
            self.response.write.out(error)

class ViewPostHandler(BlogHandler):
    def get(self, id):
        int_id=int(id)
        id_num = BlogsDB.get_by_id(int_id)

        if id-num:
            self,render("post.html", id_num=id_num)
        else:
            error="<h1 color='red'>I did not find a post with that ID</h1>"
            self.response.write.out(error)

app = webapp2.WSGIApplication([
    ('/blog', MainPage),
    ('/newpost', NewPost),
    webapp2.Route('/blog/<id:\d+',)
])
