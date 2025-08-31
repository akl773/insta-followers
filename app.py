from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import os
import time
from datetime import datetime
from typing import List, Dict, Any

from instagrapi import Client
from instagrapi.types import UserShort
from pathlib import Path
from dotenv import load_dotenv

from models.report import Report
from models.user import User
from utils.time import get_morning_time

load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

class InstagramAPI:
    def __init__(self):
        self.client = self._init_client()
        
    def _init_client(self) -> Client:
        """Initialize the Instagram client with session management."""
        user, pwd = os.getenv('INSTAGRAM_USERNAME'), os.getenv('INSTAGRAM_PASSWORD')
        if not user or not pwd:
            raise Exception("Instagram credentials missing in .env")
            
        client = Client()
        sf = Path(f"session/{user}_session.json")
        sf.parent.mkdir(exist_ok=True)

        def do_login():
            client.login(user, pwd)
            client.dump_settings(sf)

        if sf.exists():
            try:
                client.load_settings(sf)
                client.user_following(str(client.user_id), amount=1)
            except Exception:
                do_login()
        else:
            do_login()
        return client

    def get_followers(self, amount: int = 0) -> List[Dict]:
        """Fetch followers and return as list of dictionaries."""
        followers = self.client.user_followers(str(self.client.user_id), amount=amount)
        return [self._to_user_dict(u) for u in followers.values()]

    def get_following(self, amount: int = 0) -> List[Dict]:
        """Fetch following and return as list of dictionaries."""
        following = self.client.user_following_v1(str(self.client.user_id), amount=amount)
        return [self._to_user_dict(u) for u in following]

    @staticmethod
    def _to_user_dict(u: UserShort) -> Dict:
        """Convert Instagram UserShort to dictionary."""
        return {
            'id': u.pk,
            'username': u.username,
            'full_name': u.full_name,
            'profile_pic_url': str(u.profile_pic_url)
        }

# Global Instagram API instance
instagram_api = None

def get_instagram_api():
    global instagram_api
    if instagram_api is None:
        instagram_api = InstagramAPI()
    return instagram_api

@app.route('/')
def index():
    """Serve the React frontend."""
    return render_template('index.html')

@app.route('/api/health')
def health_check():
    """Health check endpoint."""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

