"""Standalone collector script - Run collection from command line"""

import sys
import argparse
from pathlib import Path

# Add app directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.config import Config
from app.collector import collect_posts


def main():
    parser = argparse.ArgumentParser(
        description="Misinformation Debunking Copilot - Post Collector"
    )

    parser.add_argument(
        '--max-posts',
        type=int,
        default=Config.DEFAULT_MAX_POSTS_PER_TARGET,
        help='Maximum posts to collect per target'
    )

    parser.add_argument(
        '--max-targets',
        type=int,
        default=Config.DEFAULT_MAX_TARGETS_PER_RUN,
        help='Maximum targets to process'
    )

    parser.add_argument(
        '--scroll-passes',
        type=int,
        default=Config.DEFAULT_SCROLL_PASSES,
        help='Number of scroll passes per target'
    )

    parser.add_argument(
        '--scroll-delay',
        type=float,
        default=Config.DEFAULT_SCROLL_DELAY,
        help='Delay between scrolls in seconds'
    )

    parser.add_argument(
        '--headless',
        action='store_true',
        help='Run browser in headless mode'
    )

    args = parser.parse_args()

    print("=" * 60)
    print("Misinformation Debunking Copilot - Collector")
    print("=" * 60)
    print()

    # Load targets
    targets = Config.load_targets()

    if not targets:
        print("❌ No targets found in data/targets.json")
        print("Please add targets to the configuration file.")
        sys.exit(1)

    print(f"📋 Loaded {len(targets)} targets")
    print(f"⚙️  Settings:")
    print(f"   - Max posts per target: {args.max_posts}")
    print(f"   - Max targets: {args.max_targets}")
    print(f"   - Scroll passes: {args.scroll_passes}")
    print(f"   - Scroll delay: {args.scroll_delay}s")
    print(f"   - Headless: {args.headless}")
    print()

    # Limit targets
    targets_to_process = targets[:args.max_targets]

    print("🎯 Targets to process:")
    for i, target in enumerate(targets_to_process, 1):
        print(f"   {i}. {target['name']} ({target.get('type', 'page')})")
    print()

    # Confirm
    response = input("Continue? [y/N]: ")
    if response.lower() != 'y':
        print("Cancelled.")
        sys.exit(0)

    print()
    print("🚀 Starting collection...")
    print()

    # Run collection
    def progress_callback(msg):
        print(f"   {msg}")

    try:
        stats = collect_posts(
            targets=targets_to_process,
            max_posts_per_target=args.max_posts,
            scroll_passes=args.scroll_passes,
            scroll_delay=args.scroll_delay,
            headless=args.headless,
            progress_callback=progress_callback
        )

        print()
        print("=" * 60)
        print("✅ Collection Complete")
        print("=" * 60)
        print(f"Targets processed: {stats['targets_processed']}")
        print(f"Posts collected: {stats['posts_collected']}")

        if stats['errors']:
            print(f"\n⚠️  Errors encountered: {len(stats['errors'])}")
            for error in stats['errors']:
                print(f"   - {error}")

        print()
        print("Next steps:")
        print("1. Run the Streamlit dashboard: streamlit run app/ui.py")
        print("2. Review collected posts and generate rebuttals")
        print("3. Copy drafts and manually post them on Facebook")
        print()

    except KeyboardInterrupt:
        print("\n\n⚠️  Collection interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Collection failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
