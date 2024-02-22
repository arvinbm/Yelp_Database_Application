import pyodbc
import random
import string
from datetime import datetime

# Create a connection  to the database
myCon = pyodbc.connect('driver={ODBC Driver 18 for SQL Server};server=cypress.csil.sfu.ca;uid=s_aba191;pwd=3jGPNPMQn4Q4ef7F;Encrypt=yes;TrustServerCertificate=yes')

def login():
    userID = input("Enter your user ID: ")
    userIDcur = myCon.cursor()
    userIDcur.execute('select USER_ID from user_yelp')
    results = userIDcur.fetchone()

    while results:
        if (userID == results[0]):
            break
        results = userIDcur.fetchone()

    #check if the userID provided is valid
    while (not results):
        print("===========================================")
        print("The user ID provided is invalid")
        userID = input("Enter your user ID: ")

        userIDcur.execute('select USER_ID from user_yelp')
        results = userIDcur.fetchone()

        while results:
            if (userID == results[0]):
                break
            results = userIDcur.fetchone()
    return userID
            

def showMenu():

    print("===========================================")
    print("Select a functionality from the list below:")
    print("1. Search a Business")
    print("2. Search a User")
    print("3. Make a Friend")
    print("4. Write a Review")
    print("5. Quit the program")
    selectedOption = input("Enter the option's corresponding number: ")


    # Check if the string provided is a number
    try:
        int(selectedOption)
    except:
        print("The string provided cannot be converted into a number.")
        selectedOption = input("Please provide a number (1-4): ")

    # Check if the selected number is valid
    while (int(selectedOption) != 1 and int(selectedOption) != 2 and int(selectedOption) != 3 and int(selectedOption) != 4 
    and int(selectedOption) != 5):
        print("===========================================")
        print("Invalid selected option!")
        print("Select a functionality from the list below:")
        print("1. Search a Business")
        print("2. Search a User")
        print("3. Make a Friend")
        print("4. Write a Review")
        selectedOption = input("Enter the option's corresponding number: ")

        # Check if the string provided is a number
        try:
            int(selectedOption)
        except:
            print("The string provided cannot be converted into a number.")
            selectedOption = input("Please provide a number (1-4): ")

    return selectedOption

def mainMenu(userID):
    print("===========================================")
    selectedOption = showMenu()
    
    # Call the funtion which corresponds to the selected option provided by the user
    if (int(selectedOption) == 1):
        searchBusiness(userID)

    elif (int(selectedOption) == 2):
        searchUser(userID) 

    elif (int(selectedOption) == 3):
        makeFriend(userID)

    elif (int(selectedOption) == 4):
        writeReview(userID)

    elif (int(selectedOption) == 5):
        print("Goodbye!")
        myCon.close
        exit()

def CheckValidInput(filterOption):
    # Check if the string provided is a number
    try: 
        int(filterOption)
    except:
        print("The string provided cannot be converted into a number.")
        filterOption = input("Please provide a number (1-4): ")

    while (int(filterOption) != 1 and int(filterOption) != 2 and int(filterOption) != 3 and int(filterOption) != 4 ):
        print("===========================================")
        print("Invalid selected option!")
        print("Select a filter from the list below:")
        print("1. Search the businesses with minimum number of stars.")
        print("2. Search the businesses with maximum number of stars.")
        print("3. Search businesses by their city name.")
        print("4. Search businesses by their name (or part of their name).")
        filterOption = input("Select one of the corresponding numbers: ")

        # Check if the string provided is a number
        try: 
            int(filterOption)
        except:
            print("The string provided cannot be converted into a number.")
            filterOption = input("Please provide a number (1-4): ")

    return filterOption


def CheckIfTheFilterWasSelected(filterOptionList, filterOption):
    for i in range(len(filterOptionList)):
        if filterOptionList[i] == int(filterOption):
            return False
    return True

def validateFilterOption(filterOption):
    try:
        int(filterOption)
    except:
        return False
    return True

