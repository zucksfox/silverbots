import requests
import random
import io
import os
from PIL import Image

STRUK_FOLDER = r"C:\Users\hp\Downloads\botsilver\struk\struk"
MAX_RECEIPT_UPLOAD = 5

# Baca semua token dari file
def load_tokens(filepath="token.txt"):
    with open(filepath, "r") as f:
        return [line.strip() for line in f if line.strip()]

# Header Authorization Bearer
def get_headers(token):
    return {
        "Authorization": token,
        "Accept": "application/json",
    }

# Ambil profil dan return kuota cerita + struk
def get_profile(headers):
    res = requests.get("https://coklatmerdeka.silverqueen.id/api/me", headers=headers)
    res.raise_for_status()
    profile = res.json()["data"]
    print(f"👤 {profile['name']} | 🏆 Poin: {profile['total_point']} | Rank {profile['rank']} | Upload cerita hari ini: {profile['message_upload_today']}/5 | Upload struk: {profile['receipt_upload_today']}/5")
    return {
        "story_quota": profile["available_quotas"],
        "receipt_uploaded": profile["receipt_upload_today"]
    }

# Ambil daftar kota
def get_cities():
    res = requests.get("https://coklatmerdeka.silverqueen.id/api/cities")
    res.raise_for_status()
    return res.json()["data"]

# Template cerita berdasarkan nama kota
def generate_story(city_name):
    templates = [
        f"Liburan ke {city_name} adalah momen paling menyenangkan di masa kecilku.",
        f"Kenangan terbaikku adalah saat makan coklat bareng teman-teman di {city_name}.",
        f"Di {city_name}, aku pertama kali merasakan hangatnya persahabatan dan manisnya coklat.",
        f"{city_name} selalu mengingatkanku pada tawa, coklat, dan kenangan indah masa kecil.",
    ]
    return random.choice(templates)

# Ambil gambar random dari picsum.photos
def get_random_image():
    img_url = f"https://picsum.photos/400/300?random={random.randint(1, 99999)}"
    res = requests.get(img_url)
    img = Image.open(io.BytesIO(res.content))
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    buf.seek(0)
    return ("upload.jpg", buf, "image/jpeg")


def share_message(headers, message_id):
    res = requests.post(
        f"https://coklatmerdeka.silverqueen.id/api/messages/{message_id}/share",
        headers=headers
    )

    if res.status_code == 200:
        data = res.json()["data"]
        shared_count = data.get("shared_count", 0)
        points = data.get("points_awarded", 0)
        print(f"🔗 Shared! Total: {shared_count} | Poin: {points}")

        if shared_count >= 5:
            print("⚠️ Sudah mencapai batas share harian.")
            return False  # stop jika sudah limit
        return True

    else:
        try:
            error_message = res.json().get("message", "")
            print(f"❌ Gagal share: {res.status_code} | {error_message}")
            if "limit" in error_message.lower():
                print("⚠️ Share sudah limit.")
                return False
        except:
            print(f"❌ Gagal share: {res.status_code}")
        return False


# Submit cerita dan gambar random
def submit_story(headers, city_id, city_name, story):
    image_file = get_random_image()
    data = {
        "city_id": str(city_id),
        "title": "Cerita Manis #2",
        "content": story,
    }

    res = requests.post(
        "https://coklatmerdeka.silverqueen.id/api/messages",
        headers=headers,
        files={"image": get_random_image()},
        data=data,
    )

    if res.status_code not in [200, 201]:
        print(f"❌ Gagal kirim cerita. Status: {res.status_code}")
        return False

    try:
        message_id = res.json()["data"]["id"]
    except Exception as e:
        print("⚠️ Gagal ambil ID pesan:", e)
        return False

    print(f"✅ Cerita berhasil dikirim ke {city_name}! ID: {message_id}")
    share_message(headers, message_id)

    return True

def get_random_struk():
    files = [f for f in os.listdir(STRUK_FOLDER) if f.lower().endswith((".jpg", ".jpeg", ".png"))]
    if not files:
        return None
    return os.path.join(STRUK_FOLDER, random.choice(files))

# Submit struk dari folder lokal
def submit_receipt(headers, receipt_uploaded_count):
    remaining_quota = MAX_RECEIPT_UPLOAD - receipt_uploaded_count
    if remaining_quota <= 0:
        print("⛔ Batas upload struk hari ini tercapai.")
        return

    files_available = [f for f in os.listdir(STRUK_FOLDER) if f.lower().endswith((".jpg", ".jpeg", ".png"))]
    if not files_available:
        print("🚫 Tidak ada file struk ditemukan di folder.")
        return

    print(f"📤 Upload struk tersisa hari ini: {remaining_quota}")

    # Acak daftar file agar tidak selalu kirim file yang sama
    random.shuffle(files_available)

    for i in range(min(remaining_quota, len(files_available))):
        filename = files_available[i]
        filepath = os.path.join(STRUK_FOLDER, filename)

        with open(filepath, "rb") as file:
            files = {
                "file": (filename, file, "image/jpeg")
            }
            res = requests.post(
                "https://coklatmerdeka.silverqueen.id/api/receipt/upload",
                headers=headers,
                files=files
            )

        if res.status_code == 201 and res.json().get("success"):
            file_url = res.json()["data"]["file"]
            print(f"✅ [{i+1}] Struk berhasil dikirim: {filename}")
            print("   📎", file_url)
        else:
            print(f"❌ [{i+1}] Gagal kirim struk: {filename}")
            print("   🔎 Response:", res.text)


# Proses satu token: cerita dan struk
def process_token(token, cities):
    headers = get_headers(token)
    try:
        profile = get_profile(headers)
    except Exception as e:
        print("🚫 Token tidak valid:", e)
        return

    # Submit cerita
    for i in range(profile["story_quota"]):
        city = random.choice(cities)
        story = generate_story(city["location"])
        print(f"\n📝 Cerita {i+1}: {story}")
        submit_story(headers, city["id"], city["location"], story)

    # Submit struk
    print("\n🧾 Mulai upload struk...")
    submit_receipt(headers, profile["receipt_uploaded"])

# Main
def main():
    tokens = load_tokens("token.txt")
    if not tokens:
        print("🚫 Tidak ada token ditemukan.")
        return

    try:
        cities = get_cities()
    except Exception as e:
        print("💥 Gagal ambil daftar kota:", e)
        return

    for i, token in enumerate(tokens, 1):
        print(f"\n=== 🔁 Token {i}/{len(tokens)} ===")
        process_token(token, cities)

if __name__ == "__main__":
    main()

