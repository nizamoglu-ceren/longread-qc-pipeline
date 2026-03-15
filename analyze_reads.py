import sys
import csv
import gzip
import os

def parse_quality(qual_str):
    """Kalite string'ini Phred skoruna çevir"""
    return [ord(c) - 33 for c in qual_str]

def mean_quality(qual_str):
    """Ortalama kalite skoru hesapla"""
    scores = parse_quality(qual_str)
    return sum(scores) / len(scores) if scores else 0

def gc_content(seq):
    """GC içeriği yüzdesi hesapla"""
    seq = seq.upper()
    gc = seq.count('G') + seq.count('C')
    return (gc / len(seq) * 100) if len(seq) > 0 else 0

def read_fastq(filepath):
    """FASTQ dosyasını oku, her read için (header, seq, qual) döndür"""
    opener = gzip.open if filepath.endswith('.gz') else open
    with opener(filepath, 'rt') as f:
        while True:
            header = f.readline().strip()
            if not header:
                break
            seq    = f.readline().strip()
            plus   = f.readline().strip()
            qual   = f.readline().strip()
            yield header, seq, qual

def main():
    if len(sys.argv) < 3:
        print("Kullanim: python analyze_reads.py input.fastq output.csv")
        sys.exit(1)

    input_file  = sys.argv[1]
    output_file = sys.argv[2]

    print(f"Dosya okunuyor: {input_file}")

    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['read_id', 'read_length', 'gc_content', 'mean_quality'])

        for i, (header, seq, qual) in enumerate(read_fastq(input_file)):
            read_id     = header.split()[0].lstrip('@')
            length      = len(seq)
            gc          = round(gc_content(seq), 2)
            mean_qual   = round(mean_quality(qual), 2)
            writer.writerow([read_id, length, gc, mean_qual])

            if (i + 1) % 10000 == 0:
                print(f"  {i+1} read islendi...")

    print(f"Tamamlandi! Sonuclar: {output_file}")

if __name__ == "__main__":
    main()
