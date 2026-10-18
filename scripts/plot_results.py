"""
Flow Control RL Results Plots Verifier
Verifies plots/sonuc_1, plots/sonuc_2, and plots/sonuc_3.
"""
import os

def check_plots():
    plots = [
        "plots/sonuc_1_sifir_atik_gurultu_aktarimi.png",
        "plots/sonuc_2_esit_butce_ogrenme_egrileri.png",
        "plots/sonuc_3_senaryolar_arasi_kiyaslama.png"
    ]
    for p in plots:
        if os.path.exists(p):
            print(f"[OK] Grafik hazir: {p} ({os.path.getsize(p)/1024:.1f} KB)")
        else:
            print(f"[EKSIK] Grafik bulunamadi: {p}")

if __name__ == "__main__":
    check_plots()
