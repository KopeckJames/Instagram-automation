from instagram_api import InstagramAPI
from content_scraper import ContentScraper
from content_generator import ContentGenerator
from post_scheduler import PostScheduler
from dm_sender import DMSender
from engagement_manager import EngagementManager
from utils import load_credentials

def main():
    # Load credentials
    username, password, client_id, client_secret = load_credentials()

    # Create instances of classes
    instagram_api = InstagramAPI(username, password)
    content_scraper = ContentScraper()
    content_generator = ContentGenerator()
    post_scheduler = PostScheduler(instagram_api)
    dm_sender = DMSender(instagram_api)
    engagement_manager = EngagementManager(instagram_api)

    # Configure parameters
    search_query = "austin food"  # Adjust search query as needed
    quality_criteria = {'min_width': 800, 'min_height': 600, 'keywords': ['austin', 'food', 'texas']}
    post_schedule = ['7:00', '14:00', '21:00']  # CST
    max_follows = 50
    max_unfollows = 20
    engagement_threshold = 3  # Minimum number of recent engagements

    # Scrape content
    image_urls = content_scraper.scrape_images_from_unsplash(search_query)
    image_urls.extend(content_scraper.scrape_images_from_pixabay(search_query))
    videos = content_scraper.scrape_videos_from_youtube(search_query, client_id)
    filtered_content = content_scraper.filter_content(image_urls + videos, quality_criteria)

    # Generate captions and schedule posts
    for content in filtered_content:
        caption = content_generator.generate_caption(content)
        post_scheduler.schedule_post(content, caption, [], post_schedule)

    # Send DMs to restaurants
    restaurant_usernames = dm_sender.get_restaurant_usernames(search_query)
    message_template = "Hi @{username},\n\nI'm a big fan of your restaurant! I'd love to collaborate with you on a promotion. I can share a review of your restaurant with my followers in exchange for a free entree or discount. Let me know if you're interested!"
    dm_sender.send_dms_to_restaurants(restaurant_usernames, message_template)

    # Manage engagement
    engagement_manager.follow_unfollow_strategy(max_follows, max_unfollows, engagement_threshold)

    # Run the scheduling loop
    while True:
        schedule.run_pending()
        time.sleep(1)