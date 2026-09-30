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

NanoPlot is a long-read specific QC tool. It was run on the raw FASTQ file to get 
an initial sense of the data — how long the reads are, how the quality is distributed, 
and whether anything looks off before going further.

Output: `results/nanoplot/`

### Step 2: Per-Read Statistical Analysis

`analyze_reads.py` iterates over every read in the FASTQ file and computes three values: 
read length, GC content, and mean Phred quality score. The results are written to a CSV file.

Output: `results/read_stats.csv`

### Step 3: Visualization

`visualize.py` loads the CSV and plots the distribution of each metric as a histogram. 
Key summary statistics are printed to the terminal at the same time.

Output: `results/qc_plots.png`

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

## What the Results Show

The three panels in `results/qc_plots.png` each tell a different part of the story.

The read length distribution (left panel) is plotted on a log scale because a small number 
of reads reach up to 686,000 bp — on a linear scale, everything else would be invisible. 
Most reads cluster between a few hundred and a few thousand base pairs, which is typical 
for this type of data.

The GC content (middle panel) sits around 53.5% and follows a clean bell curve. 
This is well within the normal range and suggests there are no obvious issues with 
sample quality or contamination.

The quality score distribution (right panel) has two peaks rather than one. This means 
the dataset contains a mix of high and low quality reads. The Q20 threshold is marked 
on the plot — reads to the right of that line are generally considered reliable enough 
for downstream analysis.

---

## Reproducibility

The environment is defined in `environment.yml` and can be set up with a single Conda command. 
The workflow steps are managed by Snakemake through the `Snakefile`, so there is no manual 
intervention required. The pipeline runs from start to finish automatically.

---



