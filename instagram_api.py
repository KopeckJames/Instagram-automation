import instagrapi1

class InstagramAPI:
    def __init__(self, username, password):
        self.client = instagrapi1.Client()
        self.client.login(username, password)

    def upload_post(self, media_path, caption, hashtags):
        try:
            self.client.upload_photo(media_path, caption=caption, hashtags=hashtags)
            print("Post uploaded successfully.")
        except Exception as e:
            print(f"Error uploading post: {e}")

    def send_direct_message(self, user_id, message):
        try:
            self.client.send_direct_message(user_id, message)
            print("DM sent successfully.")
        except Exception as e:
            print(f"Error sending DM: {e}")

    def like_post(self, post_id):
        try:
            self.client.like(post_id)
            print("Post liked successfully.")
        except Exception as e:
            print(f"Error liking post: {e}")

    def follow(self, user_id):
        try:
            self.client.follow(user_id)
            print("User followed successfully.")
        except Exception as e:
            print(f"Error following user: {e}")

    def unfollow(self, user_id):
        try:
            self.client.unfollow(user_id)
            print("User unfollowed successfully.")
        except Exception as e:
            print(f"Error unfollowing user: {e}")

    def search_users(self, search_query):
        try:
            results = self.client.search_users(search_query)
            return results
        except Exception as e:
            print(f"Error searching users: {e}")
            return []

    def username_to_user_id(self, username):
        try:
            user_id = self.client.username_to_user_id(username)
            return user_id
        except Exception as e:
            print(f"Error converting username to user ID: {e}")
            return None

    def get_following(self):
        try:
            following = self.client.get_following()
            return following
        except Exception as e:
            print(f"Error getting following list: {e}")
            return []

    def get_followers(self):
        try:
            followers = self.client.get_followers()
            return followers
        except Exception as e:
            print(f"Error getting followers list: {e}")
            return []

    def user_feed(self, user_id):
        try:
            feed = self.client.user_feed(user_id)
            return feed
        except Exception as e:
            print(f"Error getting user feed: {e}")
            return []

    def is_liked(self, post_id):
        try:
            is_liked = self.client.is_liked(post_id)
            return is_liked
        except Exception as e:
            print(f"Error checking if post is liked: {e}")
            return False

    def has_commented(self, post_id):
        try:
            comments = self.client.get_post_comments(post_id)
            for comment in comments:
                if comment['owner']['pk'] == self.client.user_id:
                    return True
            return False
        except Exception as e:
            print(f"Error checking if post has comments: {e}")
            return False