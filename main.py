import os
import sys
import time
import datetime as dt
from typing import Dict, Any, List, Optional

import praw
from praw.exceptions import RedditAPIException

# ==================
# RUNTIME SETTINGS
# ==================
DRY_RUN = False  # Set True to test without actually posting

UTC_NOW = dt.datetime.utcnow()  # All scheduling is done in UTC

# ===================
# SUBREDDIT CONFIG
# ===================
CONFIG: Dict[str, Dict[str, Any]] = {
    # DAILY POSTS
    "r/MCVanillaServers": {
        "schedule": {"freq": "daily"},
        "post_type": "markdown",
        "title_template": "⬆️ Straight Up ⬆️ [Vanilla] [Survival] {1.21.8} {No Whitelist} {No Map Resets}",
        "body_md": (
            "**Server IP (Java Edition)**: play.straightupminecraft.com\n\n"
            "**Join us on Discord**: [https://discord.gg/camSwwyUAe](https://discord.gg/camSwwyUAe)\n\n"
            "**Check out our website**: [https://straightupminecraft.com](https://straightupminecraft.com)\n\n"
            "## **About Straight Up:**\n\n"
            "> \"Everyone’s forever world.\"\n\n"
            "No resets, no land claims, and no TPA - just “Straight Up” vanilla Minecraft. "
            "The overworld has never been wiped since our founding date of April 1^(st), 2019, "
            "and we intend to keep it that way. With a rich history spanning over 6 years, "
            "there is much to explore and many adventures to be had.\n\n"
            "🚫 **No /tpa and no /home.** No currency, factions, or economy plugins that ruin the vanilla experience. "
            "Just Straight Up survival Minecraft. The way the game was meant to be played.\n\n"
            "🌎 **No world resets.** Many servers boast this, but few have stuck around as long as we have (6 years!).\n\n"
            "🧨 **PvP and griefing permitted.** No land claims or protected areas.\n\n"
            "🔊 **Proximity chat.** We have server-side support for the Simple Voice Chat mod (optional: requires client-side mod)\n\n"
            "💻 **Stable server performance.** The server is carefully optimized without cutting into the gameplay experience.\n\n"
            "‼️ **Unintrusive anticheat.** We aim to put vanilla players on a fair footing and prevent exploits from ruining the server experience.\n\n"
            "### Want more details? [Here](https://straightupminecraft.com) is a link to our website. "
            "Additional questions? Reach out to us on [Discord](https://discord.gg/camSwwyUAe)!"
        ),
    },
    "r/MinecraftServer": {
        "schedule": {"freq": "daily"},
        "post_type": "image",
        "title_template": "No resets, no land claims, and no TPA - just Straight Up vanilla Minecraft since 2019. IP: play.straightupminecraft.com (Java 1.21.8, no whitelist) | Discord: https://discord.gg/camSwwyUAe | Website: https://straightupminecraft.com",
        "images": ["images/001.png", "images/002.png", "images/003.png", "images/004.png", "images/005.png", "images/006.png", "images/007.png", "images/008.png", "images/009.png"]
    },
    "r/MinecraftServerFinder": {
        "schedule": {"freq": "daily"},
        "post_type": "image",
        "flair_id": "da524996-0140-11ec-9f06-f697810cb0d0",
        "title_template": "No resets, no land claims, and no TPA - just Straight Up vanilla Minecraft since 2019. IP: play.straightupminecraft.com (Java 1.21.8, no whitelist) | Discord: https://discord.gg/camSwwyUAe | Website: https://straightupminecraft.com",
        "images": ["images/001.png", "images/002.png", "images/003.png", "images/004.png", "images/005.png", "images/006.png", "images/007.png", "images/008.png", "images/009.png"]
    },
    "r/MinecraftServerShare": {
        "schedule": {"freq": "daily"},
        "post_type": "image",
        "title_template": "No resets, no land claims, and no TPA - just Straight Up vanilla Minecraft since 2019. IP: play.straightupminecraft.com (Java 1.21.8, no whitelist) | Discord: https://discord.gg/camSwwyUAe | Website: https://straightupminecraft.com",
        "images": ["images/001.png", "images/002.png", "images/003.png", "images/004.png", "images/005.png", "images/006.png", "images/007.png", "images/008.png", "images/009.png"]
    },

    # WEEKLY POSTS
    "r/mcservers": {
        "schedule": {"freq": "weekly", "weekday": 1},
        "post_type": "markdown",
        "title_template": "⬆️ Straight Up ⬆️ [Vanilla] [SMP] {1.21.8} {No Map Resets} {No Whitelist}",
        "flair_id": "03ff495c-d099-11eb-9732-0e0a754ed6b5",
        "body_md": (
            "**Server IP (Java Edition)**: play.straightupminecraft.com\n\n"
            "**Join us on Discord**: [https://discord.gg/camSwwyUAe](https://discord.gg/camSwwyUAe)\n\n"
            "**Check out our website**: [https://straightupminecraft.com](https://straightupminecraft.com)\n\n"
            "## **About Straight Up:**\n\n"
            "> \"Everyone’s forever world.\"\n\n"
            "No resets, no land claims, and no TPA - just “Straight Up” vanilla Minecraft. "
            "The overworld has never been wiped since our founding date of April 1^(st), 2019, "
            "and we intend to keep it that way. With a rich history spanning over 6 years, "
            "there is much to explore and many adventures to be had.\n\n"
            "🚫 **No /tpa and no /home.** No currency, factions, or economy plugins that ruin the vanilla experience. "
            "Just Straight Up survival Minecraft. The way the game was meant to be played.\n\n"
            "🌎 **No world resets.** Many servers boast this, but few have stuck around as long as we have (6 years!).\n\n"
            "🧨 **PvP and griefing permitted.** No land claims or protected areas.\n\n"
            "🔊 **Proximity chat.** We have server-side support for the Simple Voice Chat mod (optional: requires client-side mod)\n\n"
            "💻 **Stable server performance.** The server is carefully optimized without cutting into the gameplay experience.\n\n"
            "‼️ **Unintrusive anticheat.** We aim to put vanilla players on a fair footing and prevent exploits from ruining the server experience.\n\n"
            "### Want more details? [Here](https://straightupminecraft.com) is a link to our website. "
            "Additional questions? Reach out to us on [Discord](https://discord.gg/camSwwyUAe)!"
        ),
    },
    "r/MinecraftSMPs": {
        "schedule": {"freq": "weekly", "weekday": 1},
        "post_type": "image",
        "title_template": "No resets, no land claims, and no TPA - just Straight Up vanilla Minecraft since 2019. IP: play.straightupminecraft.com (Java 1.21.8, no whitelist) | Website: https://straightupminecraft.com ",
        "images": ["images/001.png", "images/002.png", "images/003.png", "images/004.png", "images/005.png", "images/006.png", "images/007.png", "images/008.png", "images/009.png"]
    },

    # MONTHLY POSTS
    "r/MCServerAds": {
        "schedule": {"freq": "monthly", "monthday": 1},
        "post_type": "image",
        "title_template": "No resets, no land claims, and no TPA - just Straight Up vanilla Minecraft since 2019. IP: play.straightupminecraft.com (Java 1.21.8, no whitelist) | Website: https://straightupminecraft.com ",
        "images": ["images/001.png", "images/002.png", "images/003.png", "images/004.png", "images/005.png", "images/006.png", "images/007.png", "images/008.png", "images/009.png"]
    },
    "r/mcpublicservers": {
        "schedule": {"freq": "monthly", "monthday": 1},
        "post_type": "markdown",
        "title_template": "⬆️ Straight Up ⬆️ [Vanilla] [Survival] {1.21.8} {No Whitelist} {No Map Resets}",
        "body_md": (
            "**Server IP (Java Edition)**: play.straightupminecraft.com\n\n"
            "**Join us on Discord**: [https://discord.gg/camSwwyUAe](https://discord.gg/camSwwyUAe)\n\n"
            "**Check out our website**: [https://straightupminecraft.com](https://straightupminecraft.com)\n\n"
            "## **About Straight Up:**\n\n"
            "> \"Everyone’s forever world.\"\n\n"
            "No resets, no land claims, and no TPA - just “Straight Up” vanilla Minecraft. "
            "The overworld has never been wiped since our founding date of April 1^(st), 2019, "
            "and we intend to keep it that way. With a rich history spanning over 6 years, "
            "there is much to explore and many adventures to be had.\n\n"
            "🚫 **No /tpa and no /home.** No currency, factions, or economy plugins that ruin the vanilla experience. "
            "Just Straight Up survival Minecraft. The way the game was meant to be played.\n\n"
            "🌎 **No world resets.** Many servers boast this, but few have stuck around as long as we have (6 years!).\n\n"
            "🧨 **PvP and griefing permitted.** No land claims or protected areas.\n\n"
            "🔊 **Proximity chat.** We have server-side support for the Simple Voice Chat mod (optional: requires client-side mod)\n\n"
            "💻 **Stable server performance.** The server is carefully optimized without cutting into the gameplay experience.\n\n"
            "‼️ **Unintrusive anticheat.** We aim to put vanilla players on a fair footing and prevent exploits from ruining the server experience.\n\n"
            "### Want more details? [Here](https://straightupminecraft.com) is a link to our website. "
            "Additional questions? Reach out to us on [Discord](https://discord.gg/camSwwyUAe)!"
        ),
    },
}

