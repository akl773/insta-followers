import os
import time
from pathlib import Path
from typing import List, Dict, Any, Union, Set

from instagrapi import Client
from dotenv import load_dotenv
from instagrapi.types import UserShort
from colorama import init, Fore, Style

from Models.report import Report
from Models.user import User
from utils.time import get_morning_time

init()
load_dotenv()


class InstagramFollower:
    def __init__(self):
        """Initialize the Instagram follower analyzer with user settings."""
        self._print_header()
        self.start_time = time.time()
        self.client = self._init_client()
        self.dry_run = self._get_choice("Enable dry run mode? (Limited to 10 users) [y/N]: ")
        self.force_run = self._get_choice("Force regenerate today's report if it exists? [y/N]: ")
        if self.dry_run:
            print(f"{Fore.YELLOW}⚠️  DRY RUN MODE ENABLED - Limited to 10 users{Style.RESET_ALL}")
        if self.force_run:
            print(f"{Fore.YELLOW}⚠️  FORCE RUN MODE ENABLED - Will regenerate today's report{Style.RESET_ALL}")
        self.amount = 10 if self.dry_run else 0

    @staticmethod
    def _print_header():
        """Display the program header with formatting."""
        print(f"{Fore.CYAN}╔{'═' * 38}╗{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║{' Instagram Follower Analyzer ':^38}║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}╚{'═' * 38}╝{Style.RESET_ALL}")

    @staticmethod
    def _get_choice(prompt: str, default: bool = False) -> bool:
        """Get a yes/no choice from the user with a default option."""
        while True:
            resp = input(f"{Fore.YELLOW}{prompt}{Style.RESET_ALL}").strip().lower()
            if not resp:
                return default
            if resp in ('y', 'yes'):
                return True
            if resp in ('n', 'no'):
                return False
            print(f"{Fore.RED}Invalid input. Enter 'y' or 'n'.{Style.RESET_ALL}")

    @staticmethod
    def _init_client() -> Client:
        """Initialize the Instagram client with session management."""
        user, pwd = os.getenv('INSTAGRAM_USERNAME'), os.getenv('INSTAGRAM_PASSWORD')
        if not user or not pwd:
            print(f"{Fore.RED}Credentials missing in .env{Style.RESET_ALL}")
            exit(1)
        client = Client()
        sf = Path(f"session/{user}_session.json");
        sf.parent.mkdir(exist_ok=True)

        def do_login():
            client.login(user, pwd)
            client.dump_settings(sf)

        if sf.exists():
            print(f"{Fore.BLUE}🔑 Loading session for @{user}...{Style.RESET_ALL}")
            try:
                client.load_settings(sf)
                client.user_following(str(client.user_id), amount=1)
                print(f"{Fore.GREEN}✅ Session loaded{Style.RESET_ALL}")
            except Exception:
                print(f"{Fore.RED}Session failed, logging in...{Style.RESET_ALL}")
                do_login()
        else:
            print(f"{Fore.BLUE}🔑 First-time login...{Style.RESET_ALL}")
            do_login()
            print(f"{Fore.GREEN}✅ Session saved{Style.RESET_ALL}")
        return client

    def get_followers(self):
        """ Fetches the followers of the logged-in user.  """
        print(f"\n{Fore.BLUE}📥 Fetching followers...{Style.RESET_ALL}")
        t0 = time.time()
        followers = self.client.user_followers(str(self.client.user_id), amount=self.amount)
        users = [self._to_user(u) for u in followers.values()]
        print(
            f"{Fore.GREEN}✅ Retrieved {Fore.YELLOW}{len(users)}{Fore.GREEN}"
            f" followers in {Fore.YELLOW}{time.time() - t0:.2f}s{Style.RESET_ALL}"
        )
        return users

    def get_following(self):
        """ Fetches the following of the logged-in user.  """
        print(f"\n{Fore.BLUE}📥 Fetching following...{Style.RESET_ALL}")
        t0 = time.time()
        followers = self.client.user_following_v1(str(self.client.user_id), amount=self.amount)
        users = [self._to_user(u) for u in followers]
        print(
            f"{Fore.GREEN}✅ Retrieved {Fore.YELLOW}{len(users)}{Fore.GREEN}"
            f" followers in {Fore.YELLOW}{time.time() - t0:.2f}s{Style.RESET_ALL}"
        )
        return users

    @staticmethod
    def _to_user(u: UserShort) -> User:
        """Convert an Instagram UserShort object to our User model."""
        return User(_id=u.pk, username=u.username, full_name=u.full_name, profile_pic_url=str(u.profile_pic_url))

    @staticmethod
    def get_relationship_counts(
            followers: Union[List[User], List[Dict[str, Any]]],
            following: Union[List[User], List[Dict[str, Any]]]
    ) -> Dict[str, int]:
        """Calculate counts of different relationship types between followers and following."""
        # Handle both User objects and dictionaries
        if followers and isinstance(followers[0], dict):
            # We're dealing with dictionaries
            fids = {u.get('id') for u in followers if u.get('id')}
            gids = {u.get('id') for u in following if u.get('id')}
        else:
            # We're dealing with User objects
            fids = {u.id for u in followers}
            gids = {u.id for u in following}

        return {
            "followers": len(followers),
            "following": len(following),
            "mutual": len(fids & gids),
            "followers_only": len(fids - gids),
            "following_only": len(gids - fids)
        }

    def generate_report(self, followers: List[User], following: List[User]) -> Report:
        """Generate a new report based on current followers and following."""
        print(f"\n{Fore.BLUE}📊 Generating report...{Style.RESET_ALL}")
        t0 = time.time()
        fids, gids = {u.id for u in followers}, {u.id for u in following}
        users: Dict[str, Dict] = {}
        for u in followers + following:
            d = users.setdefault(u.id, u.get_dict() | {'type': []})
            if u.id in fids and 'follower' not in d['type']:
                d['type'].append('follower')
            if u.id in gids and 'following' not in d['type']:
                d['type'].append('following')

        generated_at = get_morning_time()
        report = Report(
            _id=str(generated_at),
            generated_at=get_morning_time(),
            num_followers=len(followers),
            num_following=len(following),
            users=list(users.values())
        )
        report.save()
        print(f"{Fore.GREEN}✅ Report generated in {Fore.YELLOW}{time.time() - t0:.2f}s{Style.RESET_ALL}")
        return report

    def print_summary(self, report: Report, counts: Dict[str, int] = None):
        """Print a summary of the report showing follower/following statistics."""
        if counts is None:
            counts = self.get_relationship_counts([
                u for u in report.users if 'follower' in u.get('type', [])
            ], [
                u for u in report.users if 'following' in u.get('type', [])
            ])
        content = [
            f"Date: {report.generated_at:%Y-%m-%d}",
            f"Total Followers: {Fore.YELLOW}{counts['followers']}{Style.RESET_ALL}",
            f"Total Following: {Fore.YELLOW}{counts['following']}{Style.RESET_ALL}",
            f"Mutual: {Fore.GREEN}{counts['mutual']}{Style.RESET_ALL}",
            f"Followers Only: {Fore.BLUE}{counts['followers_only']}{Style.RESET_ALL}",
            f"Following Only: {Fore.MAGENTA}{counts['following_only']}{Style.RESET_ALL}"
        ]
        self._print_box("Report Summary", content)

    def print_changes(self, report: Report, last: Report):
        """Print changes between current report and previous report."""
        stats = getattr(report, 'stats', {})
        if not stats:
            print(f"{Fore.YELLOW}ℹ️ No change data.{Style.RESET_ALL}")
            return
        content = []
        changed = [
            ('new_followers_count', '📈 New Followers', Fore.GREEN, report.new_followers),
            ('lost_followers_count', '📉 Lost Followers', Fore.RED, getattr(report, 'lost_followers', [])),
            ('new_following_count', '➕ New Following', Fore.GREEN, report.new_following),
            ('unfollowed_count', '➖ Unfollowed', Fore.RED, getattr(report, 'unfollowed', []))
        ]
        content.append(f"Previous: {stats.get('previous_report_date')}")
        for key, label, color, lst in changed:
            cnt = stats.get(key, 0)
            if cnt:
                content.append(f"{color}{label}: {cnt}{Style.RESET_ALL}")
                for i, uid in enumerate(lst[:5], 1):
                    user = (report if 'new' in key else last).get_user_by_id(uid)
                    if user:
                        content.append(f"  {i}. @{user.get('username', 'unknown')} ({user.get('full_name', '')})")
                if len(lst) > 5:
                    content.append(f"  ... and {len(lst) - 5} more")
            else:
                content.append(f"{Fore.YELLOW}{label}: 0{Style.RESET_ALL}")
        for net_key, label in [('net_follower_change', '📊 Net follower change'),
                               ('net_following_change', '📊 Net following change')]:
            val = stats.get(net_key, 0)
            col = Fore.GREEN if val > 0 else Fore.RED if val < 0 else Fore.YELLOW
            prefix = '+' if val > 0 else ''
            content.append(f"{col}{label}: {prefix}{val}{Style.RESET_ALL}")
        self._print_box("Changes Analysis", content)

    def analyse_reports(self, report: Report, last: Report):
        """Analyze differences between current and previous reports."""
        print(f"\n{Fore.BLUE}🔍 Analyzing since {last.generated_at:%Y-%m-%d}...{Style.RESET_ALL}")
        curr_f = set(report.get_user_ids_by_type('follower'))
        prev_f = set(last.get_user_ids_by_type('follower'))
        curr_g = set(report.get_user_ids_by_type('following'))
        prev_g = set(last.get_user_ids_by_type('following'))
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
            'previous_report_date': last.generated_at.strftime('%Y-%m-%d')
        }
        report.save()
        print(f"{Fore.GREEN}✅ Analysis complete{Style.RESET_ALL}")

    @staticmethod
    def _print_box(title: str, content: List[str], color=Fore.CYAN):
        """Print a formatted box with title and content."""
        width = max(len(line) for line in content + [title]) + 6
        print(f"\n{color}┌{'─' * (width - 2)}┐{Style.RESET_ALL}")
        print(f"{color}│{title.center(width - 2)}│{Style.RESET_ALL}")
        print(f"{color}├{'─' * (width - 2)}┤{Style.RESET_ALL}")
        for line in content:
            print(f"{color}│ {line}{' ' * (width - len(line) - 3)}│{Style.RESET_ALL}")
        print(f"{color}└{'─' * (width - 2)}┘{Style.RESET_ALL}")

    def run(self):
        """Run the Instagram follower analysis process."""
        today = get_morning_time()
        existing = Report.find_one({"generated_at": today})
        if existing and not self.force_run and not self.dry_run:
            print(f"\n{Fore.YELLOW}ℹ️ Report exists for {today:%Y-%m-%d}{Style.RESET_ALL}")
            if self._get_choice("View existing? [Y/n]: ", True):
                last = Report.find_one({"generated_at": {"$lt": today}}, sort=[("generated_at", -1)])
                self.print_summary(existing)
                if last:
                    self.print_changes(existing, last)
            return

        followers = self.get_followers()
        following = self.get_following()

        print(f"\n{Fore.BLUE}💾 Updating user DB...{Style.RESET_ALL}")
        User.update_many(followers + following)

        print(f"{Fore.GREEN}✅ User database updated{Style.RESET_ALL}")

        report = self.generate_report(followers, following)
        counts = self.get_relationship_counts(followers, following)
        self.print_summary(report, counts)

        last = Report.find_one({"generated_at": {"$lt": today}}, sort=[("generated_at", -1)])
        if last:
            self.analyse_reports(report, last)
            self.print_changes(report, last)
        else:
            print(f"\n{Fore.YELLOW}ℹ️ This is the first report - no comparison data available.{Style.RESET_ALL}")

        total = time.time() - self.start_time
        print(f"\n{Fore.GREEN}✅ Done in {Fore.YELLOW}{total:.2f}s{Style.RESET_ALL}")


if __name__ == "__main__":
    try:
        InstagramFollower().run()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}⚠️ Interrupted by user{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}❌ Error: {e}{Style.RESET_ALL}")
        raise
