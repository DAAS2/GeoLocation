Geo-Location Child Tracking App:

Project Description:
The goal of this project is to design and develop a child tracking app that utilizes geolocation technology to track the child for their parents to know where they are. Parents are also able to communicate with their child in real time using websockets and channels in Django.

The App uses Django as the web framework, Python(Backend) and Javascript, HTML&CSS (Frontend)

Features of app:
- Real-Time Location Tracking: The app uses GPS technology to track the child's location in real-time, allowing parents to view their child's current location on a map and this is done by using Google API.

- Live Chat System: The app has a live chat system, which lets parents and children to communicate with each other in real-time.

Primary Goal:
- Let the parents know about their childs location and to ensure their saftey incase something were to happen
- The real-time location tracking feature will allow the parents to quickly locate their children in case of an emergency, 
- The live chat system will help parents and children to stay connected throughout the day


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
- It displays a map view with the child's location, and the marker has the childs name
- It has a livetracking feature and it tracks the childs location on the live using javascript, specially navigator.geolocation.watchPosition 
which watches the childs position real time
- It also sends the child location to the servers through ajax and jquery which sends it as a POST method and a json object
- The server then updates the child's location in the database

contact_child.html
- This is the page where the parent can send messages to their child
- It has a text box where the parent or child can type their message and a button to send it 
- It also displays the messages sent by the parent or child, its a green text if the user send it and a white if someonne else has sent it 
- It uses websockets to send and receive messages in real time, Django channels then handles those websockets


models.py
- The database is in SQLite
- The database has three tables: User, Parent, Child, and ChatMessage
- The database is used to store the user's information, parent's information, child's information and the chat information 
- The database is used to authenticate the users and to store the location of the child in lat and lng
- The database is also used to store the messages sent between the parent and child


Functions in views.py:
index():
- This function renders the index page
- It checks if the user is a parent or child and then sends the info to index.html

find_child():
- It gets the child's location from the database and sends it to findchild.html
- It also checks if the user has a child or not and if it doesn't the it renders you don't have any children

update_location():
- This function is used to update the child's location in the database
- It receives the child's location from the findchild.html through an AJAX request
- It then gets lat and lng and updates the child's location in the database

contact_child():
- This function renders the contact_child page
- It gets the chat messages from the database and sends them to contact_child.html

login_view(), logout_view(), register():
- These are the functions for login, logout and register
- They login the user, logout and register 
- authenticates user and hashes password and important details

Functions in consumers.py:
ChatConsumer:
- This is a class that handles the chat functionality
- It uses websockets to implement chat
- It connects the parent and child to the same chat room
- It receives the messages from the parent or child and sends it to the other user
- It uses Django channels to handle the websockets
- It also sends the messages to the database to be stored

JavaScript Functions:

Chat():
- This function is used to send and receive messages
- It connects to the websocket and sends the messages to the server
- It receives the messages from the server and displays them in the chat box
- It also scrolls down the chat box when a new message is received

initMap():
- This function is used to initialize the map
- It creates a map and adds a marker to the map
- It also updates the marker's position when the child's location is updated
- It uses Google Maps API to create the map

trackLocation():
- This function is used to track the child's location
- It gets the child's location from the database and updates the marker's position
- It also updates the child's location in the database
- It uses Google Maps API to get the child's location

