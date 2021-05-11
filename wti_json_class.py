import requests

class WTIJson:
    """A class that contains common WTI json information"""
    def __init__(self, url='', url_suffix='', username='',password='', selftest=False):
        """Initializes defaults for Json stuff
        Leave blank to default to rest.wti.com
        url (String: 'https://rest.wti.com/'): The url you want to get json from
        url_suffix (String: 'api/v2/'): The path to the specific json you want to get (THIS SHOULDN'T CHANGE)
        username (String: 'restpowerpublic'): The username to login
        password (String: 'restfulpassword'): The password to login
        selftest (Bool: False): Tests to see if the initial entered information is correct (Should be used in debug environment and not for production)
        """
        self.URL_LINK = 'https://rest.wti.com/' if len(url) == 0 else url
        self.URL_EXTRAS = 'api/v2/' if len(url_suffix) == 0 else url_suffix
        self.USERNAME = "restpowerpublic" if len(username) == 0 else username
        self.PASSWORD = "restfulpassword" if len(password) == 0 else password

        if selftest:
            self._self_test()

    def _self_test(self):
        """Tests gets a json from the specified server"""
        r = requests.get(
            self.URL_LINK + self.URL_EXTRAS + "firmware",
            auth=(self.USERNAME, self.PASSWORD),
            verify=True
        )

        if r.status_code != 200:
            print(f'Connection error to {self.URL_LINK} status code: {r.status_code}')
        else:
            whole_json = r.json()
            try:
                json_status = whole_json['status']['code']
            except KeyError:
                print('Connection sucessful, but could not extract \'okay\' code from json')
                print(whole_json)
            else:
                json_status = int(json_status)
                if json_status == 0:
                    print('Self-test completed sucessfully')

    def _get_json(self, suffix=''):
        """Gets a json from the webserver and returns it"""
        r = requests.get(
            self.URL_LINK + self.URL_EXTRAS + suffix,
            auth=(self.USERNAME, self.PASSWORD),
            verify=True
        )
        return r.json()

    def print_information(self):
        """Prints URL, URL EXTRAS, USERNAME, and PASSWORD"""
        print(f'URL: {self.URL_LINK}')
        print(f'URL EXTRAS: {self.URL_EXTRAS}')
        print(f'USERNAME: {self.USERNAME}')
        print(f'PASSWORD: {self.PASSWORD}')

    def change_url(self, url):
        """Change the url"""
        print(f'Changed {self.URL_LINK} to {url}')
        self.URL_LINK = url

    def change_url_suffix(self, url_suffix):
        """Change the url suffix"""
        print(f'Changed {self.URL_EXTRAS} to {url_suffix}')
        self.URL_EXTRAS = url_suffix

    def change_username(self, username):
        """Change the username"""
        print(f'Changed {self.USERNAME} to {username}')
        self.USERNAME = username

    def change_password(self, password):
        """Change the password"""
        print(f'Changed {self.PASSWORD} to {password}')
        self.PASSWORD = password

    def get_temperature(self, no_format=False):
        """Gets the temperature from the json returned from the wti box
        Returns the temperature and format of temperature in a string
        Set no_format to True if you only want temperature back as a number, format will be truncated
        """
        whole_json = self._get_json('temperature')

        temperature = whole_json['temperature']
        temperature_format = whole_json['format']
    
        if not no_format:
            return temperature + temperature_format
        else:
            return int(temperature)

    def get_alarms(self, ):
        """Returns a list of all the alarms in the box with the statuses"""
        whole_json = self._get_json('alarms')
        
        alarms = whole_json['alarms']

        return alarms

    def get_hostname(self, ):
        """Returns the name of the box"""
        whole_json = self._get_json('hostname')

        hostname = whole_json['unitid']['hostname']

        return hostname

    def get_location(self, ):
        """Returns the location of the box"""
        whole_json = self._get_json('hostname')

        location = whole_json['unitid']['location']

        return location

    def get_current(self, ):
        """Returns a list of currents from the branches of the box"""
        whole_json = self._get_json('current')
        current_list = []

        for x in range(whole_json['branchcount']):
            tempdict = {f'branch{x}': whole_json[f'branch{x}']['current1']}
            current_list.append(tempdict)

        return current_list

    def get_power(self, ):
        # May need to look over this one again
        """Returns a list of voltages from the branches of the box"""
        whole_json = self._get_json('power')
        current_list = []

        for x in range(whole_json['branchcount']):
            tempdict = {f'branch{x}': whole_json[f'branch{x}']['voltage1']}
            current_list.append(tempdict)

        return current_list

    def get_wattage(self, ):
        """Returns the wattage of the box"""
        whole_json = self._get_json('current')
        volts = whole_json['branch1']['voltage1']
        current = whole_json['branch1']['current1']

        watts = volts * current

        return watts

    def get_version(self, ):
        """Returns a list of the firmware and family version that the box is under"""
        whole_json = self._get_json('firmware')
        current_list = [{'firmware': whole_json['config']['firmware'], 'family': whole_json['config']['family']}]

        return current_list

if __name__ == "__main__":
    # Simple test to get the temperature of the box
    wtiobj = WTIJson()
    wtitemp = wtiobj.get_temperature()

    print(f'The temperature is: {wtitemp}')