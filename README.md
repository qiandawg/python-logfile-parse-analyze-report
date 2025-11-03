PerfTraceAnalyzer: Server Performance Log Analyzer

A Python tool to parse server performance trace logs, calculate key architectural metrics, and generate a summary report.

This project was built to demonstrate proficiency in file parsing, data aggregation, and statistical reporting with Python, specifically for system architecture and performance analysis use cases.

The "Why"

In system architecture and performance debugging, engineers work with trace logs that can be billions of lines long. Manually inspecting them is impossible.

This tool simulates the real-world task of an architect: quickly writing a script to parse a massive log file and extract high-level, actionable insights to identify performance bottlenecks.

Features

File Parsing: Reads and parses a structured, line-by-line log file.

Data Aggregation: Uses dictionaries to efficiently count and categorize millions of events.

Metrics Calculation: Computes key performance indicators (KPIs) crucial for a server architect:

Cache Hit Rate

TLB (Translation Lookaside Buffer) Hit Rate

Average Main Memory (DRAM) Access Latency

How to Run

This script is designed to be run from the command line and accepts a log file as an argument.

1. Project Structure

Your folder should look like this:

PerfTraceAnalyzer/
│
├── analyze_trace.py    # The main Python script
├── epyc_trace.log      # The sample log file
└── README.md           # This file


2. Sample Log File (epyc_trace.log)

The included sample log (epyc_trace.log) uses a simple ::-delimited format:

TIMESTAMP::EVENT_TYPE::DETAILS
...
1001::CACHE_ACCESS::core=0,addr=0x1A00,status=HIT
1004::CACHE_ACCESS::core=2,addr=0x3C00,status=MISS
1005::MEM_READ::addr=0x3C00,latency_ns=85
1014::TLB_LOOKUP::core=1,addr=0x8F00,status=MISS
...


3. Running the Analysis

From your terminal, navigate to the project folder and run the script, passing the log file as an argument:

python analyze_trace.py epyc_trace.log


If you do not provide an argument, the script will default to looking for epyc_trace.log in the same directory.

4. Sample Report Output

The script will process the file and print a final report to the console:

--- Starting analysis of epyc_trace.log ---

--- 📈 Performance Analysis Report ---

## Cache Performance
  Total Accesses: 10
  Cache Hits:     7
  Cache Misses:   3
  Cache Hit Rate: 70.00%

## TLB Performance
  Total Lookups: 3
  TLB Hits:      2
  TLB Misses:    1
  TLB Hit Rate:  66.67%

## Memory Subsystem
  Total DRAM Reads:  3
  Average Latency: 99.00 ns


Analysis of this Report: This output immediately shows a poor Cache Hit Rate (70%) and a critical TLB Hit Rate (66.67%), pointing to a potential bottleneck in address translation or memory access patterns.