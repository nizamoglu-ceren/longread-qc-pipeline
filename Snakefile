configfile: "config.yaml"

rule all:
    input:
        "results/nanoplot/NanoPlot-report.html",
        "results/read_stats.csv",
        "results/qc_plots.png"

rule nanoplot_qc:
    input:
        fastq = config["fastq_input"]
    output:
        html = "results/nanoplot/NanoPlot-report.html"
    shell:
        """
        NanoPlot --fastq {input.fastq} \
                 --outdir results/nanoplot \
                 --plots hex dot \
                 --N50 \
                 --title "Barcode77 QC"
        """

rule analyze_reads:
    input:
        fastq = config["fastq_input"]
    output:
        csv = "results/read_stats.csv"
    shell:
        "python analyze_reads.py {input.fastq} {output.csv}"

rule visualize:
    input:
        csv = "results/read_stats.csv"
    output:
        png = "results/qc_plots.png"
    shell:
        "python visualize.py {input.csv} {output.png}"
