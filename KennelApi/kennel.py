import os
from datadog import api, initialize

'''
Author: Julian Levi Hernandez - May 19, 2020
'''


class Kennel:
    '''
    self.commands: is the registry tuple used to call functions
    self.api_key: is the os environment stored API Key
    self.app_key: is the os environment stored APP Key
    '''
    def __init__(self, cnffile):
        self.cnffile = cnffile
        # Globalize Dictionary of choices
        # Register the new endpoint and define the new function to expand KennelApi
        self.commands = {
            "all_hosts": self.allhosts,
            "create_dashboard": self.createdashboard
        }

        # Import OS env DATADOG API & APP keys
        self.apikey = os.getenv('DATADOG_API_KEY')
        self.appkey = os.getenv('DATADOG_APPLICATION_KEY')

        self.options = {
            'api_key': self.apikey,
            'app_key': self.appkey
        }
        initialize(**self.options)

    '''
    Name: readconf
    example: reads config/get_dashboard.conf file and extracts all key and values for the function getdashboard(self)
    '''
    def readconf(self):
        delim = "="
        conf = {}
        with open(self.cnffile) as f:
            for row in f:
                if delim in row:
                    k, v = row.split(delim, 1)
                    field = k.strip()
                    fieldval = v.strip()
                    conf[field] = fieldval
        return conf

    '''
    KennelApi defined functions to call DataDog API endpoints
    In this section the user must create the body of the endpoint call and make references to the readconf keys, values
    '''
    def allhosts(self):
        cnf = self.readconf()
        title = cnf['kennel.host.all.title']
        cmd = api.Hosts.search()
        return (title, ": ",cmd)

    def createdashboard(self):
        cnf = self.readconf()  #
        title = cnf['kennel.create.dashboard.title']
        widgets = [{
            'definition': {
                'type': cnf['kennel.create.dashboard.widgets.definition.type'],
                'requests': [
                    {'q': cnf['kennel.create.dashboard.widgets.definition.requests.q']}
                ],
                'title': cnf['kennel.create.dashboard.widgets.definition.title']
            }
        }]
        layout_type = cnf['kennel.create.dashboard.layout.type']
        description = cnf['kennel.create.dashboard.description']
        is_read_only = cnf['kennel.create.dashboard.read.only']
        notify_list = cnf['kennel.create.dashboard.notify.list']
        template_variables = [{
            'name': cnf['kennel.create.dashboard.template.var.name'],
            'prefix': cnf['kennel.create.dashboard.template.var.prefix'],
            'default': cnf['kennel.create.dashboard.template.var.default']
        }]

        saved_views = [{
            'name': cnf['kennel.create.dashboard.saved.view.name'],
            'template_variables': cnf['kennel.create.dashboard.saved.view.template.variables']
        }]

        cmd = api.Dashboard.create(title=title,
                             widgets=widgets,
                             layout_type=layout_type,
                             description=description,
                             is_read_only=is_read_only,
                             notify_list=notify_list,
                             template_variables=template_variables,
                             template_variable_presets=saved_views)

        return cmd

    '''
    Dynamically executes the endpoint based on the user cli input
    '''
    def execapi(self, argument):
        fun = self.commands[argument]()
        return fun
