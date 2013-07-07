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
		request_full_url = 'http://%s?%s' % (request_url.split(':/', 1)[-1], self.request.query_string)
		
		if self.request.method == 'GET':
			content = requests.get(request_full_url, stream=True)
		elif self.request.method == 'POST':
			content = requests.post(request_full_url, stream=True, data=self.request.POST.mixed())
		headers = content.headers
		headers.pop('transfer-encoding', None)
		headers.pop('content-encoding', None)
		if headers.get('content-type', None) <> 'application/octet-stream':  headers.pop('content-length', None)
		return Response(app_iter=content.iter_content(chunk_size=512*1024), headers=headers)
