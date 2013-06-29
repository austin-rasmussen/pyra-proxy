from pyramid.response import Response
from pyramid.view import view_config

import requests

from .models import (
    DBSession,
    MyModel,
    )

class HomeView(object):
	def __init__(self, request):
		self.request = request

	@view_config(route_name='home', renderer='templates/mytemplate.pt')
	def mirror(self):
		request_url = self.request.path_info[1:]
		content = requests.get('http://%s' % request_url)
		return Response(content.content, headers={'Content-Type': content.headers['content-type']})
