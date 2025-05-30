import numpy as np
import pandas as pd
import requests
import json

from transformers import pipeline
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

