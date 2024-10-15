import schedule
import time
import pytz

class PostScheduler:
    def __init__(self, instagram_api):
        self.instagram_api = instagram_api

    def schedule_post(self, media_path, caption, hashtags, time_strings):
        time_strings = [time_string + " CST" for time_string in time_strings]  # Convert to CST timezone

        for time_string in time_strings:
            def post_function():
                self.instagram_api.upload_post(media_path, caption, hashtags)

            schedule.every().day.at(time_string).do(post_function)

        while True:
            schedule.run_pending()
            time.sleep(1)