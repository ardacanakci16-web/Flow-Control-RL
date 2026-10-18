"""
Flow Control RL Environment & Dependencies Check
"""
import sys
import os

def check():
    print("=" * 60)
    print("FLOW CONTROL RL & HYDROGYM KURULUM VE ORTAM KONTROLU")
    print("=" * 60)
    print(f"Python Surumu: {sys.version.split()[0]} ({sys.executable})")

    packages = [
        ("numpy", "NumPy Sayisal Dizi ve Matris Hesaplamalari"),
        ("scipy", "SciPy Istatistik ve Numerik Yontemler"),
        ("matplotlib", "Matplotlib Vortisite ve Grafik Cizimi"),
        ("PIL", "Pillow Gorsel Isleme"),
    ]

    all_ok = True
    for pkg, desc in packages:
        try:
            __import__(pkg)
            print(f"[OK] {pkg:<15} - {desc}")
        except ImportError:
            print(f"[EKSIK] {pkg:<15} - {desc}")
            all_ok = False

    # Check local modules
    sys.path.insert(0, os.path.abspath("."))
    try:
        from src.flow_control import GaussianSensorNoiseWrapper, FluidicPinballEnvironment
        print(f"[OK] src.flow_control - Akis Kontrolu ve Sensor Gurultu Motoru")
    except Exception as e:
        print(f"[EKSIK] src.flow_control - {e}")
        all_ok = False

    print("=" * 60)
    if all_ok:
        print("TEBRIKLER: Flow-Control-RL bagimliliklari eksiksiz!")
        print("Analiz ve simülasyonu calistirmak icin: python scripts/run_simulation.py")
    else:
        print("Lutfen eksik paketleri 'pip install -r requirements.txt' ile yukleyin.")
    print("=" * 60)

if __name__ == "__main__":
    check()