def printFiltersForBusinesses():
    print("===========================================")
    print("1. Search the businesses with minimum number of stars.")
    print("2. Search the businesses with maximum number of stars.")
    print("3. Search businesses by their city name.")
    print("4. Search businesses by their name (or part of their name).")
    filterOption = input("Select a filter from the above list:")

    # Check if the filter selecetd is between 1 - 4
    while (not validateFilterOption(filterOption) or (int(filterOption) < 1 or int(filterOption) > 4)):
        print("===========================================")
        print("The filter option you have selected is invalid.")
        print("The number must be between 1 - 4")
        print("===========================================")
        filterOption = input("Select a filter from the above list:")

    return filterOption
    
def listContainsNumber(filterOptionList, number):
    for i in range(len(filterOptionList)):
        if filterOptionList[i] == number:
            return True
    return False

def printResultsBusinessSearch(results, resultsCur):
    while results:
        print("===========================================")
        print("Business ID: " + results[0])
        print("Name of the business: " + results[1])
        print("Address of the business: " + str(results[2]))
        print("City of the business: " + results[3])
        print("Number of stars: " + str(results [4]))
        results = resultsCur.fetchone()

def handleEmptyResults(results):
    if results is None:
        print("No results were found based on the selected filter, name of the city, or name of the business.")

