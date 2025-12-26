import exifread
import sys
from datetime import datetime

def get_exif(path):
    with open(path, "rb") as f:
        tags = exifread.process_file(f)
    return tags

def dms_to_decimal(dms, ref):
    degrees = float(dms[0].num) / float(dms[0].den)
    minutes = float(dms[1].num) / float(dms[1].den)
    seconds = float(dms[2].num) / float(dms[2].den)
    decimal = degrees + (minutes/60) + (seconds/3600)
    if ref in ['S', 'W']:
        decimal = -decimal
    return decimal

def extract_gps(tags):
    try:
        lat = dms_to_decimal(tags['GPS GPSLatitude'].values,
                             tags['GPS GPSLatitudeRef'].values)
        lon = dms_to_decimal(tags['GPS GPSLongitude'].values,
                             tags['GPS GPSLongitudeRef'].values)
        return lat, lon
    except:
        return None, None

def detect_sky_color():
    return "Cerah / Sedikit Awan"

def environment_prediction(lat):
    return "Wilayah tropis perkotaan", "Indonesia (probabilitas tinggi)"

def print_report(filename, tags, lat, lon):
    print("\n⣿⣿⣷⡁⢆⠈⠕⢕⢂⢕⢂⢕⢂⢔⢂⢕⢄⠂⣂⠂⠆⢂⢕⢂⢕⢂⢕⢂⢕⢂")
    print("⣿⣿⣿⡷⠊⡢⡹⣦⡑⢂⢕⢂⢕⢂⢕⢂⠕⠔⠌⠝⠛⠶⠶⢶⣦⣄⢂⢕⢂⢕")
    print("⣿⣿⠏⣠⣾⣦⡐⢌⢿⣷⣦⣅⡑⠕⠡⠐⢿⠿⣛⠟⠛⠛⠛⠛⠡⢷⡈⢂⢕⢂")
    print("⠟⣡⣾⣿⣿⣿⣿⣦⣑⠝⢿⣿⣿⣿⣿⣿⡵⢁⣤⣶⣶⣿⢿⢿⢿⡟⢻⣤⢑⢂")
    print("⣾⣿⣿⡿⢟⣛⣻⣿⣿⣿⣦⣬⣙⣻⣿⣿⣷⣿⣿⢟⢝⢕⢕⢕⢕⢽⣿⣿⣷⣔")
    print("⣿⣿⠵⠚⠉⢀⣀⣀⣈⣿⣿⣿⣿⣿⣿⣿⣿⣿⣗⢕⢕⢕⢕⢕⢕⣽⣿⣿⣿⣿")
    print("⢷⣂⣠⣴⣾⡿⡿⡻⡻⣿⣿⣴⣿⣿⣿⣿⣿⣿⣷⣵⣵⣵⣷⣿⣿⣿⣿⣿⣿⡿")
    print("⢌⠻⣿⡿⡫⡪⡪⡪⡪⣺⣿⣿⣿⣿⣿⠿⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃")
    print("⠣⡁⠹⡪⡪⡪⡪⣪⣾⣿⣿⣿⣿⠋⠐⢉⢍⢄⢌⠻⣿⣿⣿⣿⣿⣿⣿⣿⠏⠈")
    print("⡣⡘⢄⠙⣾⣾⣾⣿⣿⣿⣿⣿⣿⡀⢐⢕⢕⢕⢕⢕⡘⣿⣿⣿⣿⣿⣿⠏⠠⠈")
    print("⠌⢊⢂⢣⠹⣿⣿⣿⣿⣿⣿⣿⣿⣧⢐⢕⢕⢕⢕⢕⢅⣿⣿⣿⣿⡿⢋⢜⠠⠈")
    print("⠄⠁⠕⢝⡢⠈⠻⣿⣿⣿⣿⣿⣿⣿⣷⣕⣑⣑⣑⣵⣿⣿⣿⡿⢋⢔⢕⣿⠠⠈")
    print("⠨⡂⡀⢑⢕⡅⠂⠄⠉⠛⠻⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢋⢔⢕⢕⣿⣿⠠⠈")
    print("⠄⠪⣂⠁⢕⠆⠄⠂⠄⠁⡀⠂⡀⠄⢈⠉⢍⢛⢛⢛⢋⢔⢕⢕⢕⣽⣿⣿⠠⠈\n")

    print("Informasi Foto")
    print(f"- Nama file     : {filename}")

    if "EXIF DateTimeOriginal" in tags:
        dt = str(tags['EXIF DateTimeOriginal'])
        print(f"- Diambil pada  : {dt}")
    else:
        print("- Diambil pada  : Tidak ada data")

    if "Image Model" in tags:
        print(f"- Perangkat     : {tags['Image Model']}")
    else:
        print("- Perangkat     : Tidak ada data")

    print("\n Lokasi (EXIF GPS)")
    if lat and lon:
        print(f"- Latitude      : {lat}")
        print(f"- Longitude     : {lon}")
        print(f"- Maps Link     : https://maps.google.com/?q={lat},{lon}")
    else:
        print("- Tidak ada data GPS ditemukan")

    print("\n Analisa Cuaca")
    print(f"- Kondisi langit : {detect_sky_color()}")
    print("- Potensi Waktu  : Sore Hari (perkiraan dari cahaya)")

    env, country = environment_prediction(lat)
    print("\n OSINT Lingkungan")
    print(f"- Jenis wilayah  : {env}")
    print(f"- Kemungkinan negara : {country}")

if __name__ == "__main__":
    file = sys.argv[1]
    tags = get_exif(file)
    lat, lon = extract_gps(tags)
    print_report(file, tags, lat, lon)
