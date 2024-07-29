# FoodFind

Welcome to FoodFind, a restaurant discovery web app. It helps users find and explore restaurants based on their tastes, leveraging a user-friendly interface built with Vite and TypeScript. This project was completed as part of my 6th semester Software Engineering degree. Discover new dining spots, read reviews, and connect with food lovers in your community with FoodFind! 

The backend repository can be found [here](https://github.com/dhunganaPradeep/FoodFindBE).

## Objectives

The project's objectives are to:

- Develop a user-friendly platform to explore Kathmandu's restaurant scene.
- Enhance the online presence of local restaurants and facilitate the sharing of culinary reviews and experiences.

## Features
- **Google Auth :** Login/Signup is managed through Google Auth
- **Admin Panel :** Manage and monitor restaurant listings and user reviews.
- **Providing Reviews :** Users can leave reviews for restaurants they visit.
- **Searching Restaurants :** Find restaurants by name and location.
- **Add to Favourites :** Save your favorite restaurants for easy access.
- **Recommendations :** Get personalized restaurant suggestions.
- **Map Section :** Map to show nearby restaurants within a 3km radius of the user's current location.
- **Search and Route :** Search for restaurants and view the route and distance from your location.
- **Menu :** Access restaurant menus.
- **User Profile :** User Profile section.


## Tech Stack

- **Backend Database:** SQLite
- **REST API Service:** Django REST Framework, Postman
- **Web Application:** React + TypeScript + Vite
- **IDE / Code Editor:** Sublime Text, Code-OSS
- **Version Control System:** GitHub
- **Documentation:** Overleaf

## Installation steps for Frontend

To set up the frontend locally, follow these steps:

```bash
# Clone the repository
git clone https://github.com/visionrijal/FoodFind.git
cd FoodFindFrontend

# Install dependencies
npm install

# Run the development server
npm run dev

# Open your browser and go to
# http://localhost:3000 to see the application in action
```


## Installation steps for Backend

To set up the backend locally, follow these steps:

```bash
# Clone the repository
git clone https://github.com/dhunganaPradeep/FoodFindBE
cd FoodFindBE

# Install dependencies
pip install -r requirements.txt

# Set up the database
python manage.py makemigrations
python manage.py migrate

# Create and admin user
python manage.py createsuperuser

#  Populate the database with initial data
python populate.py 
python assignTags.py
python addTopRestaurant.py
python addReviews.py
python addMenu.py

# Run the development server
python manage.py runserver

# Open your browser and go to
# http://127.0.0.1:8000/admin to see the application in action
```

## Outputs

Below are some screenshots and outputs from the project:

- **Home Page:**
  ![Home Page](/Outputs/home.png)

- **Restaurant Page:**
  ![Restaurant Page](/Outputs/restro.png)

- **Restaurant Profile:**
  ![Restaurant Page](/Outputs/profile.png)

- **Map Section:**
  ![Map Section](/Outputs/map%20section.png)

- **Admin Panel:**
  ![Admin Panel](/Outputs/admin.png)


## Collaborators
- [Pradip Dhungana](dhunganapradip.com.np)
- [Vision Rijal](https://visionrijal.com.np/)
- [Bishnu Timilsena](https://github.com/BishnuTimilsena)


## Contributing

Feel free to fork this repository, make modifications, and contribute to the enhancement of FoodFind. Your contributions are valuable in making this project even better!

Happy exploring!