def resultsBasedOnFilters(filterOptionList, nameCity, nameBusiness):

    # Retrieve the appropriate data based on the filters selected by the user
    if (len(filterOptionList) == 1 and listContainsNumber(filterOptionList, 1)):
        print("===========================================")
        print("Retreiving data (Businesses with minimum number of stars)")
        print("===========================================")
        resultsCur = myCon.cursor()
        resultsCur.execute('select business_id, name, address, city, stars ' + 
                           'from business where stars = (select min(stars) from business) order by name')
        results = resultsCur.fetchone()
        printResultsBusinessSearch(results, resultsCur)
        handleEmptyResults(results)

    elif (len(filterOptionList) == 1 and listContainsNumber(filterOptionList, 2)):
        print("===========================================")
        print("Retreiving data (Businesses with maximum number of stars)")
        print("===========================================")
        resultsCur = myCon.cursor()
        resultsCur.execute('select business_id, name, address, city, stars ' + 
                           'from business where stars = (select max(stars) from business) order by name')
        results = resultsCur.fetchone()
        printResultsBusinessSearch(results, resultsCur)
        handleEmptyResults(results)

    elif (len(filterOptionList) == 1 and listContainsNumber(filterOptionList, 3)):
        print("===========================================")
        print("Retreiving data (Businesses in " + nameCity + ")")
        print("===========================================")
        resultsCur = myCon.cursor()

        resultsCur.execute('select business_id, name, address, city, stars ' + 
                           'from business where city = ? order by name', nameCity)
        results = resultsCur.fetchone()
        printResultsBusinessSearch(results, resultsCur)
        handleEmptyResults(results)

    elif (len(filterOptionList) == 1 and listContainsNumber(filterOptionList, 4)):
        print("===========================================")
        print("Retreiving data (Businesses with name " + nameBusiness + ")")
        print("===========================================")
        resultsCur = myCon.cursor()

        resultsCur.execute('select business_id, name, address, city, stars ' +
                           'from business where name like ? order by name', '%' + nameBusiness + '%')
        results = resultsCur.fetchone()
        printResultsBusinessSearch(results, resultsCur)
        handleEmptyResults(results)

    elif (len(filterOptionList) == 2 and listContainsNumber(filterOptionList, 1)
          and listContainsNumber(filterOptionList, 2)):
        print("===========================================")
        print("Retreiving data (Businesses with maximum and minimum number of stars)")
        print("===========================================")
        resultsCur = myCon.cursor()

        resultsCur.execute('select business_id, name, address, city, stars ' +
                           'from business ' +
                           'where stars = (select min(stars) from business) or stars = (select max(stars) from business)' +
                           'order by name')
        results = resultsCur.fetchone()
        printResultsBusinessSearch(results, resultsCur)
        handleEmptyResults(results)

    elif (len(filterOptionList) == 2 and listContainsNumber(filterOptionList, 1)
          and listContainsNumber(filterOptionList, 3)):
        print("===========================================")
        print("Retreiving data (Businesses with minimum number of stars in " + nameCity + ")")
        print("===========================================")
        resultsCur = myCon.cursor()

        resultsCur.execute('select business_id, name, address, city, stars ' +
                           'from business ' +
                           'where stars = (select min(stars) from business where city = ?) and city = ? order by name'
                           , [nameCity, nameCity])
        results = resultsCur.fetchone()
        printResultsBusinessSearch(results, resultsCur)
        handleEmptyResults(results)

    
    elif (len(filterOptionList) == 2 and listContainsNumber(filterOptionList, 1)
          and listContainsNumber(filterOptionList, 4)):
        print("===========================================")
        print("Retreiving data (Businesses with minimum number of stars with name " + nameBusiness + ")")
        print("===========================================")
        resultsCur = myCon.cursor()

        resultsCur.execute('select business_id, name, address, city, stars ' +
                           'from business ' +
                           'where stars = (select min(stars) from business where name like ?) and name like ? order by name', 
                           ['%' + nameBusiness + '%', '%' + nameBusiness + '%'])
        results = resultsCur.fetchone()
        printResultsBusinessSearch(results, resultsCur)
        handleEmptyResults(results)

    elif (len(filterOptionList) == 2 and listContainsNumber(filterOptionList, 2)
          and listContainsNumber(filterOptionList, 3)):
        print("===========================================")
        print("Retreiving data (Businesses with maximum number of stars in " + nameCity + ")")
        print("===========================================")
        resultsCur = myCon.cursor()

        resultsCur.execute('select business_id, name, address, city, stars ' +
                           'from business ' +
                           'where stars = (select max(stars) from business where city = ?) and city = ? order by name', 
                           [nameCity, nameCity])
        results = resultsCur.fetchone()
        printResultsBusinessSearch(results, resultsCur)
        handleEmptyResults(results)


    elif (len(filterOptionList) == 2 and listContainsNumber(filterOptionList, 2)
          and listContainsNumber(filterOptionList, 4)):
        print("===========================================")
        print("Retreiving data (Businesses with maximum number of stars with name " + nameBusiness + ")")
        print("===========================================")
        resultsCur = myCon.cursor()

        resultsCur.execute('select business_id, name, address, city, stars ' +
                           'from business ' +
                           'where stars = (select max(stars) from business where name like ?) and name like ? order by name',
                            ['%' + nameBusiness + '%', '%' + nameBusiness + '%'])
        results = resultsCur.fetchone()
        printResultsBusinessSearch(results, resultsCur)
        handleEmptyResults(results)


    elif (len(filterOptionList) == 2 and listContainsNumber(filterOptionList, 3)
          and listContainsNumber(filterOptionList, 4)):
        print("===========================================")
        print("Retreiving data (Businesses in " + nameCity + " with the name " + nameBusiness + ")")
        print("===========================================")
        resultsCur = myCon.cursor()

        resultsCur.execute('select business_id, name, address, city, stars ' +
                           'from business ' +
                           'where city = ? and name like ? order by name', (nameCity, '%' + nameBusiness + '%'))
        results = resultsCur.fetchone()
        printResultsBusinessSearch(results, resultsCur)
        handleEmptyResults(results)
    
    elif (len(filterOptionList) == 3 and listContainsNumber(filterOptionList, 1)
          and listContainsNumber(filterOptionList, 2) and listContainsNumber(filterOptionList, 3)):
        print("===========================================")
        print("Retreiving data (Businesses with maximum and minimum number of stars in " + nameCity + ")")
        print("===========================================")
        resultsCur = myCon.cursor()

        resultsCur.execute('select business_id, name, address, city, stars ' +
                           'from business ' +
                           'where (stars = (select min(stars) from business where city = ?) or stars = (select max(stars) from business where city = ?))' +
                           'and city = ? order by name', [nameCity, nameCity, nameCity])
        results = resultsCur.fetchone()
        printResultsBusinessSearch(results, resultsCur)
        handleEmptyResults(results)

    elif (len(filterOptionList) == 3 and listContainsNumber(filterOptionList, 1)
          and listContainsNumber(filterOptionList, 2) and listContainsNumber(filterOptionList, 4)):
        print("===========================================")
        print("Retreiving data (Businesses with maximum and minimum number of stars with name = " + nameBusiness)
        print("===========================================")
        resultsCur = myCon.cursor()

        resultsCur.execute('select business_id, name, address, city, stars ' +
                           'from business ' +
                           'where (stars = (select min(stars) from business where name like ?) or stars = (select max(stars) from business where name like ?))' +
                           'and name like ? order by name', ['%' + nameBusiness + '%', '%' + nameBusiness + '%', '%' + nameBusiness + '%'])
        results = resultsCur.fetchone()
        printResultsBusinessSearch(results, resultsCur)
        handleEmptyResults(results)

    elif (len(filterOptionList) == 3 and listContainsNumber(filterOptionList, 1)
          and listContainsNumber(filterOptionList, 3) and listContainsNumber(filterOptionList, 4)):
        print("===========================================")
        print("Retreiving data (Businesses with minimum number of stars in " + nameCity + " with name " + nameBusiness + ")")
        print("===========================================")
        resultsCur = myCon.cursor()

        resultsCur.execute('select business_id, name, address, city, stars ' +
                           'from business ' +
                           'where stars = (select min(stars) from business where name like ? and city = ?) and name like ? ' +
                           'and city = ? order by name', ('%' + nameBusiness + '%', nameCity, '%' + nameBusiness + '%', nameCity  ))
        results = resultsCur.fetchone()
        printResultsBusinessSearch(results, resultsCur)
        handleEmptyResults(results)

    elif (len(filterOptionList) == 3 and listContainsNumber(filterOptionList, 2)
          and listContainsNumber(filterOptionList, 3) and listContainsNumber(filterOptionList, 4)):
        print("===========================================")
        print("Retreiving data (Businesses with maximum number of stars in " + nameCity + " with name " + nameBusiness + ")")
        print("===========================================")
        resultsCur = myCon.cursor()

        resultsCur.execute('select business_id, name, address, city, stars ' +
                           'from business ' +
                           'where stars = (select max(stars) from business where name like ? and city = ?) and name like ? ' +
                           'and city = ? order by name', ('%' + nameBusiness + '%', nameCity,'%' + nameBusiness + '%', nameCity))
        results = resultsCur.fetchone()
        printResultsBusinessSearch(results, resultsCur)
        handleEmptyResults(results)

    elif (len(filterOptionList) == 4 and listContainsNumber(filterOptionList, 1)
          and listContainsNumber(filterOptionList, 2) and listContainsNumber(filterOptionList, 3) and listContainsNumber(filterOptionList, 4)):
        print("===========================================")
        print("Retreiving data (Businesses with maximum and minimum number of stars in " + nameCity + " with name " + nameBusiness + ")")
        print("===========================================")
        resultsCur = myCon.cursor()

        resultsCur.execute('select business_id, name, address, city, stars ' +
                           'from business ' +
                           'where (stars = (select max(stars) from business where name like ? and city = ? ) ' +
                           'or stars = (select min(stars) from business where name like ? and city = ?)) and name like ? ' +
                           'and city = ? order by name', 
                           ('%' + nameBusiness + '%', nameCity, '%' + nameBusiness + '%', nameCity, '%' + nameBusiness + '%', nameCity))
        results = resultsCur.fetchone()
        printResultsBusinessSearch(results, resultsCur)
        handleEmptyResults(results)

