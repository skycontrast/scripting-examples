# Purpose    : Display lists of wildlife observations and allow for entry of new observations
# Date       : December 4th 2019
# Written By : Del Bello, R


#===========================================================================
# Function: menu()
# Purpose : Display the menu of options and request a choice from the user.
#===========================================================================
def menu():

    # Present the menu until a valid choice is entered.
    choice = 0
    while choice < 1 or choice > 7:
        print "\n\n\t Wildlife information Management"
        print "\t======== Selection Menu ========="
        print "\t================================="
        print "\t1. Show all Observations"
        print "\t2. Show Observations by a Person"
        print "\t3. Show Observations of a Species"
        print "\t4. Add an Observation"
        print "\t5. Add an Observer"
        print "\t6. Add a Species"
        print "\t7. Exit"

        # A non-number will be set to zero.  (Causing the menu to show again)
        try:
            choice = raw_input("\n\tEnter your selection: ")
            if choice == "":
                choice = 0
            else:
                choice = int(choice)
        except:
            print "\n\t%s is not valid\n" % choice
            choice = 0

    # Return the number entered.
    return choice
    
#===========================================================================
# Functions: display_all() , get_person(), display_species()
#===========================================================================

#==============================================
# Function : display_all()
# Purpose  : display all observation entries
#============================================
def display_all():
    #open record file in read mode
    infile = open('wildlife.txt','r')
    
    #print out header for displaying data
    print"\n\tObserver     Time Date           Town           Lat  Long   Species"
    print"\t%s" % ('-'*70)

    #for every entry found in the file
    for entry in infile:
        entry = entry.replace('"','').rstrip('\n')                       # replace double quotes with empty string, string new line
        entry = entry.split(',')                                         # split string into a list                                         
        entry[-3],entry[-2] = float(entry[-3]),float(entry[-2])          # convert lat and long values into float 
        
        #print data for when the entry contained a date with a comma
        if len(entry) == 8:                                              # if the list had 8 elements, ie. the date was split with a comma
            date = entry[2] + entry[3]                                   # put them back together
            print "\t%-11s%6s %-14s%   -14s% -5.2f  %-5.2f  %-7s" %(entry[0],entry[1],date,entry[4],entry[5],entry[6],entry[7])

        #if not, print all entries
        else:
            print "\t%-11s%6s %-14s%   -14s% -5.2f  %-5.2f  %-7s"%(entry[0],entry[1],entry[2],entry[3],entry[4],entry[5],entry[6])
    #close file
    infile.close()
      

#=========================================================================
# Function : display_name()
# Purpose  : display observations of a specific person
# Arguments: none
#  Rafael
#=========================================================================
def display_name():
    #open file
    infile = open('wildlife.txt','r')                         # open file in read mode

    #print header for data display
    print"\n\tObserver     Time Date          Town           Lat  Long   Species"
    print"\t%s" % ('-' * 70)

    #for every entry found in the file
    for entry in infile:                                          # for each observation entries in file
        entry = entry.replace('"','').rstrip('\n')                # remove '"' and strip new line
        entry = entry.split(',')                                  # split into list items at commas
        entry[-3], entry[-2] = float(entry[-3]), float(entry[-2]) # convert string lat/long into floats



        #if value at index 0 , the name, is the same as the name selection from get_person()
        
        if entry[0] == names[n-1]:                            
            if len(entry) == 8:                              
                #and there was a comma in the date, merge them
                date = entry[2] + entry[3]                  
                #print for that statement
                print "\t%-11s%6s %-14s%-12s% -5.2f  %-5.2f  %-7s" % (entry[0], entry[1], date, entry[4], entry[5], entry[6], entry[7])

            # if date not separated, print all values normaly
            else:
                print "\t%-11s%6s %-14s%-12s% -5.2f  %-5.2f  %-7s" % (entry[0], entry[1], entry[2], entry[3], entry[4], entry[5], entry[6])

    #close infile
    infile.close()

#========================================================================================
# Function: display_sp()
# Purpose : display all observations of a particular specie
#========================================================================================


def display_sp():

    #open file in read mode 
    infile = open('wildlife.txt', 'r')

    #print header for display
    print"\n\tObserver     Time Date          Town           Lat  Long   Species"
    print"\t%s" % ('-' * 70)

    # for every lines in the file
    for entry in infile:                                           # for each observation entries in file
        entry = entry.replace('"', '').rstrip('\n')                # remove '"' and strip new line
        entry = entry.split(',')                                   # split into items at commas
        entry[-3], entry[-2] = float(entry[-3]), float(entry[-2])  # convert string lat/long into floats


        #if the last item of line, the specie, is the same as specie selection for get_specie()
        if entry[-1] == species[n-1]:  
            #and if the lengh of items is 8
            if len(entry) == 8:                                      #if data entry contained comma, merge and call date
                date = entry[2] + entry[3]
                print "\t%-11s%6s %-14s%  -12s% -5.2f  %-5.2f  %-7s" % (entry[0], entry[1], date, entry[4], entry[5], entry[6], entry[7])

            # if date not separated, print all values normaly
            else:

                print "\t%-11s%6s %-14s%  -12s% -5.2f  %-5.2f  %-7s" % (entry[0], entry[1], entry[2], entry[3], entry[4], entry[5], entry[6])
    #close infile           
    infile.close()
