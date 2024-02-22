# Program Functionality README

## Login
When the user first starts the program, they will be prompted to enter their user ID. If the entered user ID exists in the database, they will be shown the menu containing the functionalities of the program. Otherwise, they will be prompted to enter a valid user ID.

## Menu of Functionalities
The user has the following options:
1. Search a business based on filters which are explained later.
2. Search a user based on filters which are explained later.
3. Make a friendship.
4. Write a review for a business.
5. Quit the program.

If the user enters an invalid option, for example a number more than 5 or less than 1, or a string of characters, they will be asked to enter a valid option.

## Search a Business
A user has the option to select any combination of the following filters:
1. Businesses with the maximum number of stars.
2. Businesses with the minimum number of stars.
3. Search a business based on the name of the city they are located in.
4. Search a business based on the name of the business (or part of the name).

If the user selects an invalid option, they will be asked to enter a number between 1 and 4. Each time a user enters a valid option, they will be asked if they wish to select more options. They can answer with "yes" or "no" (case insensitive). Any order of selecting the filters is valid. If options 1 and 2 are selected, both the minimum and maximum number of stars will be printed on the terminal. When option 3 is selected, the user is asked to enter the name of the city (case insensitive). When option 4 is selected, the user can provide the name or part of the name of the business they wish to search. After any number or combination of filters, the result of the search is printed on the terminal. The user will be notified if the result is empty. The result is ordered by the name of the business.

## Search a User
A user has the option to select any combination of the following filters:
1. Search a user based on their name (or part of their name).
2. A useful user.
3. A funny user.
4. A cool user.

After selecting the filters, the result of the search will be shown on the terminal. The user will be notified if the search result is empty. The result is ordered by the name of the user.

## Make a Friendship
The user will be asked for the user ID of the user they wish to be friends with. If the user ID does not exist in the database, the user is notified and asked for another valid user ID. The user will be notified when the friendship is recorded in the database.

## Write a Review for a Business
The user will be asked to enter the ID of the business they wish to review. If the business ID does not exist in the database, the user is asked to enter another valid business ID. The user will be notified once the review has been recorded in the database.

After each of these functions returns the results, the menu of functions is shown again to the user.