def printFiltersForTheUser(userFilterOptionList):
    wishesToIncludeNameInTheSearch = ''
    nameToSearch = ''
    wishesToIncludeUseful = ''
    wishesToIncludeFunny = ''
    wishesToIncludeCool = ''

    # Get input on whether the user wishes to include a name in their search 
    print("===========================================")
    wishesToIncludeNameInTheSearch = input("Do you wish to include the name of the user in your search? (yes/no): ").upper()
    if (wishesToIncludeNameInTheSearch != 'NO'):
        userFilterOptionList.append(1)
        nameToSearch = input("Enter the name of the user you wish to search (Or part of the name): ").upper()
    else:
        userFilterOptionList.append(0)

    # Get input on whether the user wishes to include useful users in their search  
    print("===========================================")  
    wishesToIncludeUseful = input("Do you wish to search the users that are useful? (yes/no): ").upper()
    if(wishesToIncludeUseful != 'NO'):
        userFilterOptionList.append(2)
    else: 
        userFilterOptionList.append(0)

    # Get input on whether the user wishes to include useful in their search
    print("===========================================")
    wishesToIncludeFunny = input("Do you wish to search the users that are funny? (yes/no): ").upper()
    if(wishesToIncludeFunny != 'NO'):
        userFilterOptionList.append(3)
    else:
        userFilterOptionList.append(0)

    # Get input on whether the user wishes to include useful in their search
    print("===========================================")
    wishesToIncludeCool = input("Do you wish to search the users that are cool? (yes/no): ").upper()
    if(wishesToIncludeCool != 'NO'):
        userFilterOptionList.append(4)
    else:
         userFilterOptionList.append(0)

    return nameToSearch

