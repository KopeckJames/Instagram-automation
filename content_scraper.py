import requests
from bs4 import BeautifulSoup
from googleapiclient.discovery import build
from PIL import Image
from urllib.parse import urlparse
import tensorflow as tf

class ContentScraper:
    def scrape_images_from_unsplash(self, search_query):
        url = f"https://unsplash.com/s/photos/{search_query}"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        images = soup.find_all('img', class_='sq-photo__img')
        image_urls = [img['src'] for img in images]

        return image_urls

    def scrape_images_from_pixabay(self, search_query):
        url = f"https://pixabay.com/images/search/{search_query}"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        images = soup.find_all('a', class_='img-container')
        image_urls = [img.find('img')['src'] for img in images]

        return image_urls

    def scrape_videos_from_youtube(self, search_query, api_key):
        youtube = build('youtube', 'v3', developerKey=api_key)

        search_response = youtube.search().execute(part='snippet', q=search_query, maxResults=50)
        video_ids = [video['id']['videoId'] for video in search_response['items']]

        videos = []
        for video_id in video_ids:
            video_response = youtube.videos().list(part='snippet,contentDetails', id=video_id).execute()
            videos.append(video_response['items'][0])

        return videos

    def filter_content(self, content_urls, quality_criteria):
        filtered_content = []

        for content in content_urls:
            if self.check_quality(content, quality_criteria):
                filtered_content.append(content)

        return filtered_content

    def check_quality(self, content, quality_criteria):
        if isinstance(content, dict):  # Assuming content is a YouTube video object
            # Check video duration
            duration_seconds = int(content['contentDetails']['duration'][1:])
            if duration_seconds < quality_criteria.get('min_duration', 30):
                return False

            # Check video resolution
            video_details = youtube.videos().list(part='contentDetails', id=content['id']).execute()
            resolution = video_details['items'][0]['contentDetails']['definition']
            if resolution != 'highdefinition' and resolution != 'standard':
                return False

            # Check video relevance (e.g., using keyword matching)
            keywords = content['snippet']['title'].lower().split()
            if any(keyword in keywords for keyword in quality_criteria.get('keywords', [])):
                return True

            return False
        elif isinstance(content, str):  # Assuming content is a URL
            try:
                response = requests.get(content, stream=True)
                response.raise_for_status()

                image = Image.open(response.raw)
                width, height = image.size

                if width < quality_criteria.get('min_width', 800) or height < quality_criteria.get('min_height', 600):
                    return False

                # Check image relevance using image recognition
                model = tf.keras.models.load_model('your_image_recognition_model.h5')  # Replace with your model path
                image_array = preprocess_image(image)  # Preprocess image for model input
                predictions = model.predict(image_array)

                # Analyze predictions and determine relevance
                if any(prediction > 0.8 for prediction in predictions):  # Adjust threshold as needed
                    return True

                return False
            except Exception as e:
                print(f"Error processing image: {e}")
                return False

        return False

def preprocess_image(image):
    # Preprocess image (e.g., resize, normalize) for model input
    image = image.resize((224, 224))  # Assuming your model expects 224x224 images
    image_array = tf.keras.preprocessing.image.img_to_array(image)
    image_array = tf.keras.applications.imagenet_utils.preprocess_input(image_array)
    image_array = tf.expand_dims(image_array, axis=0)

    return image_array

####dont forget to make the model
