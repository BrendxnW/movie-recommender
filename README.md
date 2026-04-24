<h1 align="center"> Movie Recommender and Remixer</h1>

<p align="center">
<strong>Natural-language movie recommendations with summaries</strong><br>
<strong>Link to app: http://3.142.164.130:8000</strong>
</p>
<p align="center">
  <a href="https://www.python.org/">
    <img src="https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white" />
  </a>
  <a href="LICENSE">
    <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" />
  </a>
</p>

## Table of Contents
- [Security](#security)
- [Background](#background)
- [Features](#features)
- [Demo Video](#demo-video)
- [Install](#install)
- [Usage](#usage)
- [API](#api)
- [Contributing](#contributing)
- [License](#license)

## Security
This project uses the TMDb API for fetching movie metadata. API keys should be stored securely using environment variables and should not be committed to version control.  
This project is intended for educational use.

## Background
This project explores natural language interfaces for movie discovery. Users can describe what they are in the mood for (e.g., “a feel-good comedy”) and receive curated recommendations with engaging summaries. The goal is to bridge user intent with structured movie metadata using NLP techniques and lightweight ML models.


## Features
- Natural Language Understanding: Parses genre from user input
- Dynamic Movie Suggestions
- Intent Detection (WIP): Working on integrating NLP models to classify user intent
- Efficient Data Processing: Uses NumPy and Pandas for metadata filtering and scoring
  
## Demo Video
https://github.com/user-attachments/assets/53067306-7e60-412a-9611-d368ef266ad2

## Install
```bash
git clone https://github.com/yourname/movie-recommender.git  
cd movie-recommender
python -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt
```

## Usage
**Local (Development)**
```bash
python manage.py runserver localhost:8000
```
**Docker**
```bash
docker build -t movie-app .
docker run -p 8000:8000 movie-app
```

## API
### Data Sources

- Movie data retrieved using the IMDB API
- Dataset from Kaggle:
  - [The Movies Dataset](https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset)
  - `movies_metadata.csv`
  - `keywords.csv`

### Machine Learning

- Built using Hugging Face Transformers
- Utilizes text generation to remix and combine movie plots
- Model leverages semantic understanding of movie descriptions and keywords


## Contributing

Contributions are welcome!
1. Fork the repo
2. Create a feature branch
3. Submit a PR with a clear description

## License
[MIT © Richard McRichface.](./LICENSE)