def constructTheQuery(userFilterOptionList):
    query = 'select user_id, name, useful, funny, cool, yelping_since from user_yelp where '

    # The case where a name is included in the search
    if (listContainsNumber(userFilterOptionList, 1)):
        query += 'name like ? '
    
    # The case where usefulness is included in the search
    if(listContainsNumber(userFilterOptionList, 2)):
        if (listContainsNumber(userFilterOptionList, 1)):
            query += 'and useful > 0 '
        else:
            query += 'useful > 0 '

    # The case where funniness is included in the search
    if(listContainsNumber(userFilterOptionList, 3)):
        if (listContainsNumber(userFilterOptionList, 1) or listContainsNumber(userFilterOptionList, 2)):
            query += 'and funny > 0 '
        else:
            query += 'funny > 0 '


    # The case where coolness is included in the search
    if(listContainsNumber(userFilterOptionList, 4)):
        if(listContainsNumber(userFilterOptionList, 1) or listContainsNumber(userFilterOptionList, 2)
           or listContainsNumber(userFilterOptionList, 3)):
            query += 'and cool > 0 '
        else:
            query += 'cool > 0 '
    
    query += ' order by name'

    return query

def printResultsForUserSearch(results, userSearchCur):
    while results:
        print("===========================================")
        print("ID of the user: " + results[0])
        print("Name of the user: " + results[1])
        print("Useful: " + str(results[2]))
        print("Funny: " + str(results[3]))
        print("Cool: " + str(results[4]))
        print("The user has been yeslping since: " + str(results[5]))
        results = userSearchCur.fetchone()

def executeQuery(query, nameToSeach): 
    userSearchCur = myCon.cursor()

    # The case where a name is included for a search
    if (nameToSeach != ''):
        userSearchCur.execute(query, '%' + nameToSeach + '%')
        results = userSearchCur.fetchone()
    
    # The case where a name is not included for a search
    else:
        userSearchCur.execute(query)
        results = userSearchCur.fetchone()

     #Check if the result is empty
    if results is None:
        print("No results were found based on the selected filter, name of the city, or name of the business.")

    else:
        printResultsForUserSearch(results, userSearchCur)


