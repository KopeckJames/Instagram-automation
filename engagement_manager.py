import random
import time

class EngagementManager:
    def __init__(self, instagram_api):
        self.instagram_api = instagram_api

    def follow_unfollow_strategy(self, max_follows, max_unfollows, engagement_threshold):
        # Get a list of users to follow based on hashtags
        users_to_follow = self.get_users_from_hashtags(['austin', 'texas', 'food', 'photography'])

        # Follow users
        for user_id in users_to_follow[:max_follows]:
            self.follow_users([user_id])

        # Get a list of users to unfollow based on engagement
        users_to_unfollow = self.get_users_to_unfollow(engagement_threshold)

        # Unfollow users
        for user_id in users_to_unfollow[:max_unfollows]:
            self.unfollow_users([user_id])

    def get_users_from_hashtags(self, hashtags):
        users = []
        for hashtag in hashtags:
            search_results = self.instagram_api.client.search_hashtag(hashtag)
            for post in search_results['items']:
                user_id = post['owner']['pk']
                if user_id not in users:
                    users.append(user_id)

        return users

    def get_users_to_unfollow(self, engagement_threshold):
        # Get a list of users you're following
        following_list = self.instagram_api.client.get_following()

        # Filter users based on engagement (e.g., no recent likes or comments)
        users_to_unfollow = []
        for user in following_list:
            user_id = user['pk']
            if not self.has_recent_engagement(user_id, engagement_threshold):
                users_to_unfollow.append(user_id)

        return users_to_unfollow

    def has_recent_engagement(self, user_id, engagement_threshold):
        # Get the user's recent posts
        user_posts = self.instagram_api.client.user_feed(user_id)

        # Check if the user has engaged with your posts recently
        for post in user_posts:
            if post['owner']['pk'] == self.instagram_api.client.user_id:
                # Check if you've liked or commented on the user's post
                if self.instagram_api.client.is_liked(post['pk']) or self.instagram_api.client.has_commented(post['pk']):
                    return True

        # If no recent engagement, check if the user has liked or commented on your posts
        for post in self.instagram_api.client.user_feed(self.instagram_api.client.user_id):
            if post['owner']['pk'] == user_id:
                # Check if the user has liked or commented on your posts
                if self.instagram_api.client.is_liked(post['pk']) or self.instagram_api.client.has_commented(post['pk']):
                    return True

        # If no recent engagement, check if the user has followed back
        if self.is_user_following_back(user_id):
            return True

        # Otherwise, the user has not engaged recently
        return False

    def follow_users(self, user_ids):
        for user_id in user_ids:
            try:
                self.instagram_api.client.follow(user_id)
                print(f"Followed user {user_id}")
            except Exception as e:
                print(f"Error following user {user_id}: {e}")

    def unfollow_users(self, user_ids):
        for user_id in user_ids:
            try:
                self.instagram_api.client.unfollow(user_id)
                print(f"Unfollowed user {user_id}")
            except Exception as e:
                print(f"Error unfollowing user {user_id}: {e}")