#===========================================================================
# Function : in_list()
# Purpose  : Check if the value s is in the list.
# Arguments: s    - the selected item (A person or species)
#            list - the list to check (List of people or species)
#===========================================================================
def in_list(s,list):

    # For each list item, check of it matches the text value s
    match = False
    for item in list:
        if s.upper() == item.upper(): #   if a match is found:
            match = True              #   set the boolean to True
            break                     #   and stop looking any further

    # Return True or False (That it was found)
    
    return match
            
#===========================================================================
# Function: load_names()
# Purpose : Populate the names list with all the people in the file
#===========================================================================
def load_names():
    global names

    # If the list of names is already populated, the try: action will succeed
    # and the names will not be read again.
    # If the names haven't been loaded yet, the exception will be run to load
    # the names from the file.
    try:
        x = names[0]
    except:
        names = []

        infile = open("wildlife.txt","r")      #RAF -- CHANGED FILE DIRECTORY TO CURRENT
        for data in infile:
            f = data.split(",")                # f is all the fields
            name = f[0].strip('"')             # f[0] is the name
            if not in_list(name,names):        # if not in the list append it
                names.append(name)

        

#===========================================================================
# Function: get_person()
# Purpose : Show the names and get a selection from the list.
#===========================================================================
def get_person():
    global n   # make n global so it can be used in other functions

    load_names()                               # Build the list of names

    print "\n\tThese are the current names"
    print "\t==========================="

    # Show the names each with a number (1 greater than the index)
    for name in names:
        print "\t\t%d. %s" % (names.index(name)+1,name)

    # Get a number within the valid range
    n = 0
    while n < 1 or n > len(names):
        try:
            n = raw_input("\n\tChoose a number : ")
            n = int(n)
            
            # Force the exception if the number is not out of range.

            if n < 0 or n > len(names):
                x = int("A")
        except:
            print "Choose from 1 to %d" % (len(names))
    
        
    # Return the index number for the name selected
    # - (1 less than the number entered.)
    
    return n - 1
    #display_name()   ##RAF added
    

#===========================================================================
# Function: load_species()
# Purpose : Populate the list of species
#===========================================================================
def load_species():
    global species

    # Similar to load_names(), the exception will populate the list of species
    try:
        x = species[0]
    except:
        species = []

        infile = open("wildlife.txt","r")

        for data in infile:
            data = data.replace('"','')
            data = data.strip('\n')
            f = data.split(",")                # f is all the fields       
            sp = f[len(f)-1]                   # The last field is the species
            if not in_list(sp,species):        # if not in the list append it
                species.append(sp)

        
        
#===========================================================================
# Function: get_species()
# Purpose : Display the species and get a selection.
#===========================================================================
def get_species():
    global n

    load_species()                             # Build the list of species

    print "\n\tThese are the current Species"
    print "\t============================="

    # Show the species

    for sp in species:
        print "\t\t%d. %s" % (species.index(sp)+1,sp)

    # Repeat until a valid number is entered.
    
    n = 0
    while n < 1 or n > len(species):
        try:
            n = raw_input("\n\tChoose a number : ")
            n = int(n)
            
            # If out of range, force an error to show the exception.

            if n < 0 or n > len(species):
                x = int("A")
        except:
            print "Choose from 1 to %d" % (len(species))

    # Return the index for the selected species.

    return n - 1



#=============================================================================
# Function: hasNumber()
# Purpose: function will return True is a number is in a string, false if not
#=============================================================================

# function that will return TRUE when string contains numeric types ( any char ) and False if not
# will be used for validation when asking for user input for observations
def hasNumbers(inputString):
     return any(char.isdigit() for char in inputString)