# ============
# HELPERS
# ============
def should_post_today(sched: Dict[str, Any], now_utc: dt.datetime) -> bool:
    freq = (sched.get("freq") or "").lower()
    if freq == "daily":
        return True
    if freq == "weekly":
        return now_utc.isoweekday() == int(sched.get("weekday", 1))
    if freq == "monthly":
        target = int(sched.get("monthday", 1))
        last_day = (now_utc.replace(day=28) + dt.timedelta(days=4)).replace(day=1) - dt.timedelta(days=1)
        return now_utc.day == min(target, last_day.day)
    return False

def pick_rotating_image(images: List[str], now_utc: dt.datetime) -> Optional[str]:
    if not images:
        return None
    idx = (now_utc.isoweekday() - 1) % len(images)
    path = images[idx]
    if not os.path.exists(path):
        print(f"[WARN] Image not found at '{path}'.", file=sys.stderr)
        return None
    return path

def build_title(template: str) -> str:
    return template.strip() if template else "⬆️ Straight Up ⬆️ [Vanilla] [Survival] {1.21.8} {No Whitelist} {No Map Resets}"

def reddit_client_from_env() -> praw.Reddit:
    return praw.Reddit(
        client_id=os.environ["REDDIT_CLIENT_ID"],
        client_secret=os.environ["REDDIT_CLIENT_SECRET"],
        username=os.environ["REDDIT_USERNAME"],
        password=os.environ["REDDIT_PASSWORD"],
        user_agent=f"StraightUpAds by u/{os.environ.get('REDDIT_USERNAME','unknown')}"
    )

