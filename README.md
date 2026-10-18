<a id="readme-top"></a>

<!-- PROJECT LOGO --> <br /> <div align="center"> <h3 align="center">Austrian Inflation Tracker</h3> <p align="center">A Flask web app visualising consumer price inflation in Austria</p> </div> <!-- TABLE OF CONTENTS --> <details> <summary>Table of Contents</summary> <ol> <li> <a href="#about-the-project">About The Project</a> <ul> <li><a href="#built-with">Built With</a></li> </ul> </li> <li> <a href="#getting-started">Getting Started</a> <ul> <li><a href="#prerequisites">Prerequisites</a></li> <li><a href="#installation">Installation</a></li> </ul> </li> <li><a href="#usage">Usage</a></li> <li><a href="#contributing">Contributing</a></li> <li><a href="#license">License</a></li> <li><a href="#contact">Contact</a></li> </ol> </details> <!-- ABOUT THE PROJECT -->
About The Project

A web app that analyses the development of the Austrian Consumer Price Index (CPI, base year 2015) from 2015 to 2025. Data is stored in SQLite and queried with SQL; the dashboard computes the latest annual inflation rate, finds the basket category with the highest index value and shows how prices for food, education and health changed year on year.

Built as a personal learning project combining Python, SQL and web development.

Features:

Interactive Plotly chart of the overall CPI over time
Automatically calculated year-on-year inflation for the most recent full year
Highlights for the biggest basket contributor and key categories
Inflation calculator converting 2015 euros into today's value
Full English and German versions of every page
mainProject.py: a standalone command-line script for quick SQL queries and a Matplotlib plot
Built With
Python 3
Flask
SQLite
Plotly
Matplotlib & pandas
HTML, CSS, JavaScript (CountUp.js)
<p align="right">(<a href="#readme-top">back to top</a>)</p> <!-- GETTING STARTED -->
Getting Started

To get a local copy up and running follow these simple example steps.

Prerequisites
Python 3
An SQLite database austrian_cpi.db with the CPI data (see below)
Installation
Clone the repo
sh
   git clone https://github.com/DV155/market-analysis-project.git
   cd market-analysis-project
Create a virtual environment and install the dependencies
sh
   python -m venv env
   source env/bin/activate   # Windows: env\Scripts\activate
   pip install -r requirements.txt
Provide the database. Database files are git-ignored, so create austrian_cpi.db in the project root with a table available_data. The columns are year, cpi_overall and one column per basket category:
   food_beverages, alcohol_tobacco, clothing_footwear, housing_utilities,
   furnishings_household, health, transport, communication,
   recreation_culture, education, restaurants_hotels, miscellaneous

Annual CPI values (2015 = 100) are published by Statistik Austria. 4. Run the app

sh
   python app.py
<p align="right">(<a href="#readme-top">back to top</a>)</p> <!-- USAGE -->
Usage

Open http://127.0.0.1:5000 in your browser.

Route	Page
/ · /de	Dashboard (English / German)
/calc · /calcDE	Inflation calculator
/about · /aboutDE	About the project

For a production-style server, the app is set up to run with Waitress: replace app.run(debug=True) with serve(app) in app.py.

To run the command-line analysis instead:

sh
python mainProject.py
<p align="right">(<a href="#readme-top">back to top</a>)</p> <!-- CONTRIBUTING -->
Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are greatly appreciated.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement". Don't forget to give the project a star! Thanks again!

Fork the Project
Create your Feature Branch (git checkout -b feature/AmazingFeature)
Commit your Changes (git commit -m 'Add some AmazingFeature')
Push to the Branch (git push origin feature/AmazingFeature)
Open a Pull Request
<p align="right">(<a href="#readme-top">back to top</a>)</p>
Top contributors:
<a href="https://github.com/DV155/market-analysis-project/graphs/contributors"> <img src="https://contrib.rocks/image?repo=DV155/market-analysis-project" alt="contrib.rocks image" /> </a> <!-- LICENSE -->
License

Distributed under the MIT license. See LICENSE for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p> <!-- CONTACT -->
Contact

Daniil Vasilcovschii - LinkedIn - GitHub

Project Link: https://github.com/DV155/market-analysis-project

<p align="right">(<a href="#readme-top">back to top</a>)</p>
