import os, re, sys
from ruxit.api.base_plugin import BasePlugin
from ruxit.api.selectors import HostSelector
from subprocess import check_output

class hostSessionCountPlugin(BasePlugin):
	def query(self, **kwargs):
		
		host_id =  self.query_snapshot.host_id
		
		if (sys.platform.startswith("win")):
			result = check_output("quser", shell=True)
			output = result.decode(encoding='utf-8')
			self.results_builder.absolute(key="sessionCount",value=len(output.splitlines())-1,entity_id=host_id)

		elif (sys.platform.startswith("linux")):
			result = check_output("who -q", shell=True)
			output = result.decode(encoding='utf-8')
			session_search = re.search('users=([0-9]+)', output, re.IGNORECASE)
			if session_search:
				self.results_builder.absolute(key="sessionCount",value=session_search.group(1),entity_id=host_id)
