# wti-json
A class that contains common wti json functions

# Current functions:

print_information(): Prints out the user's URL, URL Extras, username, and password

change_url(): Changes the URL

change_url_suffix(): Changes the url extras

change_username(): Changes the username

change_password(): Change the password

get_tempertaure(no_format=False): Returns the temperature of the box OPTIONAL: no_format: If set to true then it will include the format of the temperature (F,C)

get_alarms(): Retruns the alarms of the box

get_hostname(): Returns the hostname of the box

get_location(): Returns the location of the box

get_current(): Returns a list of all currents in the box

get_voltage(): Returns a list of all voltages in the box

get_wattage(): Returns the wattage of the box

get_version(): Returns a list of the firmware and family version of the box

