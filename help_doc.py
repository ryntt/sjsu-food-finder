# This is just a help documentation variable placed in another python
# module to make readability easier on the main bot module.

HELP_DOC = """
This Discord bot is designed to look for eateries within a mile of SJSU. 
All queries to this bot must start with "$sjsufood", followed by any of 
these arguments:

- help: brings up the help documentation, can also be brought up if 
        $sjsufood is inputted without any arguments\n
- find: (restaurant name): locates a restaurant and returns the 
        following information: name, address, phone number, 
        approximate distance from SJSU, and whether it is currently 
        open. Will only display a result if it contains all the 
        information. \n
One or more of the following:
- category(s): limit the search to a specific type of eatery.
        Multiple categories can be specified through a comma-delimited 
        string (ex. chinese,noodles). Note that there are no spaces 
        around the comma(s).
- n1-n10: display 1-10 eateries in the results depending on the 
        specified argument, default is 5
- r1.0-5.0: only show eateries greater than or equal to the rating 
        specified (anywhere from 1-5, 1 and 5 denoting lowest and 
        highest rated, respectively), default is 3.5
- p1-p4: only show eateries less than or equal to the price rating 
        specified (anywhere from 1-4, 1 and 4 denoting least and most
        expensive, respectively), default is 2
"""