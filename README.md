# Bioinformatics Pipeline for Long-Read Quality Control

This repository contains a quality control pipeline for Oxford Nanopore long-read sequencing data. 
The workflow takes a raw FASTQ file as input, calculates per-read statistics, and produces 
visualizations and a summary report — all before proceeding to any downstream analysis.

The pipeline was built using Snakemake for workflow management and custom Python scripts 
for statistical analysis and visualization.

---

## Project Goal

Before running any downstream analysis such as alignment, it is important to understand 
the quality of the raw sequencing data. This pipeline was built to evaluate the read length 
distribution, GC content, and mean quality scores of the dataset. Based on these metrics, 
it becomes possible to decide whether the data is ready for alignment or whether additional 
filtering steps are needed first.

---

## Biological Background

DNA sequencing is the process of reading the genetic code of an organism. The result is millions of DNA fragments called **reads**, stored in raw form in a **FASTQ** file.

**What is a FASTQ file?**
Each read is represented by 4 lines:
```text
@read_id        → read name
ACTGACTG...     → DNA sequence
+               → separator
IIIIIIII...     → quality scores (Phred)
```

**What is long-read sequencing?**
Classical technologies (e.g. Illumina) produce reads of 150–300 base pairs. Oxford Nanopore technology can produce reads of thousands to hundreds of thousands of base pairs. This allows more accurate analysis of complex genomic regions.

**Why Quality Control?**
Raw sequencing data is not always perfect. Before proceeding to alignment or other downstream analyses, it is critical to assess the quality of the data. Including low-quality reads in the analysis can lead to misleading results.

---

## Metrics Calculated

This pipeline calculates three key metrics for each individual read:

| Metric | Description | Expected Range |
|--------|-------------|----------------|
| **Read Length** | Length of the DNA fragment in base pairs (bp) | 500–50,000 bp typical for Nanopore |
| **GC Content (%)** | Percentage of G and C bases in the sequence | 40–60% considered normal |
| **Mean Quality (Phred)** | Reliability score of each base call. Q20 = 99% accuracy, Q30 = 99.9% accuracy | Q15+ acceptable, Q20+ good |

---

## Requirements