@app.route('/api/followers', methods=['GET'])
def get_followers():
    """Get followers with optional limit."""
    try:
        amount = request.args.get('limit', 0, type=int)
        api = get_instagram_api()
        followers = api.get_followers(amount)
        return jsonify({
            'success': True,
            'data': followers,
            'count': len(followers)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/following', methods=['GET'])
def get_following():
    """Get following with optional limit."""
    try:
        amount = request.args.get('limit', 0, type=int)
        api = get_instagram_api()
        following = api.get_following(amount)
        return jsonify({
            'success': True,
            'data': following,
            'count': len(following)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/reports', methods=['GET'])
def get_reports():
    """Get all reports with optional limit."""
    try:
        limit = request.args.get('limit', 10, type=int)
        reports = Report.find_many(
            query={},
            sort=[('generated_at', -1)],
            limit=limit
        )
        return jsonify({
            'success': True,
            'data': [report.get_dict() for report in reports]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/reports/latest', methods=['GET'])
def get_latest_report():
    """Get the most recent report."""
    try:
        report = Report.find_one(
            query={},
            sort=[('generated_at', -1)]
        )
        if report:
            return jsonify({
                'success': True,
                'data': report.get_dict()
            })
        else:
            return jsonify({'success': False, 'error': 'No reports found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/reports/generate', methods=['POST'])
def generate_report():
    """Generate a new report."""
    try:
        api = get_instagram_api()
        
        # Get current data
        followers = api.get_followers()
        following = api.get_following()
        
        # Update user database
        User.update_many([User(**user) for user in followers + following])
        
        # Generate report
        fids, gids = {u['id'] for u in followers}, {u['id'] for u in following}
        users = {}
        
        for u in followers + following:
            user_id = u['id']
            if user_id not in users:
                users[user_id] = u.copy()
                users[user_id]['type'] = []
            
            if user_id in fids and 'follower' not in users[user_id]['type']:
                users[user_id]['type'].append('follower')
            if user_id in gids and 'following' not in users[user_id]['type']:
                users[user_id]['type'].append('following')

        generated_at = get_morning_time()
        report = Report(
            _id=str(generated_at),
            generated_at=generated_at,
            num_followers=len(followers),
            num_following=len(following),
            users=list(users.values())
        )
        
        # Check for previous report to analyze changes
        last_report = Report.find_one(
            query={"generated_at": {"$lt": generated_at}},
            sort=[("generated_at", -1)]
        )
        
        if last_report:
            # Analyze changes
            curr_f = set(report.get_user_ids_by_type('follower'))
            prev_f = set(last_report.get_user_ids_by_type('follower'))
            curr_g = set(report.get_user_ids_by_type('following'))
            prev_g = set(last_report.get_user_ids_by_type('following'))
            
            report.new_followers = list(curr_f - prev_f)
            report.lost_followers = list(prev_f - curr_f)
            report.new_following = list(curr_g - prev_g)
            report.unfollowed = list(prev_g - curr_g)
            
            report.stats = {
                'new_followers_count': len(report.new_followers),
                'lost_followers_count': len(report.lost_followers),
                'new_following_count': len(report.new_following),
                'unfollowed_count': len(report.unfollowed),
                'net_follower_change': len(report.new_followers) - len(report.lost_followers),
                'net_following_change': len(report.new_following) - len(report.unfollowed),
                'previous_report_date': last_report.generated_at.strftime('%Y-%m-%d')
            }
        
        report.save()
        
        return jsonify({
            'success': True,
            'data': report.get_dict(),
            'message': 'Report generated successfully'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/user/<user_id>', methods=['GET'])
def get_user_details(user_id):
    """Get detailed information about a specific user."""
    try:
        api = get_instagram_api()
        
        # Get user info from Instagram
        user_info = api.client.user_info_by_username_v1(user_id)
        
        # Get user's followers and following counts
        followers_count = api.client.user_followers_count(user_info.pk)
        following_count = api.client.user_following_count(user_info.pk)
        
        # Get recent posts (limit to 6 for performance)
        try:
            user_posts = api.client.user_medias(user_info.pk, amount=6)
            recent_posts = []
            for post in user_posts:
                recent_posts.append({
                    'id': post.pk,
                    'media_type': post.media_type,
                    'thumbnail_url': str(post.thumbnail_url) if post.thumbnail_url else None,
                    'media_url': str(post.media_url) if post.media_url else None,
                    'caption': post.caption_text if post.caption_text else '',
                    'like_count': post.like_count,
                    'comment_count': post.comment_count,
                    'taken_at': post.taken_at.isoformat() if post.taken_at else None
                })
        except Exception as e:
            recent_posts = []
            print(f"Could not fetch posts for user {user_id}: {e}")
        
        # Check if this user follows us and we follow them
        current_user_id = str(api.client.user_id)
        is_following_us = False
        we_are_following = False
        
        try:
            # Check if they follow us
            our_followers = api.client.user_followers(current_user_id, amount=1000)
            is_following_us = user_info.pk in our_followers
            
            # Check if we follow them
            our_following = api.client.user_following_v1(current_user_id, amount=1000)
            we_are_following = user_info.pk in our_following
        except Exception as e:
            print(f"Could not check follow status: {e}")
        
        user_details = {
            'id': user_info.pk,
            'username': user_info.username,
            'full_name': user_info.full_name,
            'profile_pic_url': str(user_info.profile_pic_url),
            'biography': user_info.biography,
            'website': user_info.website,
            'is_private': user_info.is_private,
            'is_verified': user_info.is_verified,
            'followers_count': followers_count,
            'following_count': following_count,
            'media_count': user_info.media_count,
            'recent_posts': recent_posts,
            'relationship_status': {
                'is_following_us': is_following_us,
                'we_are_following': we_are_following,
                'is_mutual': is_following_us and we_are_following
            }
        }
        
        return jsonify({
            'success': True,
            'data': user_details
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/not-following-back', methods=['GET'])
def get_not_following_back():
    """Get users who are not following back."""
    try:
        report = Report.find_one(
            query={},
            sort=[('generated_at', -1)]
        )
        
        if not report:
            return jsonify({'success': False, 'error': 'No reports found'}), 404
            
        exceptions = os.getenv("EXCEPTION_NOT_FOLLOWING_BACK", "")
        exception_list = [username.strip().lower() for username in exceptions.split(",") if username.strip()]
        
        not_following_back = []
        for user in report.users:
            username = user.get("username", "").strip()
            types = user.get("type", [])
            
            if username.lower() in exception_list:
                continue
            if types != ["following"]:
                continue
                
            not_following_back.append({
                'username': username,
                'full_name': user.get('full_name', ''),
                'profile_pic_url': user.get('profile_pic_url', ''),
                'instagram_url': f"https://www.instagram.com/{username}/"
            })
        
        return jsonify({
            'success': True,
            'data': not_following_back,
            'count': len(not_following_back)
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
