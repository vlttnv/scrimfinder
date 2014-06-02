from jinja2 import Markup

class momentjs(object):
    def __init__(self, timestamp):
        self.timestamp = timestamp

    def render(self, format):
        return Markup("<script>\ndocument.write(moment(\"%s\").%s);\n</script>" % (self.timestamp.strftime("%Y-%m-%dT%H:%M:%S Z"), format))

    def renderTimezone(self, timezone, format):
        return Markup("<script>\ndocument.write(moment.tz(\"%s\", \"%s\").%s);\n</script>" % (self.timestamp.strftime("%Y-%m-%dT%H:%M:%S Z"), timezone, format))

    def format(self, fmt):
        return self.render("format(\"%s\")" % fmt)

    def formatTimezone(self, timezone, fmt):
        return self.renderTimezone("\"%s\"" % timezone, "format(\"%s\")" % fmt)

    def calendar(self):
        return self.render("calendar()")

    def fromNow(self):
        return self.render("fromNow()")