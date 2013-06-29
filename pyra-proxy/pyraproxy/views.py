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
		# Split off the protocol
		content = requests.get('http://%s?%s' % (request_url.split(':/', 1)[-1], self.request.query_string), stream=True)
		headers = content.headers
		headers.pop('transfer-encoding', None)
		return Response(app_iter=content.iter_content(chunk_size=512*1024), headers=headers)
