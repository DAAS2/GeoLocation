Geo-Location Child Tracking App:

Project Description:
The goal of this project is to design and develop a child tracking app that utilizes geolocation technology to track the child for their parents to know where they are. Parents are also able to communicate with their child in real time. 

The App uses Django as the web framework, Python(Backend) and Javascript, HTML&CSS (Frontend)

Features of app:
Real-Time Location Tracking: The app uses GPS technology to track the child's location in real-time, allowing parents to view their child's current location on a map and this is done by using Google API.


Live Chat System: The app has a live chat system, which will let parents and children to communicate with each other in real-time.

Primary Goal:
Let the parents know about their childs location and to ensure their saftey incase something were to happen
The real-time location tracking feature will allow the parents to quickly locate their children in case of an emergency, 
The live chat system will help parents and children to stay connected throughout the day


File Structure and Functions:
Index.html:
    - This is the main page of the application where the users get personalised information depedening if they're a child or parent
    - If the user is a child then it will display a map view where the child's location is displayed
    - If the user is a parent then it will display a the details of the parent including, Name, ID, and also the Child associated with their account

login.html:
    - This is the login page for users
    - It takes in the username and password and checks if the user exists in the database
    - If the user exists then it logs them in and redirects them to the index page
    - If the user doesn't exist then it displays an error message

register.html:
    - This is the registration page for new users to create their account
    - It takes username, email, phone number and password and then registers the user
    - After registration it redirects the user to the index page
    - If the user already exists then it displays an error message
    - If the user doesn't fill all the fields then it will display an error message

findchild.html
    - This is the page where the parent can view the location of their child
    - It displays a map view with the child's location
    
findchild.html
    Description: A dedicated page for parents to locate their children within the application.
    Functions:
    Displays a comprehensive list of children associated with the parent's account.
    Offers search and filter functionalities to streamline the process of finding specific children.
    Includes a map view to visualize the child's location, along with real-time updates on their whereabouts
    

contact_child.html
    Description: The user interface for real-time communication between parents and children.
    Functions:
    Presents a visually appealing chat interface where parents and children can exchange messages instantly.
    Implements WebSocket technology to enable seamless, bidirectional communication between clients.


Database:
models.py
    Models.py contains the tables for users, parents, childern and chat messages



Functions in views.py:
    index():
    Description: This function renders the main page of the application.
    Functions:
    It retrieves user-specific information such as parent details, child details, and recent chat messages.
    Utilizes Django's template system to dynamically render personalized content based on the user's role.

find_child():
    Description: Renders the page for parents to locate their children.
    Functions:
    Queries the database to fetch children associated with the parent's account.
    Presents the list of children in a user-friendly format for easy navigation.

update_location():
    Description: Handles POST requests to update the location of a child.
    Functions:
    Extracts latitude and longitude data from the request payload.
    Updates the child's location in the database using Django's ORM.

contact_child():
    Description: Renders the page for real-time communication between parents and children.
    Functions:
    Retrieves parent, child, and chat message data from the database.
    Passes the retrieved data to the template for rendering the chat interface.

login_view(), logout_view(), register():
    Description: Functions responsible for user authentication and registration.
    Functions:
    Handle user login, logout, and registration processes.
    Implement authentication logic using Django's built-in authentication system.
    Functions in consumers.py:

ChatConsumer:
    Description: WebSocket consumer class managing live chat functionality.
    Functions:
    connect(): Handles WebSocket connection establishment.
    disconnect(): Handles WebSocket connection termination.
    receive(): Processes incoming WebSocket messages and broadcasts them to the chat group.
    sendMessage(): Sends chat messages to connected clients.

JavaScript Functions:
Chat() (index.html):
    Description: Initializes the chat functionality on the client-side.
    Functions:
    Establishes a WebSocket connection with the server.
    Handles sending and receiving chat messages.
    Dynamically updates the chat interface with new messages.

initMap() (index.html):
    Description: Initializes the Google Maps integration for displaying child locations.
    Functions:
    Retrieves child location data from the HTML document.
    Creates a Google Map instance centered at the child's location.
    Adds a marker to the map representing the child's current position.

trackLocation() (index.html):
    Description: Tracks the user's location in real-time for child users.
    Functions:
    Utilizes the browser's geolocation API to monitor the user's position.
    Updates the child's location on the map and sends it to the server for storage.