- [Miniconda](https://docs.conda.io/en/latest/miniconda.html) or Anaconda
- Git
- Linux / WSL2 (for Windows users)

---

## Installation
```bash
# 1. Clone the repository
git clone https://github.com/nizamoglu-ceren/longread-qc-pipeline.git
cd longread-qc-pipeline

# 2. Create the Conda environment
conda env create -f environment.yml

# 3. Activate the environment
conda activate longreads
```

The `environment.yml` file defines all required tools and libraries. This ensures the pipeline runs identically on any machine — **reproducibility**.

---

## Usage

1. Place your FASTQ file in the project folder
2. Update the filename in `config.yaml`:
```yaml
fastq_input: "your_file.fastq"
```
3. Run the pipeline:
```bash
snakemake --cores 2
```

Snakemake automatically runs all steps in order. You can follow the progress in the terminal.

---

## Pipeline Architecture
```
barcode77.fastq (Raw Input)
        │
        ├──► [1] NanoPlot
        │         │
        │         └──► results/nanoplot/NanoPlot-report.html
        │               (Automated QC report)
        │
        ├──► [2] analyze_reads.py
        │         │
        │         └──► results/read_stats.csv
        │               (Per-read statistics table)
        │
        └──► [3] visualize.py
                  │
                  └──► results/qc_plots.png
                        (Distribution plots)
```

---

## Pipeline Steps 

### Step 1: Quality Control with NanoPlot

The first step runs NanoPlot, a tool specifically designed for long-read sequencing data. 
Rather than writing everything from scratch, NanoPlot provides a quick and reliable overview 
of the dataset — including read length histograms, quality score plots, and summary statistics — 
all in an interactive HTML report.

Output is stored in: `results/nanoplot/`

### Step 2: Per-Read Statistical Analysis

While NanoPlot gives a general overview, we also wanted full control over the calculations. 
A custom Python script (`analyze_reads.py`) goes through each read in the FASTQ file one by one 
and calculates three metrics: GC content percentage, read length, and mean quality score. 
The results are saved in a structured table for further use.

Output is saved in: `results/read_stats.csv`  

### Step 3: Visualization

A separate script (`visualize.py`) takes the CSV file produced in Step 2 and generates 
distribution plots for all three metrics. Summary statistics including mean, median, 
minimum, and maximum are also calculated and printed to the terminal.

Output is saved in: `results/qc_plots.png`

---

## File Structure
```
longread-qc-pipeline/
├── Snakefile              - Defines pipeline steps
├── config.yaml            - Input file settings
├── environment.yml        - Conda environment definition
├── analyze_reads.py       - Per-read statistics script
├── visualize.py           - Visualization script
├── .gitignore             - Files excluded from Git
└── results/
    ├── read_stats.csv          - Per-read calculated values
    ├── qc_plots.png            - Distribution plots
    └── nanoplot/
        └── NanoPlot-report.html   - Interactive QC report
```

---

## Barcode77 Results

| Metric | Value | Comment |
|--------|-------|---------|
| Total Reads | 81,011 | Sufficient sequencing depth |
| Median Read Length | 547 bp | Typical Nanopore distribution |
| Maximum Read Length | 686,155 bp | Ultra-long reads present |
| Median GC Content | 53.5% | Within normal range ✅ |
| Median Quality Score | Q17.3 | Acceptable |
| Q20+ Read Rate | 41.2% | Filtering recommended |

---

## Interpretation of Results

**Read Length Distribution** (`results/qc_plots.png`, left panel):
The majority of reads fall between 200–5,000 bp. Some reads exceed 100,000 bp — this is a natural characteristic of Nanopore technology. Log scale is used to prevent extreme outliers from distorting the visualization.

**GC Content Distribution** (`results/qc_plots.png`, middle panel):
A normal bell curve centered around 53.5%, well within the expected 40–60% range. No contamination or unusual base composition detected.

**Quality Score Distribution** (`results/qc_plots.png`, right panel):
A bimodal distribution is observed — two peaks suggest the presence of both low-quality and high-quality read groups. The orange dashed line marks the Q20 threshold.

---

## Reproducibility

The environment is defined in `environment.yml` and can be set up with a single Conda command. 
The workflow steps are managed by Snakemake through the `Snakefile`, so there is no manual 
intervention required. The pipeline runs from start to finish automatically.

---

## Email to Professor Kılıç

**Subject:** Barcode77 Nanopore Sequencing Data — Quality Control Report

Dear Professor Kılıç,

I have completed the quality control analysis of the barcode77 sequencing data you provided. I have tried to summarize the findings in non-technical terms.

**What I Did:**
I built an automated analysis pipeline that processed the raw data (81,011 DNA reads). The pipeline calculated the length, GC base content, and quality score of each read and produced visual reports.

**What the Results Mean:**

Read Length: Half of the reads are longer than 547 base pairs, with some reads reaching up to 686,000 base pairs. This demonstrates the long-read capability of Nanopore technology. The length distribution is within the expected range and appears normal.

GC Content: The average GC content was calculated as 53.5%, which falls within the normal range of 40–60% and forms a clean bell curve. No issues were observed in terms of sample quality.

Quality Scores: The median quality score was measured as Q17.3. 41.2% of reads exceed the high-quality threshold of Q20. A bimodal distribution is observed in the quality scores — this indicates that the device read some fragments very accurately and others at lower quality.

**Recommendation:**
The overall quality of the data is sufficient to proceed to alignment. However, for cleaner and more reliable results, I recommend filtering out reads below Q20 and reads shorter than 200 bp before alignment. This step will improve alignment accuracy and reduce false mappings. Would you like me to perform this filtering step as well?

Please feel free to reach out if you have any questions.

Kind regards,
Ceren Nizamoğlu

---


