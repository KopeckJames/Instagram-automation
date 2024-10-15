import random
import exifread
import openai
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

class ContentGenerator:
    def __init__(self):
        self.templates = [
            "Explore the beauty of Austin through this stunning image of {keyword}.",
            "Feeling inspired by {keyword} in Austin. What's your favorite spot?",
            "Austin vibes: {keyword}. Who else loves this city?",
            "Discovering hidden gems in Austin. Check out this {keyword}.",
            "Immerse yourself in the vibrant Austin culture with this {keyword}.",
            "Austin's {keyword} scene is thriving. Have you checked it out yet?",
            "A glimpse into the heart of Austin: {keyword}.",
            "Feeling {emotion} after seeing this {keyword} in Austin.",
        ]

    def generate_caption(self, image_path):
        # Extract keywords from image filename and metadata
        keywords = self.extract_keywords(image_path)

        # Use OpenAI to generate a more contextually relevant caption
        caption = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Generate a caption for an Instagram post about Austin based on these keywords: {keywords}",
            max_tokens=100,
            n=3,
            stop=None,
        )

        # Choose the best caption based on relevance and creativity
        chosen_caption = self.choose_best_caption(caption.choices, keywords)

        return chosen_caption

    def extract_keywords(self, image_path):
        keywords = []

        # Extract keywords from filename
        keywords.extend(image_path.split("/")[-1].split("_"))

        # Extract keywords from EXIF data (if available)
        try:
            with open(image_path, 'rb') as f:
                tags = exifread.process_file(f)
                if 'Image Description' in tags:
                    keywords.extend(tags['Image Description'].values.split())
        except:
            pass

        return keywords

    def choose_best_caption(self, captions, keywords):
        # Preprocess keywords and captions
        keywords = set(word_tokenize(keywords.lower())) - set(stopwords.words('english'))
        captions = [caption.text.lower() for caption in captions]

        # Calculate keyword scores
        keyword_scores = {}
        for caption in captions:
            caption_words = set(word_tokenize(caption)) - set(stopwords.words('english'))
            keyword_score = len(keywords.intersection(caption_words)) / len(keywords)
            keyword_scores[caption] = keyword_score

        # Calculate creativity scores using ChatGPT
        creativity_scores = {}
        for caption in captions:
            creativity_score = self.evaluate_creativity(caption)
            creativity_scores[caption] = creativity_score

        # Combine scores and choose the best caption
        combined_scores = {caption: keyword_score * creativity_score for caption, keyword_score, creativity_score in zip(captions, keyword_scores.values(), creativity_scores.values())}
        best_caption = max(combined_scores, key=combined_scores.get)

        return best_caption

    def evaluate_creativity(self, caption):
        # Use ChatGPT to evaluate creativity
        prompt = f"Rate the creativity of the following caption on a scale of 1-10: {caption}"
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=100,
            n=1,
            stop=None,
        )

        # Extract the creativity score from the response
        try:
            creativity_score = float(response.choices[0].text)
            if creativity_score < 0 or creativity_score > 10:
                creativity_score = 0  # Handle invalid scores
        except ValueError:
            creativity_score = 0  # Handle non-numeric responses

        return creativity_score