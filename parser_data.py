import os
import time
import re
import requests
from urllib.parse import urljoin

datas_ver_gverdis_linki = "http://cidas.isee.nagoya-u.ac.jp/WDCCR/files/STATIONS/TBILIS/SHORTFORMAT/"
OUT_DIR = "TBILIS_SHORTFORMAT"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (research data download; contact: your_email@example.com)"
}


def txt_failis_wamogeba(sesia):
    resp = sesia.get(datas_ver_gverdis_linki, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    failis_saxeli = re.findall(r'href="([^"]+\.txt)"', resp.text, flags=re.IGNORECASE)
    failis_saxeli = [os.path.basename(f) for f in failis_saxeli]
    return sorted(set(failis_saxeli))


def failis_chamotvirtva(sesia, failis_saxeli, retries=3):
    url = urljoin(datas_ver_gverdis_linki, failis_saxeli)
    out_path = os.path.join(OUT_DIR, failis_saxeli)

    for i in range(1, retries + 1):
        try:
            resp = sesia.get(url, headers=HEADERS, timeout=60)
            resp.raise_for_status()
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(resp.text)
            print(f"[OK] {failis_saxeli}  ({len(resp.text)} bytes)")
            return True
        except requests.RequestException as e:
            print(f"[{i}/{retries}] shecdoma {failis_saxeli}: {e}")
            time.sleep(2 * i)
    print(f"[dafeilda] {failis_saxeli} — ver chamoitvirta")
    return False


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    sesia = requests.Session()

    failis_saxeli = txt_failis_wamogeba(sesia)
    print(f"napovnia {len(failis_saxeli)} txt faili\n")

    dafeilebuli = []
    for j in failis_saxeli:
        ok = failis_chamotvirtva(sesia, j)
        if not ok:
            dafeilebuli.append(j)
        time.sleep(0.5)  

    print("\ndasrulda")
    print(f"srulad chamoitvirta: {len(failis_saxeli) - len(dafeilebuli)} / {len(failis_saxeli)}")
    if dafeilebuli:
        print("ver chamoitvirta:", dafeilebuli)


if __name__ == "__main__":
    main()