def searchBusiness(userID):
    # Decalre an array that holds numbers corresponding to the selecetd options
    filterOptionList = []
    nameCity = ''
    nameBusiness = ''

    filterOption = printFiltersForBusinesses() 

    #Check if the provided option is valid
    if(CheckValidInput(filterOption)):
        filterOptionList.append(int(filterOption))
        if (int(filterOption) == 3):
            nameCity = input("Enter the name of the city: ").upper()
        elif (int(filterOption) == 4): 
            nameBusiness = input("Enter the name of the business (or part of the name): ").upper()

    # Ask the user if they wish to add more filters
    wishesToAddMoreFilters = input("Do yo wish to select more filters? (Yes/No) ").upper()

    # Check if the input provided is valid
    while (wishesToAddMoreFilters != 'YES' and wishesToAddMoreFilters != 'NO'):
        print("===========================================")
        print("Please choose between Yes or No.")
        print("===========================================")
        wishesToAddMoreFilters = input("Do yo wish to select more filters? (Yes/No) ").upper()

    while(wishesToAddMoreFilters == 'YES'):
        filterOption = printFiltersForBusinesses()

        # Check if the user have already selecetd the filter
        while(not CheckIfTheFilterWasSelected(filterOptionList, filterOption)):
             print("You have already selected this filter.")
             filterOption = printFiltersForBusinesses()

        filterOption = CheckValidInput(filterOption)
        filterOptionList.append(int(filterOption))

        # Prompt the user for a city name or a business name if option 3 or 4 are selected
        if (int(filterOption) == 3):
            nameCity = input("Enter the name of the city: ").upper()

        elif (int(filterOption) == 4): 
            nameBusiness = input("Enter the name of the business (or part of the name): ").upper()
        
        # Check if the user has not selected all the filters yet
        if(len(filterOptionList) < 4):
            wishesToAddMoreFilters = input("Do yo wish to select more filters? (Yes/No) ").upper()

            # Check if the input provided is valid
            while (wishesToAddMoreFilters != 'YES' and wishesToAddMoreFilters != 'NO'):
                print("===========================================")
                print("Please choose between Yes or No.")
                print("===========================================")
                wishesToAddMoreFilters = input("Do yo wish to select more filters? (Yes/No) ").upper()

        else:
            print("You have selected all four filters!")
            wishesToAddMoreFilters = 'NO'

    # provoke the appropriate SQL query for each selected filter
    if (nameCity == '' and nameBusiness == ''):
        resultsBasedOnFilters(filterOptionList, '', '')

    elif (nameCity != '' and nameBusiness == ''):
        resultsBasedOnFilters(filterOptionList, nameCity, '')

    elif(nameCity == '' and nameBusiness != ''):
        resultsBasedOnFilters(filterOptionList, '', nameBusiness)

    else:
        resultsBasedOnFilters(filterOptionList, nameCity, nameBusiness)
    
    mainMenu(userID)

def validateExistingFriendship(userID, userIDofTheFriend):
    curValidateFriendshipExists = myCon.cursor()
    curValidateFriendshipExists.execute('SELECT user_id, friend FROM friendship')
    results = curValidateFriendshipExists.fetchone()

    while results:
        if (userID == results[0] and userIDofTheFriend == results[1]):
            return True
        results = curValidateFriendshipExists.fetchone()

    return False


def updateTheFriendship(userID, userIDofTheFriend):
    curInsertingFriendship = myCon.cursor()

    # Check if the frinendship is already recorded in the database
    if (validateExistingFriendship(userID, userIDofTheFriend)):
        print("===========================================")
        print("This frindship is already recorded in the database.")
        return 

    commandForInsertingFriendship = ("INSERT INTO friendship(user_id, friend) VALUES(?,?)")
    values = [userID,userIDofTheFriend]

    curInsertingFriendship.execute(commandForInsertingFriendship, values)

    myCon.commit()
    print("===========================================")
    print("Your frienship was successfuly recorded.")

        
def searchUser(userID):
    userFilterOptionList = []

    nameToSearch = printFiltersForTheUser(userFilterOptionList)
    query = constructTheQuery(userFilterOptionList)
    executeQuery(query, nameToSearch)
    mainMenu(userID)

