"""Facebook post collector using Playwright"""

import time
import re
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional, Callable
from playwright.sync_api import sync_playwright, Browser, Page, TimeoutError as PlaywrightTimeout

from .config import Config, BROWSER_PROFILE_DIR, SCREENSHOTS_DIR
from .storage import get_storage
from .scoring import MisinfoScorer


class FacebookCollector:
    """Collects posts from Facebook using Playwright"""

    def __init__(
        self,
        headless: bool = None,
        progress_callback: Optional[Callable[[str], None]] = None
    ):
        self.headless = headless if headless is not None else Config.BROWSER_HEADLESS
        self.progress_callback = progress_callback or (lambda x: print(x))
        self.storage = get_storage()
        self.scorer = MisinfoScorer()

    def collect_from_targets(
        self,
        targets: List[Dict[str, Any]],
        max_posts_per_target: int = 20,
        scroll_passes: int = 3,
        scroll_delay: float = 2.0
    ) -> Dict[str, Any]:
        """
        Collect posts from multiple targets

        Args:
            targets: List of target dicts with 'name', 'url', 'type'
            max_posts_per_target: Max posts to collect per target
            scroll_passes: Number of scroll passes
            scroll_delay: Delay between scrolls in seconds

        Returns:
            Dict with collection stats
        """
        stats = {
            'targets_processed': 0,
            'posts_collected': 0,
            'errors': []
        }

        with sync_playwright() as p:
            # Launch browser with persistent context (preserves login)
            browser_context = p.chromium.launch_persistent_context(
                user_data_dir=str(BROWSER_PROFILE_DIR),
                headless=self.headless,
                viewport={'width': 1280, 'height': 720},
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--disable-dev-shm-usage',
                    '--no-sandbox'
                ]
            )

            try:
                page = browser_context.pages[0] if browser_context.pages else browser_context.new_page()
                page.set_default_timeout(Config.BROWSER_TIMEOUT)

                for target in targets:
                    try:
                        self.progress_callback(f"Processing target: {target['name']}")
                        collected = self._collect_from_target(
                            page,
                            target,
                            max_posts_per_target,
                            scroll_passes,
                            scroll_delay
                        )
                        stats['posts_collected'] += collected
                        stats['targets_processed'] += 1

                    except Exception as e:
                        error_msg = f"Error processing {target['name']}: {str(e)}"
                        self.progress_callback(error_msg)
                        stats['errors'].append(error_msg)

            finally:
                browser_context.close()

        return stats

    def _collect_from_target(
        self,
        page: Page,
        target: Dict[str, Any],
        max_posts: int,
        scroll_passes: int,
        scroll_delay: float
    ) -> int:
        """Collect posts from a single target"""
        target_name = target['name']
        target_url = target['url']

        self.progress_callback(f"Navigating to {target_url}")

        try:
            # Navigate to target
            page.goto(target_url, wait_until='networkidle', timeout=60000)
            time.sleep(3)  # Let page settle

            # Handle potential dialogs/popups
            self._handle_facebook_dialogs(page)

            # Scroll to load more posts
            self.progress_callback(f"Scrolling to load posts (passes: {scroll_passes})...")
            for i in range(scroll_passes):
                page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                time.sleep(scroll_delay)
                self.progress_callback(f"Scroll pass {i+1}/{scroll_passes}")

            # Scroll back to top
            page.evaluate("window.scrollTo(0, 0)")
            time.sleep(1)

            # Extract posts
            self.progress_callback(f"Extracting posts...")
            posts = self._extract_posts(page, target_name, max_posts)

            self.progress_callback(f"Collected {len(posts)} posts from {target_name}")
            return len(posts)

        except PlaywrightTimeout:
            self.progress_callback(f"Timeout loading {target_url}")
            return 0
        except Exception as e:
            self.progress_callback(f"Error: {str(e)}")
            return 0

    def _handle_facebook_dialogs(self, page: Page):
        """Handle common Facebook dialogs and popups"""
        try:
            # Close cookie consent
            selectors = [
                'button[data-cookiebanner="accept_button"]',
                'button[title="Accept All"]',
                'button:has-text("Accept")',
                'button:has-text("Allow")',
                '[aria-label="Close"]'
            ]

            for selector in selectors:
                try:
                    button = page.locator(selector).first
                    if button.is_visible(timeout=2000):
                        button.click(timeout=2000)
                        time.sleep(1)
                except:
                    pass

        except Exception as e:
            # Dialogs are optional, continue if they fail
            pass

    def _extract_posts(self, page: Page, target_name: str, max_posts: int) -> List[Dict[str, Any]]:
        """Extract post data from page"""
        posts = []

        # Facebook post selectors (these may need updating as FB changes)
        # We'll try multiple selectors for robustness
        post_selectors = [
            '[data-ad-preview="message"]',  # Post content
            '[role="article"]',  # Article containers
            'div[class*="userContentWrapper"]',  # Legacy
            'div.x1yztbdb'  # Newer FB class pattern
        ]

        collected_texts = set()  # Avoid duplicates

        for selector in post_selectors:
            try:
                elements = page.locator(selector).all()
                self.progress_callback(f"Found {len(elements)} elements with selector {selector}")

                for elem in elements[:max_posts * 2]:  # Check extra for filtering
                    if len(posts) >= max_posts:
                        break

                    try:
                        post_data = self._extract_post_data(page, elem, target_name)

                        if post_data and post_data['text_content']:
                            # Avoid duplicates
                            text_key = post_data['text_content'][:100]
                            if text_key not in collected_texts:
                                collected_texts.add(text_key)
                                posts.append(post_data)

                    except Exception as e:
                        continue  # Skip problematic posts

                if len(posts) >= max_posts:
                    break

            except Exception as e:
                continue

        return posts[:max_posts]

    def _extract_post_data(self, page: Page, element, target_name: str) -> Optional[Dict[str, Any]]:
        """Extract data from a single post element"""
        try:
            # Extract text content
            text_content = element.inner_text().strip()

            if not text_content or len(text_content) < 20:
                return None

            # Try to extract author
            author = None
            try:
                # Multiple possible selectors for author name
                author_selectors = [
                    'a[role="link"] strong',
                    'h2 span',
                    'strong > span',
                    'a[aria-label]'
                ]
                for selector in author_selectors:
                    author_elem = element.locator(selector).first
                    if author_elem.is_visible(timeout=500):
                        author = author_elem.inner_text().strip()
                        if author:
                            break
            except:
                pass

            # Try to extract post URL
            post_url = None
            try:
                # Look for timestamp link which usually has post URL
                link = element.locator('a[href*="/posts/"], a[href*="/permalink/"], a[href*="/photo"]').first
                if link.is_visible(timeout=500):
                    href = link.get_attribute('href')
                    if href:
                        # Normalize URL
                        if href.startswith('/'):
                            post_url = f"https://www.facebook.com{href}"
                        elif not href.startswith('http'):
                            post_url = f"https://www.facebook.com/{href}"
                        else:
                            post_url = href
            except:
                pass

            # Take screenshot
            screenshot_filename = f"{target_name}_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}.png"
            screenshot_path = SCREENSHOTS_DIR / screenshot_filename

            try:
                element.screenshot(path=str(screenshot_path), timeout=5000)
            except:
                # If element screenshot fails, try viewport screenshot
                try:
                    element.scroll_into_view_if_needed(timeout=2000)
                    page.screenshot(path=str(screenshot_path))
                except:
                    screenshot_path = None

            # Store in database
            post_id = self.storage.add_post(
                target_name=target_name,
                url=post_url,
                author=author,
                text_content=text_content,
                screenshot_path=str(screenshot_path.name) if screenshot_path else None
            )

            # Score the post
            try:
                score_result = self.scorer.score_post(text_content)
                self.storage.update_post(
                    post_id,
                    misinfo_score=score_result['score'],
                    tags=score_result['tags'],
                    rationale=score_result['rationale'],
                    fact_check_questions=score_result['fact_check_questions']
                )
            except Exception as e:
                self.progress_callback(f"Scoring failed for post {post_id}: {e}")

            return {
                'id': post_id,
                'text_content': text_content,
                'author': author,
                'url': post_url
            }

        except Exception as e:
            return None

    def test_with_sample_html(self, html_file: Path) -> Dict[str, Any]:
        """
        Dry run mode: Test with local HTML file instead of Facebook

        Args:
            html_file: Path to sample HTML file

        Returns:
            Collection stats
        """
        stats = {
            'targets_processed': 1,
            'posts_collected': 0,
            'errors': []
        }

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            try:
                # Load local HTML
                page.goto(f"file://{html_file.absolute()}")
                time.sleep(1)

                # Extract posts using same logic
                posts = self._extract_posts(page, "Sample_Target", max_posts=10)
                stats['posts_collected'] = len(posts)

            except Exception as e:
                stats['errors'].append(str(e))
            finally:
                browser.close()

        return stats


def collect_posts(
    targets: List[Dict[str, Any]],
    max_posts_per_target: int = 20,
    scroll_passes: int = 3,
    scroll_delay: float = 2.0,
    headless: bool = None,
    progress_callback: Optional[Callable[[str], None]] = None
) -> Dict[str, Any]:
    """
    Convenience function to collect posts

    Args:
        targets: List of target dicts
        max_posts_per_target: Max posts per target
        scroll_passes: Number of scroll passes
        scroll_delay: Delay between scrolls
        headless: Run browser in headless mode
        progress_callback: Optional callback for progress updates

    Returns:
        Collection statistics
    """
    collector = FacebookCollector(headless=headless, progress_callback=progress_callback)
    return collector.collect_from_targets(
        targets,
        max_posts_per_target=max_posts_per_target,
        scroll_passes=scroll_passes,
        scroll_delay=scroll_delay
    )
