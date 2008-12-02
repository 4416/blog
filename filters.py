import hashlib
import BeautifulSoup
import datetime
from django.template.defaultfilters import timesince
from django.conf import settings
from google.appengine.ext.webapp import template

register = template.create_template_register()

UTC_OFFSET = getattr(settings, "UTC_OFFSET", 0)

def bettertimesince(dt):
    delta = datetime.datetime.utcnow() - dt
    local_dt = dt + datetime.timedelta(hours=UTC_OFFSET)
    if delta.days == 0:
        return timesince(dt) + " ago"
    elif delta.days == 1:
        return "Yesterday" + local_dt.strftime(" at %I:%M %p")
    elif delta.days < 5:
        return ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"][local_dt.weekday()] + local_dt.strftime(" at %I:%M %p")
    elif delta.days < 365:
        return local_dt.strftime("%B %d at %I:%M %p")
    else:
        return local_dt.strftime("%B %d, %Y")

register.filter(bettertimesince)

@register.filter
def body_parse(entry):
    """Parse a body and replace its 
    <media> tags with equivalent HTML markup"""
    soup = BeautifulSoup.BeautifulSoup(entry.body)
    mediatags = soup.findAll('media')
    for tag in mediatags:
        tag.replaceWith('hah')
    return soup

@register.filter
def hashit(text):
    """generate an id"""
    return hashlib.md5(text).hexdigest()[:10]

def noprotocol(url):
    return url.replace('http://www.', '').replace('http://', '')


@register.filter
def mediaparam(url):
    "returns a param for players"

    if noprotocol(url).startswith('youtube.com'):
        param = url.replace('watch?v=', '/v/')
    if noprotocol(url).startswith('seesmic.com'):
        urlparts = url.split('/')
        param = urlparts[-1]
    if noprotocol(url).startswith('vimeo.com'):
        urlparts = url.split('/')
        param = urlparts[-1]


    return param


