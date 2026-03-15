# Long-Read Sequencing QC Pipeline

Oxford Nanopore uzun okuma verileri için kalite kontrol pipeline'ı.

## Gereksinimler

- [Miniconda](https://docs.conda.io/en/latest/miniconda.html)
- Git

## Kurulum
```bash
git clone https://github.com/KULLANICI_ADIN/longread_qc.git
cd longread_qc
conda env create -f environment.yml
conda activate longreads
```

## Kullanım

1. FASTQ dosyanı proje klasörüne koy
2. `config.yaml` içinde dosya adını güncelle:
```yaml
fastq_input: "senin_dosyan.fastq"
```
3. Pipeline'ı çalıştır:
```bash
snakemake --cores 2
```

## Pipeline Adımları

| Adım | Araç | Çıktı |
|------|------|-------|
| QC Raporu | NanoPlot | `results/nanoplot/NanoPlot-report.html` |
| Read İstatistikleri | Python (analyze_reads.py) | `results/read_stats.csv` |
| Görselleştirme | Python (visualize.py) | `results/qc_plots.png` |

## Hesaplanan Metrikler

- **Read Uzunluğu**: Her readın baz çifti (bp) cinsinden uzunluğu
- **GC İçeriği**: G ve C bazlarının yüzdesi
- **Ortalama Kalite**: Phred kalite skoru (Q20 = %99 doğruluk)

## Barcode77 Sonuçları

| Metrik | Değer |
|--------|-------|
| Toplam Read | 81.011 |
| Medyan Uzunluk | 547 bp |
| Medyan GC | %53.5 |
| Medyan Kalite | Q17.3 |
| Q20+ Read Oranı | %41.2 |

---

## Profesör Kılıç'a E-posta

**Konu:** Barcode77 Nanopore Dizileme Verisi — Kalite Kontrol Raporu

Sayın Profesör Kılıç,

Göndermiş olduğunuz barcode77 dizileme verisinin kalite kontrolünü tamamladım. Bulgularımı teknik olmayan bir dille özetlemeye çalıştım.

**Ne Yaptım?**
Ham veriyi (81.011 DNA okuması) bilgisayar ortamında otomatik olarak işleyen bir analiz hattı kurdum. Bu hat; her okumanın uzunluğunu, GC baz içeriğini ve kalite skorunu hesaplayarak görsel raporlar üretti.

**Sonuçlar Ne Anlama Geliyor?**

*Read Uzunluğu:* Okumaların yarısı 547 baz çiftinden uzun. Bazı okumalar 686.000 baz çiftine kadar ulaşıyor — bu, Nanopore teknolojisinin en büyük avantajı olan uzun okuma kapasitesini gösteriyor. Uzunluk dağılımı beklenen aralıkta.

*GC İçeriği:* Ortalama %53.5 olarak hesaplandı. Bu değer normal kabul edilen %40-60 aralığında ve güzel bir çan eğrisi oluşturuyor. Örnekleme kalitesi açısından sorun yok.

*Kalite Skorları:* Medyan kalite Q17.3 olarak ölçüldü. Okumaların %41.2'si yüksek kalite eşiği olan Q20'nin üzerinde. Nanopore verileri için kabul edilebilir bir kalite olmakla birlikte, alignment öncesi düşük kaliteli okumaların filtrelenmesini öneririm.

**Öneri:**
Verinin genel kalitesi hizalama (alignment) işlemine geçmek için yeterlidir. Ancak daha temiz sonuçlar için önce Q20 altındaki okumaları ve 200 bp'den kısa okumaları filtrelemek, hizalama doğruluğunu artıracaktır. Bu filtreleme adımını da gerçekleştirmemi ister misiniz?

Sorularınız için her zaman ulaşabilirsiniz.

Saygılarımla,
Ceren Nizamoğlu
