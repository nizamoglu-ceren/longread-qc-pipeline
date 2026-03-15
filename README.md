# Long-Read Sequencing QC Pipeline

Oxford Nanopore teknolojisiyle üretilmiş long-read dizileme verilerinin kalite kontrolü için geliştirilmiş bir analiz hattı.

## Hesaplanan Metrikler

Bu pipeline her read için üç temel metrik hesaplar:

| Metrik | Açıklama | 
|--------|----------|
| **Read Uzunluğu** | Okunan DNA parçasının baz çifti (bp) cinsinden uzunluğu 
| **GC İçeriği (%)** | DNA dizisindeki G ve C bazlarının yüzdesi 
| **Ortalama Kalite (Phred)** | Her bazın ne kadar güvenilir okunduğunun skoru. 

## Gereksinimler

- [Miniconda](https://docs.conda.io/en/latest/miniconda.html)
- Git
  
## Girdi Veri Formatı

Pipeline, long-read dizileme teknolojilerinden (örneğin Oxford Nanopore) üretilmiş FASTQ formatındaki ham dizileme verisini girdi olarak alır.

FASTQ dosyası dört satırlık kayıt yapısına sahiptir:

@read_id
ACTGACTGACTG
+
IIIIIIIIIIII

1. satır: read kimliği  
2. satır: DNA dizisi  
3. satır: ayırıcı satır  
4. satır: kalite skorları (Phred)

```bash
# 1. Repoyu bilgisayarına indir
git clone https://github.com/nizamoglu-ceren/longread-qc-pipeline.git
cd longread-qc-pipeline

# 2. Gerekli tüm araçları tek komutla kur
conda env create -f environment.yml

# 3. Ortamı aktive et
conda activate longreads
```

`environment.yml` dosyası projenin ihtiyaç duyduğu tüm araç ve kütüphaneleri tanımlar. 
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

Snakemake pipeline akışını görselleştirmek için:

snakemake --dag | dot -Tpng > workflow.png

## Pipeline Mimarisi
```
barcode77.fastq (Ham Veri)
        │
        ├──► [1] NanoPlot ──────────► results/nanoplot/NanoPlot-report.html
        │         (Otomatik QC raporu)
        │
        ├──► [2] analyze_reads.py ──► results/read_stats.csv
        │         (GC, uzunluk,           (Her read için istatistik tablosu)
        │          kalite hesaplama)
        │                │
        └────────────────►
                         │
                    [3] visualize.py ──► results/qc_plots.png
                    (Grafik üretimi)      (Dağılım grafikleri)
```

**Snakemake** bu adımları otomatik olarak sıraya koyar. 
---

## 📁 Dosya Yapısı
```
longread-qc-pipeline/
├── Snakefile              - Pipeline adımlarını tanımlar
├── config.yaml            - Girdi dosyası ayarları
├── environment.yml        - Conda ortam tanımı
├── analyze_reads.py       - GC, uzunluk, kalite hesaplama scripti
├── visualize.py           - Grafik üretim scripti
├── .gitignore             - Git'e yüklenmeyecek dosyalar
└── results/
    ├── read_stats.csv          - Her read için hesaplanan değerler
    ├── qc_plots.png            - Dağılım grafikleri 
    └── nanoplot/
        └── NanoPlot-report.html   - QC raporu
```

---

## Hesaplanan Metrikler

- **Read Uzunluğu**: Her readın baz çifti (bp) cinsinden uzunluğu
- **GC İçeriği**: G ve C bazlarının yüzdesi
- **Ortalama Kalite**: Phred kalite skoru (Q20)

---

## Barcode77 Sonuçları

| Metrik | Değer |
|--------|-------|
| Toplam Read | 81.011 |
| Medyan Uzunluk | 547 bp |
| Medyan GC | %53.5 |
| Medyan Kalite | Q17.3 |
| Q20+ Read Oranı | %41.2 |

---



## Profesör Kılıç'a Rapor

**Konu:** Barcode77 Nanopore Dizileme Verisi — Kalite Kontrol Raporu

Sayın Profesör Kılıç,

Göndermiş olduğunuz barcode77 dizileme verisinin kalite kontrolünü tamamladım. 

Ham veriyi (81.011 DNA okuması) bilgisayar ortamında otomatik olarak işleyen bir analiz hattı kurdum. Bu işlem; her okumanın uzunluğunu, GC baz içeriğini ve kalite skorunu hesaplayarak görsel raporlar üretti.

**Sonuçlar**

*Read Uzunluğu:* Okumaların yarısı 547 baz çiftinden uzun, bazı okumalar 686.000 baz çiftine kadar ulaşıyor. Bu, Nanopore teknolojisinin en büyük avantajı olan uzun okuma kapasitesini gösteriyor. Uzunluk dağılımı beklenen aralıkta ve normal görünüyor.

*GC İçeriği:* Ortalama %53.5 olarak hesaplandı. Bu değer normal kabul edilen %40–60 aralığında ve güzel bir çan eğrisi oluşturuyor. Örnekleme kalitesi açısından herhangi bir sorun gözlemlenmedi.

*Kalite Skorları:* Medyan kalite Q17.3 olarak ölçüldü. Okumaların %41.2'si yüksek kalite eşiği olan Q20'nin üzerinde. Kalite skoru dağılımında iki ayrı tepe görülmektedir — bu, cihazın bazı okumaları çok iyi, bazılarını ise daha düşük kalitede okuduğuna işaret ediyor.

**Öneri:**
Verinin genel kalitesi hizalama (alignment) işlemine geçmek için yeterlidir. Ancak daha temiz ve güvenilir sonuçlar için alignment öncesi şu filtrelemenin yapılmasını öneririm: Q20 altındaki okumaların ve 200 bp'den kısa okumaların veri setinden çıkarılması. Bu adım hizalama doğruluğunu önemli ölçüde artıracaktır. 

Sorularınız için her zaman ulaşabilirsiniz.

Saygılarımla,

Ceren Nizamoğlu

Bu pipeline tekrar üretilebilir olacak şekilde tasarlanmıştır.

Tüm bağımlılıklar `environment.yml` dosyasında tanımlanmıştır ve Conda kullanılarak tek komutla kurulabilir. Böylece farklı bilgisayarlarda aynı analiz ortamı oluşturulabilir.
