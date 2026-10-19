<a id="readme-top"></a>



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <h3 align="center">Austrian Inflation Tracker</h3>
  <p align="center">A Flask web app visualising consumer price inflation in Austria</p>
  <p align="center"><a href="https://market-analysis-project.onrender.com/"><strong>View the live site »</strong></a></p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#deployment">Deployment</a></li>
    <li><a href="#data-source">Data Source</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

A web app that analyses the development of the Austrian Consumer Price Index (CPI, base year 2015) from 2015 to the latest available year. The data is downloaded automatically from Statistik Austria's open data portal, stored in SQLite and queried with SQL; the dashboard computes the latest annual inflation rate, finds the basket category that contributed the most to inflation and shows how prices for food, education and health changed year on year.

Built as a personal learning project combining Python, SQL and web development.

**Live site:** [market-analysis-project.onrender.com](https://market-analysis-project.onrender.com/). It's on Render's free tier, so the first visit after a quiet period can take up to a minute while the server wakes up.

Features:
* Automatic data download from Statistik Austria, refreshed every 30 days
* Interactive Plotly chart of the overall CPI over time
* Automatically calculated year-on-year inflation for the most recent year in the database
* Biggest inflation driver, using Statistik Austria's official contributions (basket weight × price change)
* Highlights for key categories
* Inflation calculator converting euros from ten years ago into the latest year's value
* Full English and German versions of every page
* `mainProject.py`: a standalone command-line script for quick SQL queries and a Matplotlib plot

### Built With

* Python 3
* Flask
* SQLite
* Plotly
* Matplotlib
* HTML, CSS, JavaScript (CountUp.js)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

To just try the app, open the [live site](https://market-analysis-project.onrender.com/), no installation needed. To get a local copy up and running follow these simple example steps.

### Prerequisites
* Python 3.11+

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/DV155/market-analysis-project.git
   cd market-analysis-project
   ```
2. Create a virtual environment and install the dependencies
   ```sh
   python -m venv env
   source env/bin/activate   # Windows: env\Scripts\activate
   pip install -r requirements.txt
   ```
3. Run the app
   ```sh
   python app.py
   ```
   On first start the app downloads the CPI data and builds `austrian_cpi.db` (git-ignored). After that it only downloads again when the database is older than 30 days. To force a refresh:
   ```sh
   python fetch_data.py
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE -->
## Usage

Open the [live site](https://market-analysis-project.onrender.com/), or `http://127.0.0.1:5000` when running locally.

| Route | Page |
| --- | --- |
| [`/`](https://market-analysis-project.onrender.com/) · [`/de`](https://market-analysis-project.onrender.com/de) | Dashboard (English / German) |
| [`/calc`](https://market-analysis-project.onrender.com/calc) · [`/calcDE`](https://market-analysis-project.onrender.com/calcDE) | Inflation calculator |
| [`/about`](https://market-analysis-project.onrender.com/about) · [`/aboutDE`](https://market-analysis-project.onrender.com/aboutDE) | About the project |

To run the command-line analysis instead:
```sh
python mainProject.py
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- DEPLOYMENT -->
## Deployment

The live site runs on [Render](https://render.com) as a free web service, connected to this repository. Every push to `main` triggers a new deploy automatically.

| Setting | Value |
| --- | --- |
| Build command | `pip install -r requirements.txt` |
| Start command | `waitress-serve --listen=0.0.0.0:$PORT app:app` |

No database is stored on the server: Render's disk is wiped on every deploy and restart, so the app downloads the CPI data and rebuilds `austrian_cpi.db` on the first request after starting.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Top contributors:

<a href="https://github.com/DV155/market-analysis-project/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=DV155/market-analysis-project" alt="contrib.rocks image" />
</a>



<!-- DATA SOURCE -->
## Data Source

Consumer Price Index base 2015 (annual averages, basket weights and contributions to inflation), [Statistik Austria - data.statistik.gv.at](https://data.statistik.gv.at/web/meta.jsp?dataset=OGD_vpi15_VPI_2015_1), licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT license. See `LICENSE` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