def post_markdown(reddit: praw.Reddit, target: str, title: str, body_md: str, flair_id: Optional[str], flair_text: Optional[str]):
    if DRY_RUN:
        print(f"[DRY RUN] Would POST markdown to {target}\n  Title: {title}\n  Flair ID: {flair_id or '(none)'}")
        return
    try:
        submission = reddit.subreddit(target).submit(title=title, selftext=body_md, flair_id=flair_id, flair_text=flair_text)
        print(f"[INFO] Submitted markdown post to {target} (id={submission.id})")
    except Exception as e:
        print(f"[ERROR] Failed posting markdown to {target}: {repr(e)}")

def post_image(reddit: praw.Reddit, target: str, title: str, image_path: str, flair_id: Optional[str], flair_text: Optional[str]):
    images = CONFIG.get(target, {}).get("images", [])
    if not images:
        print(f"[WARN] {target}: No images configured.")
        return
    rotated_images = images[images.index(image_path):] + images[:images.index(image_path)]
    gallery_items = [{"image_path": img} for img in rotated_images if os.path.exists(img)]
    if not gallery_items:
        print(f"[WARN] {target}: No valid images for gallery.")
        return
    if DRY_RUN:
        print(f"[DRY RUN] Would POST gallery to {target}\n  Flair ID: {flair_id or '(none)'}")
        return
    try:
        submission = reddit.subreddit(target).submit_gallery(title=title, images=gallery_items, flair_id=flair_id, flair_text=flair_text)
        print(f"[INFO] Submitted gallery to {target} (id={submission.id})")
    except Exception as e:
        print(f"[ERROR] Failed posting gallery to {target}: {repr(e)}")

# =======
# MAIN
# =======
def main() -> int:
    reddit = reddit_client_from_env()
    any_attempted = False
    print("[INFO] Waiting 15 minutes before first post to avoid Reddit spam filters...")
    time.sleep(900)

    for target, cfg in CONFIG.items():
        if not should_post_today(cfg.get("schedule", {}), UTC_NOW):
            print(f"[SKIP] {target}: Not scheduled today (UTC).")
            continue

        title = build_title(cfg.get("title_template"))
        flair_id = cfg.get("flair_id")
        flair_text = cfg.get("flair_text")
        post_type = (cfg.get("post_type") or "markdown").lower()

        if post_type == "markdown":
            body = cfg.get("body_md", "").strip()
            if not body:
                print(f"[WARN] {target}: Markdown body empty. Skipping.")
            else:
                print(f"[INFO] Posting MARKDOWN to {target} with title '{title}'")
                post_markdown(reddit, target, title, body, flair_id, flair_text)
                any_attempted = True
        elif post_type == "image":
            img = pick_rotating_image(cfg.get("images") or [], UTC_NOW)
            if not img:
                print(f"[WARN] {target}: No valid image. Skipping.")
            else:
                print(f"[INFO] Posting IMAGE to {target} with title '{title}' -> {img}")
                post_image(reddit, target, title, img, flair_id, flair_text)
                any_attempted = True
        else:
            print(f"[WARN] {target}: Unknown post_type='{post_type}'. Skipping.")

        time.sleep(180)

    print("[OK] Finished scheduled run." if any_attempted else "[INFO] No posts attempted today.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())