def validateIDExists(userIDofTheFriend):
    curValidateUserID = myCon.cursor()
    curValidateUserID.execute('SELECT USER_ID FROM user_yelp')
    results = curValidateUserID.fetchone()

    while results:
        if (userIDofTheFriend == results[0]):
            return True
        results = curValidateUserID.fetchone()

    return False
    
def makeFriend(userID):

    userIDofTheFriend = input("Enter the ID of the user you wish to be friends with: ")

    # Validate if the ID provided existsin the database
    while (not validateIDExists(userIDofTheFriend)):
        print("=======================================================")
        print("The ID of the user provided does not exist in the database.")
        print("=======================================================")
        userIDofTheFriend = input("Enter the ID of the user you wish to be friends with: ")

    updateTheFriendship(userID, userIDofTheFriend)
    mainMenu(userID)


def validateNumberOfStars(numberOfStars):

    # Validate if the number is an integer
    try: 
        int(numberOfStars)
    except:
        print("=======================================================")
        print('The number provided must be an integer.')
        return False

    if (int(numberOfStars) > 5 or int(numberOfStars) < 1):
        return False
    else: 
        return True

def validateBusinessExists(businessIDReview):
    curValidateBusiness = myCon.cursor()
    curValidateBusiness.execute('SELECT business_id FROM business')
    results = curValidateBusiness.fetchone()

    while results: 
        if (businessIDReview == results[0]):
            return True
        results = curValidateBusiness.fetchone()

    return False

def generateRandomReviewID():
    # generate random string of length 22 with upper case and lower case letters
    randomReviewID = ''.join(random.choice(string.ascii_letters)
    for i in range(22))

    return randomReviewID

def validateReviewIDExists(generatedRandomInterviewID):
    curValidateInterviewID = myCon.cursor()
    curValidateInterviewID.execute('SELECT review_id FROM review')
    results = curValidateInterviewID.fetchone()

    while results:
        if (generatedRandomInterviewID == results[0]):
            return False
        results = curValidateInterviewID.fetchone()

    return True


def insertTheReview(userID, businessIDReview, numberOfStars, generatedRandomReviewID, dateAndTime):
    curInsertingReview = myCon.cursor()

    commandForInsertingTheReview = ("INSERT INTO review(review_id, user_id, business_id, stars, " +
    "useful, funny, cool, date) VALUES(?,?,?,?,0,0,0,?)")
    values = [generatedRandomReviewID, userID, businessIDReview, numberOfStars, dateAndTime]

    curInsertingReview.execute(commandForInsertingTheReview, values)

    myCon.commit()
    print("===========================================")
    print("Your review was inserted successfuly!")

def writeReview(userID):

    businessIDReview = input("Enter the ID of the business you wish to review: ")

    # validate that the business ID entered does not exist in the database
    while (not validateBusinessExists(businessIDReview)):
        print("=======================================================")
        print("The business ID of the business provided does not exist in the database.")
        print("=======================================================")
        businessIDReview = input("Enter the ID of the business you wish to review: ")

    numberOfStars = input ("Enter the number of stars you wish to give to this business (1-5): ")

    # Validate that the number of the star provided by the user is an integer between 1 and 5
    while (not validateNumberOfStars(numberOfStars)):
        print("=======================================================")
        print("The number of stars entered must be between 1 to 5.")
        print("=======================================================")
        numberOfStars = input ("Enter the number of stars you wish to give to this business (1-5): ")

    generatedRandomReviewID = generateRandomReviewID()

    # Validate that generated random review ID does not already exist in the database
    while (not validateReviewIDExists(generatedRandomReviewID)):
        generatedRandomReviewID = generateRandomReviewID()

    # Get the time and date of the review
    dateAndTime = datetime.now()

    insertTheReview(userID, businessIDReview, numberOfStars, generatedRandomReviewID, dateAndTime)
    mainMenu(userID)
    

def main():
    userID = login()
    mainMenu(userID)
    myCon.close

if __name__ == """__main__""":
    main()
    