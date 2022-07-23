from getpass import getuser

import ngrok
from urllib.parse import urlparse


class NgrokWraper():

    def __init__(self, token):

        self.client = ngrok.Client(token)

        #used to identify if ssh, maincra or other thing is playing
        self.default_config = {
                                "ssh": {    "protocol": "tcp", 
                                            "port": [22],
                                            "formatter": self.format_to_ssh_connection,
                                            "user": ""
                                        }
                              }

#------------------------------------------------------#
#                       setters
#------------------------------------------------------#

    def set_ssh_user(self, 
                     username: str):

        self.default_config['ssh']['user'] = username



#------------------------------------------------------#
#                       formatters
#------------------------------------------------------#

                         
    def format_to_ssh_connection(self, **kwargs):
            
        user        = self.default_config['ssh']['user']
        port        = kwargs["port"]
        hostname    = kwargs["hostname"]

        if user == "":
           user = getuser() 

        return f"ssh -p {port} {user}@{hostname}"

#------------------------------------------------------#
#                       utils
#------------------------------------------------------#

    def parsed_url_to_dict(self, 
                           parsed_url):

        return {
                "hostname": parsed_url.hostname,
                "port":     parsed_url.port,
                "scheme":   parsed_url.scheme
               }
    

#------------------------------------------------------#
#               main functions
#------------------------------------------------------#


    def get_online_tunnels(self):

        connections = []

        # list all online tunnels
        for t in self.client.tunnels.list():
            print(f"public url:\t {t.public_url}")

            url_parsed  = urlparse(t.public_url)
            url_data    = self.parsed_url_to_dict(url_parsed)

            connect_str = self.default_config["ssh"]["formatter"](**url_data)
            connections.append(connect_str)

        txt = f"Available connections\nYou can connect with: "

        for connect_str in connections:
            txt += f"\n\t {connect_str}"

                
        return txt
    
            
# ngrokwraper = NgrokWraper()
# ngrokwraper.get_online_tunnels()


