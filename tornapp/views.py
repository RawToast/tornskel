from tornado.web import RequestHandler
from tornado import escape
import tornado.web
import tornado.auth

from couchdbkit import NoResultFound, Document

class HcBaseHandler(RequestHandler):
    mime_type = {
        'page':'text/html',
        'html':'text/html',
        'json':'application/json',
        }

    def get_current_user(self):
        email = self.get_secure_cookie("authed_user")
        if not email: return None
        return User.view('user/email',key=email).one()

    def __init__(self, application, request, **kwargs):
        Document.set_db(application.couchdb)
        RequestHandler.__init__(self, application, request)
        self.output = kwargs.get('output','page')
        self.set_header("Content-Type", self.mime_type[self.output])

    def ok(self, message=""):
        self.write(json.dumps({'status':'ok','message':message}))

    def fail(self, reason=None):
        if self.output == 'page':
            content = '<p class="error">Request failed: %s</p>'%reason
            return self.render("base.html", content=content)
        return self.write(json.dumps({'status': 'fail', 'reason': reason}))


class AuthLogoutHandler(HcBaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.set_secure_cookie('authed_user', '0')
        self.redirect("/")


class AuthHandler(HcBaseHandler):
    @tornado.web.asynchronous
    def get(self):
        self.render("auth/login.html")

    def post(self):
        if False:
            pass
        else:
            raise tornado.web.HTTPError(500, "auth failed")


class SignupHandler(HcBaseHandler):
    @tornado.web.asynchronous
    def get(self):
        self.render(
            "signup/start.html",
            )

    def post(self):
        pass


class SignupCompleteHandler(HcBaseHandler):
    @tornado.web.asynchronous
    def get(self):
        signup = self.get_secure_cookie("signup_user")
        self.clear_cookie("signup_user")
        # delete cookie?
        if signup:
            self.render("signup/complete.html", signup=signup)
        else:
            self.redirect("/signup")


class ActivateHandler(HcBaseHandler):
    @tornado.web.asynchronous
    def get(self, hash):
        if False:
            pass
        else:
            raise tornado.web.HTTPError(500, "unknown hash")


class HomeHandler(HcBaseHandler):
    @tornado.web.authenticated
    def get(self):
        data = {
            }
        self.render(
            "user/home.html",
            **data
            )


class IndexHandler(HcBaseHandler):
    def get(self):
        if self.current_user: self.redirect("/home")
        else: self.render("index.html")

