import instagrapi1
import time
message_template = "Hi @{username},\n\nI'm a big fan of your restaurant! I'd love to collaborate with you on a promotion. I can share a review of your restaurant with my followers in exchange for a free entree or discount. Let me know if you're interested!"

class DMSender:
    def __init__(self, instagram_api):
        self.instagram_api = instagram_api

    def send_dms_to_restaurants(self, search_query, message_template):
        restaurant_usernames = self.get_restaurant_usernames(search_query)

        for username in restaurant_usernames:
            try:
                user_id = self.instagram_api.client.username_to_user_id(username)
                message = message_template.format(username=username)
                self.instagram_api.client.send_direct_message(user_id, message)
                print(f"DM sent to {username}")
            except instagrapi1.client.ClientError as e:
                if e.code == 429:  # Rate limit exceeded
                    print(f"Rate limit exceeded. Waiting 5 minutes...")
                    time.sleep(300)
                else:
                    print(f"Error sending DM to {username}: {e}")
            except Exception as e:
                print(f"Error sending DM to {username}: {e}")

    def get_restaurant_usernames(self, search_query):
        search_results = self.instagram_api.client.search_users(search_query)
        restaurant_usernames = [user['username'] for user in search_results if 'restaurant' in user['full_name'].lower()]

        return restaurant_usernames