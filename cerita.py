import requests
import random
import time

# Load semua token dari file
with open("token.txt", "r") as f:
    tokens = [line.strip() for line in f if line.strip()]

# Ambil semua ID cerita dengan pagination
def get_all_message_ids(token):
    headers = {"Authorization": f"Bearer {token}"}
    all_ids = []
    page = 1

    while True:
        url = f"https://coklatmerdeka.silverqueen.id/api/messages?page={page}"
        r = requests.get(url, headers=headers)

        try:
            data = r.json()
            items = data["data"]["data"]
            if not items:
                break  # Tidak ada data lagi
            all_ids.extend([msg["id"] for msg in items])
            page += 1
        except Exception as e:
            print(f"⚠️ Gagal parsing ID cerita di halaman {page}: {e}")
            break

    return all_ids

# Fungsi klaim cerita
def claim_story(token, story_id):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    url = f"https://coklatmerdeka.silverqueen.id/api/claim/{story_id}"
    r = requests.post(url, headers=headers)

    try:
        data = r.json()
        return data.get("message", "No message"), data.get("success", False)
    except:
        return "Error parsing response", False

# Loop semua akun (pemilik cerita)
for idx_owner, owner_token in enumerate(tokens):
    print(f"\n📥 Ambil SEMUA cerita dari Token {idx_owner+1}")
    message_ids = get_all_message_ids(owner_token)

    for story_id in message_ids:
        print(f"🪪 Cerita ID {story_id} → Cari token untuk klaim...")

        # Ambil daftar token selain pemilik
        claimers = [t for i, t in enumerate(tokens) if i != idx_owner]
        random.shuffle(claimers)

        claimed = False
        for idx_claimer, claimer_token in enumerate(claimers):
            msg, success = claim_story(claimer_token, story_id)
            status = "✅" if success else "❌"
            print(f"  {status} Token mencoba klaim → {msg}")
            time.sleep(1)

            if "already been claimed" in msg:
                print("⚠️ Cerita ini sudah diklaim, lanjut ke cerita berikutnya.")
                claimed = True
                break

            if success:
                claimed = True
                break  # langsung lanjut ke cerita berikutnya

        if not claimed:
            print("⚠️ Tidak ada token yang berhasil klaim cerita ini.")