#===========================================================================
# Function: add_observation()
# Purpose : Add an observation entry to the file.
#===========================================================================
def add_observation():
    
    # open file in append mode    
    outfile = open('wildlife.txt', 'a')

    # Show current list of observer by calling load_namnes()
    # User input for observer  with function get_person()
    print "\tSelect the name from the list of current observer: "
    load_names()
    get_person()

    # Show current species in file -->load_species()
    # And get specie selection from user -->get_specie()

    load_species()
    get_species()

    
    #=====================================
    # obtain input for time of observation

    goodTime = False             # initialise boolean as False
    while goodTime == False:     # while goodTime is False, ask for time to be entered
        try:
            time = raw_input("\tEnter a time: ")
            timecheck = int(time[0])                # will return False if first character not digit
            if timecheck >= 0 and len(time) >= 4:   # if first char was a digit, and lenght greater than 4 char minimum is "1:25"
                goodTime = True
                
            else:                
                print"\t Please enter a valid time format."         # if len < 4 print
        except:
            print" \tPlease enter a valid time."                    # if error occurs in te int conversion print


    #===================================
    # obtain date input for observation

    goodDate = 0
    #run loop while goodDate is 0
    while goodDate == 0:

        #promt for date of observation
        date = raw_input("\tEnter the date of observation(mm/dd/yy): ") 
        if hasNumbers(date) == True and len(date) >= 8 :                # if date contains number and is 8 character or longer
            goodDate = 1                                                # date is good
        else:
            print"\tPlease enter a valid date format."                  # invalid prompt for date again
    

    #==================================
    # obtain town input for observation


    
    goodTown = False                               # initialise good time as False and run the loop

    while goodTown == False:                       # town valid if non numeric AND  not empty string AND does not contain comma
        town = raw_input("\tEnter a town:")
        if hasNumbers(town) == False and town != "" and ',' not in town:
            goodTown = True                                               #end loop if town is valid
        else:
            print"\tPlease enter a valid town name."                      #otherwise prompt user about invalid entry




    #=====================================
    # Add Lat and Long

    goodLatLong = False                                               # initialise boolean as false
    while goodLatLong == False:                                       # while false run the loop
        try:
            lat  = float(input("\tEnter the latitude coordinates:"))  # convert input into Float to validate numeric time
            Long = float(input("\tEnter longitude coordinates:"))
            goodLatLong = True                                        # stop loop if conversion was sucessfill and no errors was raised
        except (ValueError, NameError, SyntaxError):
            print "\tPlease enter valid lat/long coordinates. For example 45.00 and 35.45."


    
    # write new observation to file

    outstring = '"%s","%s","%s","%s","%.2f","%.2f","%s"\n' % (names[n-1],time,date, town, lat, Long, species[n-1])
    outfile.write(outstring)
    # print"\n\tThank you, the observation was added to the file. You have been returned to the menu"

    outfile.close()

    #=======================================
    # Prompt user for another observation

    again = raw_input("\tWould you like to add another observation? (Y/N): ")

    # If user enters y__
    if again[0].upper() == "Y":       # convert first index of imput string to upper case
        add_observation()             # call add_observation() if user wants to add another observation
    else:
        print ""
        print ""
        
        display_all()                 # otherwise show user all observations with new entry inside

#===========================================================================
# Function: add_observer()
# Purpose : Add a name to the observer list.
#===========================================================================
def add_observer():
    load_names()                               # Build the list of names

    print "Current Observer names"
    print "="*22

    
    for name in names:
        print "\t%s" % name
    
    while in_list(name,names):
        name = raw_input("Enter the new name: ")
        if in_list(name,names):
            print "That name is already in the list"

    names.append(name)

#===========================================================================
# Function: add_species()
# Purpose : Add a species to the species list
#===========================================================================
def add_species():
    load_species()                               # Build the list of species

    print "Current Observer names"
    print "="*22

    
    for sp in species:
        print "\t%s" % sp

    # Get the species and append to the list
    # Prevent entry of an existing species
    
    while in_list(sp,species):
        sp = raw_input("Enter the new species: ")
        if in_list(sp,species):
            print "That species is already in the list"

    species.append(sp)
    
#===========================================================================
# Function: main()
# Purpose : Get the selection from the menu and call the function associated
#           with the choice
#===========================================================================
def main():
    
    # Call the menu function to show the options
    command = 1
    while command > 0 and command < 7:
        
        # Get the selection from the menu and call the corresponding function
        command = menu()


        ###################################################################
        # Assignment:
        #    - Complete the actions for selections 1, 2, 3, and 4
        ###################################################################
        if command == 1:
            display_all()# Call function to display all observations_raf
           

        elif command == 2:
            get_person()# Call function to: Select a person
            display_name()# Call function to: Display observations for the person
            
            
        elif command == 3:
            get_species()  # Call function to: Select a species
            display_sp()    # Call function to: Display observations of a species   RAF
            
            
        elif command == 4:
            add_observation()# Call function to: Add a new observation entry
            
            
        elif command == 5:             
            add_observer()             # Add a person to the list
            
        elif command == 6:
            add_species()              # Add a species to the list

    
#
#===========================================================================
# Mainline:
# Purpose : Start the process by callin the main function
#===========================================================================
main()