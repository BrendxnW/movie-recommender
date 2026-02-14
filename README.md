<h1 align="center"> Movie Summarizer and Recommender </h1>

<p align="center">
<strong>Natural-language movie recommendations with summaries</strong>
</p>
<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Status-Educational-green" />

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
pip install -r requirements.txt
```

## Usage
**Local (Development)**
```bash
python manage.py runserver
```

## API
### Classifying Intent
#### `ClassifyIntent`
**Location:** `movie_rec/nlp_utils.py`

**Description:**  
Uses a text classification model to identify the intent of the user input to find relevant movie genres and descriptions that match.

**Constructor**
```python
ClassifyIntent(user_input)
...
```

### Recommending Movie
#### `RecommendMovie`
**Location:** `movie_rec/nlp_utils.py`

**Description:**  
Uses a text classifiction model to match the user's input with a movie genre.

**Constructor**
```python
RecommendMovie(genre)
...
```

### Finding Movie
#### `FindMovie`
**Location:** `movie_rec/nlp_utils.py`

**Description:**  
Finds relevant movies based on the user's description.

**Constructor**
```python
FindMovie(user_input)
...
```

### Remixing Plot
#### `RemixPlot`
**Location:** `movie_rec/nlp_utils.py`

**Description:**  
Uses Microsoft's small language model (SLM) "microsoft/phi-2" to remix two movie plots into one.

**Constructor**
```python
Remixer(plot1, plot2, vibes=None)
...
```

## Contributing

Contributions are welcome!
1. Fork the repo
2. Create a feature branch
3. Submit a PR with a clear description

## License
[MIT © Richard McRichface.](./LICENSE)
