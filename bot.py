import time
import random
from instagrapi import Client

# ========== LOGIN LANGSUNG ==========
cl = Client()
cl.login("barasetiawannk", "BaraGanteng")

def follow_user(username):
    try:
        user_id = cl.user_id_from_username(username)
        cl.user_follow(user_id)
        return f"✅ Followed @{username}"
    except Exception as e:
        return f"❌ Error: {str(e)}"

def unfollow_user(username):
    try:
        user_id = cl.user_id_from_username(username)
        cl.user_unfollow(user_id)
        return f"✅ Unfollowed @{username}"
    except Exception as e:
        return f"❌ Error: {str(e)}"

def like_recent_posts(username, count=5):
    try:
        user_id = cl.user_id_from_username(username)
        medias = cl.user_medias(user_id, count)
        for media in medias:
            cl.media_like(media.id)
            time.sleep(random.uniform(1, 3))
        return f"✅ Liked {len(medias)} posts from @{username}"
    except Exception as e:
        return f"❌ Error: {str(e)}"

def comment_recent_posts(username, text, count=3):
    try:
        user_id = cl.user_id_from_username(username)
        medias = cl.user_medias(user_id, count)
        for media in medias:
            cl.media_comment(media.id, text)
            time.sleep(random.uniform(3, 6))
        return f"✅ Commented '{text}' on {len(medias)} posts from @{username}"
    except Exception as e:
        return f"❌ Error: {str(e)}"

def get_followers(username):
    try:
        user_id = cl.user_id_from_username(username)
        followers = cl.user_followers(user_id)
        return f"📊 @{username} has {len(followers)} followers"
    except Exception as e:
        return f"❌ Error: {str(e)}"

def send_dm(username, message):
    try:
        user_id = cl.user_id_from_username(username)
        cl.direct_send(message, [user_id])
        return f"✅ DM sent to @{username}"
    except Exception as e:
        return f"❌ Error: {str(e)}"

def handle_dm(thread_id, message_id, msg_text, user_id):
    print(f"[DM] {user_id}: {msg_text}")
    parts = msg_text.strip().split()
    if not parts:
        return
    cmd = parts[0].lower()
    args = parts[1:]
    response = ""
    
    if cmd == "/menu":
        response = """
🤖 INSTAGRAM BOT MENU 🤖

/follow <username> - Follow user
/unfollow <username> - Unfollow user
/like <username> <count> - Like posts (default 5)
/comment <username> <text> - Comment on posts
/followers <username> - Cek followers
/dm <username> <message> - Send DM
/status - Cek status bot
        """
    elif cmd == "/follow":
        response = follow_user(args[0]) if args else "❌ Pakai: /follow <username>"
    elif cmd == "/unfollow":
        response = unfollow_user(args[0]) if args else "❌ Pakai: /unfollow <username>"
    elif cmd == "/like":
        if args:
            username = args[0]
            count = int(args[1]) if len(args) > 1 else 5
            response = like_recent_posts(username, count)
        else:
            response = "❌ Pakai: /like <username> <count>"
    elif cmd == "/comment":
        if len(args) >= 2:
            username = args[0]
            text = " ".join(args[1:])
            response = comment_recent_posts(username, text)
        else:
            response = "❌ Pakai: /comment <username> <text>"
    elif cmd == "/followers":
        response = get_followers(args[0]) if args else "❌ Pakai: /followers <username>"
    elif cmd == "/dm":
        if len(args) >= 2:
            username = args[0]
            message = " ".join(args[1:])
            response = send_dm(username, message)
        else:
            response = "❌ Pakai: /dm <username> <message>"
    elif cmd == "/status":
        response = "🟢 Bot aktif! Polling DM berjalan."
    else:
        response = "❌ Perintah tidak dikenal. Ketik /menu"
    
    if response:
        cl.direct_send(response, [user_id])

def poll_dms():
    processed_ids = set()
    print("[+] Polling DM mulai...")
    print("[+] Kirim /menu ke DM akun ini")
    while True:
        try:
            threads = cl.direct_threads()
            for thread in threads:
                for msg in thread.messages:
                    if msg.id in processed_ids:
                        continue
                    if msg.text and msg.user_id != cl.user_id:
                        processed_ids.add(msg.id)
                        handle_dm(thread.id, msg.id, msg.text, msg.user_id)
            time.sleep(3)
        except Exception as e:
            print(f"[-] Polling error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    print("[+] Instagram Bot starting...")
    print("[+] Login sebagai: barasetiawannk")
    poll_dms()