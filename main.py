import os
import sys
import datetime as dt
from typing import Dict, Any, List, Optional

import praw

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
        "flair_text": "Advertising",
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
        "schedule": {
            "freq": "weekly",
            # ISO weekday: 1=Mon … 7=Sun
            "weekday": 1
        },
        "post_type": "markdown",
        "title_template": "⬆️ Straight Up ⬆️ [Vanilla] [SMP] {1.21.8} {No Map Resets} {No Whitelist}",
        "flair_text": "Vanilla",
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
    "schedule": {
        "freq": "weekly",
        # ISO weekday: 1=Mon … 7=Sun
        "weekday": 1
    },
    "post_type": "image",
    "title_template": "No resets, no land claims, and no TPA - just Straight Up vanilla Minecraft since 2019. IP: play.straightupminecraft.com (Java 1.21.8, no whitelist) | Website: https://straightupminecraft.com ",
    "images": ["images/001.png", "images/002.png", "images/003.png", "images/004.png", "images/005.png", "images/006.png", "images/007.png", "images/008.png", "images/009.png"]
    },

    # MONTHLY POSTS
    "r/MCServerAds": {
        "schedule": {"freq": "monthly", "monthday": 1},  # 1..28/29/30/31
        "post_type": "image",
        "title_template": "No resets, no land claims, and no TPA - just Straight Up vanilla Minecraft since 2019. IP: play.straightupminecraft.com (Java 1.21.8, no whitelist) | Website: https://straightupminecraft.com ",
        "images": ["images/001.png", "images/002.png", "images/003.png", "images/004.png", "images/005.png", "images/006.png", "images/007.png", "images/008.png", "images/009.png"]
    },
    "r/mcpublicservers": {
        "schedule": {"freq": "monthly", "monthday": 1},  # 1..28/29/30/31
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
    """Return True if this subreddit is scheduled to post TODAY (UTC)."""
    freq = (sched.get("freq") or "").lower()
    if freq == "daily":
        return True

    if freq == "weekly":
        # ISO weekday: Monday=1 ... Sunday=7
        target = int(sched.get("weekday", 1))
        return now_utc.isoweekday() == target

    if freq == "monthly":
        target = int(sched.get("monthday", 1))
        # Guard against months with fewer days:
        last_day = (now_utc.replace(day=28) + dt.timedelta(days=4)).replace(day=1) - dt.timedelta(days=1)
        safe_target = min(target, last_day.day)
        return now_utc.day == safe_target

    # Unknown frequency -> don't post
    return False


def pick_rotating_image(images: List[str], now_utc: dt.datetime) -> Optional[str]:
    """
    Pick ONE image for today with weekly-reset rotation.
    - Mon resets the cycle (index 0).
    - If fewer than 7 images, wrap around with modulo.
    """
    if not images:
        return None

    # Monday=1 -> index 0; Tuesday=2 -> index 1; ... Sunday=7 -> index 6
    weekday_index = now_utc.isoweekday() - 1  # 0..6
    idx = weekday_index % len(images)
    path = images[idx]

    # Ensure the file exists (for GitHub Actions runner)
    if not os.path.exists(path):
        print(f"[WARN] Image not found at '{path}'.", file=sys.stderr)
        return None

    return path


def build_title(template: str) -> str:
    """
    Return the exact title string from the config.
    """
    if not template:
        return "⬆️ Straight Up ⬆️ [Vanilla] [Survival] {1.21.8} {No Whitelist} {No Map Resets}" # Fallback
    return template.strip()

def apply_flair_if_any(reddit: praw.Reddit, submission, target: str, flair_text: Optional[str]):
    if not flair_text:
        return
    try:
        for tpl in reddit.subreddit(target).flair.link_templates.user_selectable():
            if str(tpl.get("text","")).lower() == flair_text.lower():
                submission.flair.select(tpl["id"], flair_text)
                print(f"[INFO] Applied flair '{flair_text}' on {target}")
                return
        print(f"[WARN] Flair '{flair_text}' not found or not user-selectable on {target}.")
    except Exception as e:
        print(f"[WARN] Could not apply flair on {target}: {e}")



def reddit_client_from_env() -> praw.Reddit:
    try:
        return praw.Reddit(
            client_id=os.environ["REDDIT_CLIENT_ID"],
            client_secret=os.environ["REDDIT_CLIENT_SECRET"],
            username=os.environ["REDDIT_USERNAME"],
            password=os.environ["REDDIT_PASSWORD"],
            user_agent=f"StraightUpAds by u/{os.environ.get('REDDIT_USERNAME','unknown')}"
        )
    except KeyError as e:
        missing = str(e).strip("'")
        raise RuntimeError(
            f"Missing required environment variable: {missing}. ")


def post_markdown(reddit: praw.Reddit, target: str, title: str, body_md: str, flair_text: Optional[str]):
    if DRY_RUN:
        print(f"[DRY RUN] Would POST markdown to {target}\n  Title: {title}\n  Flair: {flair_text or '(none)'}\n  Body (first 120): {body_md[:120]!r}")
        return
    submission = reddit.subreddit(target).submit(title=title, selftext=body_md)
    apply_flair_if_any(reddit, submission, target, flair_text)

def post_image(reddit: praw.Reddit, target: str, title: str, image_path: str, flair_text: Optional[str]):
    """
    Post all configured images as a gallery, rotating which one appears first each day.
    """
    images = CONFIG.get(target, {}).get("images", [])
    if not images:
        print(f"[WARN] {target}: No images configured.")
        return

    if image_path in images:
        first_index = images.index(image_path)
        rotated_images = images[first_index:] + images[:first_index]
    else:
        rotated_images = images

    gallery_items = [{"image_path": img} for img in rotated_images if os.path.exists(img)]

    if not gallery_items:
        print(f"[WARN] {target}: No valid images found for gallery.")
        return

    if DRY_RUN:
        print(f"[DRY RUN] Would POST gallery to {target}\n  Title: {title}\n  Images: {[i['image_path'] for i in gallery_items]}\n  Flair: {flair_text or '(none)'}")
        return

    submission = reddit.subreddit(target).submit_gallery(title=title, images=gallery_items)
    apply_flair_if_any(reddit, submission, target, flair_text)



# =======
# MAIN
# =======
def main() -> int:
    reddit = reddit_client_from_env()
    any_attempted = False

    for target, cfg in CONFIG.items():
        sched = cfg.get("schedule", {})
        if not should_post_today(sched, UTC_NOW):
            print(f"[SKIP] {target}: Not scheduled today (UTC).")
            continue

        post_type = (cfg.get("post_type") or "markdown").lower()
        title = build_title(cfg.get("title_template"))

        if post_type == "markdown":
            body = cfg.get("body_md", "").strip()
            if not body:
                print(f"[WARN] {target}: post_type=markdown but body_md is empty. Skipping.")
                continue
            print(f"[INFO] Posting MARKDOWN to {target} with title '{title}'")
            post_markdown(reddit, target, title, body, cfg.get("flair_text"))
            any_attempted = True

        elif post_type == "image":
            images = cfg.get("images") or []
            img = pick_rotating_image(images, UTC_NOW)
            if not img:
                print(f"[WARN] {target}: No valid image resolved (check paths). Skipping.")
                continue
            print(f"[INFO] Posting IMAGE to {target} with title '{title}' -> {img}")
            post_image(reddit, target, title, img, cfg.get("flair_text"))
            any_attempted = True

        else:
            print(f"[WARN] {target}: Unknown post_type='{post_type}'. Skipping.")

    if not any_attempted:
        print("[INFO] No posts attempted today (nothing scheduled or misconfigured).")
    else:
        print("[OK] Finished scheduled run.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
