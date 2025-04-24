# KnowHow: Automatically Applying High-Level CTI Knowledge for Interpretable and Accurate Provenance Analysis

## Project Overview
KnowHow aims to develop a system for automatically using Cyber Threat Intelligence in the APT detection field, with the help of an innovative condensed representation—Generalized Indicators of Compromise (gIoC). At the same time, it is the first to automate the analysis and semantic summary of real attack behaviors contained in attack alerts based on commonly used attack abstraction models by security analysts in APT detections. This significantly reduces false positives while greatly enhancing the readability of attack alerts.

## Design Documentation

### Key Concept: Generalized Indicator of Compromise (gIoC)
- **gIoC** is an information triplet structure <subject, verb, object> used to represent attack knowledge in cyber threat intelligence.
  - **Subject**: An attack-related concept that could be specific IoCs, domain names, software names, etc.
  - **Verb**: The action performed by the subject.
  - **Object**: The target of the action performed by the subject.

### Step One: Extracting gIoC from Cyber Threat Intelligence
- Use our domain-optimized natural language extraction tools, `optimized_subject_verb_object_extaction`, to solve the proprietary challenges of CTI extraction and achieve full extraction of gIoC.

### Step Two: Detection Based on Embedding Alignment Strategy
- Perform semantic enhancement on system logs and compare them with semantically encoded CTI-extracted triplets to determine if there's a threat.

### Step Three: Alert Denoising and Presentation Based on Attack Lifecycle and LLMs
- Validate the validity of alerts based on the attack lifecycle and use LLMs to generate attack reports.

## Usage Documentation

### Method One: Directly Using Knowledge
1. Extract gIoC knowledge from cyber threat intelligence: `python gIoC_extraction.py`
2. Train/tag benign data: `python benigntag.py xxx`, `xxx` means the relative path of benign data
3. Detect anomaly data: `python techtag.py xxx`, `xxx` means the relative path of anomaly data
4. Build graph and event alerting: `python sysdig_graph_new2.py xxx xxx y`, `xxx` means the relative path of parsed data by step 4, `y` means the threshold
5. Generate alert lifecycle: `python lifecycle.py`

### Method Two: Using Embedding-Based Knowledge (CPU-based)
1. Extract gIoC knowledge: `python gIoC_extraction.py`
2. Embed knowledge: `python parse_technique_result.py; python embedding_model.py; python cal_tech_dic.py`
3. Train/tag benign data: `python benigntag_paral.py xxx`, `xxx` means the relative path of benign data
4. Detect anomaly data: `python techtag_paral.py xxx`, `xxx` means the relative path of anomaly data
5. Build graph and event alerting: `python sysdig_graph_new2.py xxx xxx y`, `xxx` means the relative path of parsed data by step 4, `y` means the threshold
6. Generate alert lifecycle: `python lifecylce.py`

### Method Three: Using Embedding-Based Knowledge (GPU-based)
1. Extract gIoC knowledge: `python gIoC_extraction.py`
2. Embed knowledge: `python parse_technique_result.py; python embedding_model.py; python cal_tech_dic.py`
3. Train/tag benign data: `python benigntag_paral_gpu.py xxx`, `xxx` means the relative path of benign data
4. Detect anomaly data: `python techtag_paral_gpu.py xxx`, `xxx` means the relative path of anomaly data
5. Build graph and event alerting: `python sysdig_graph_new2.py xxx xxx y`, `xxx` means the relative path of parsed data by step 4, `y` means the threshold
6. Generate alert lifecycle: `python lifecycle.py`


## Dataset Release
### NewlySim Dataset
We have utilized two new CVEs in NewlySim datasets for evaluation of KnowHow against 0-day vulnerability scenarios. In addition, we used a complex set of attack commands to expand the two vulnerabilities into two APT attacks. The datasets for the two APT attacks are released in the following link for facilitating further research: <https://pan.baidu.com/s/16xGnpQhaaWhJkDKQQqX1LA?pwd=1111>.

Specifically, attack1-host1/2.zip records APT attack data built based on CVE-2023-22809 vulnerability, while attack1-host1/2.zip records APT attack data built based on CVE-2024-28085 vulnerability. And the detailed attack commandlines used by the two APT attacks are recorded in the corresponding images (attack1.png,attack2.png).

### Mimic-Prov Dataset
To evaluate the robustness of KnowHow against mimicry attacks, we constructed a mimicry dataset, Mimic-Prov, following the steps outlined in ^[A. Goyal, X. Han, G. Wang, and A. Bates, “Sometimes, you aren’t what you do: Mimicry attacks against provenance graph host intrusion detection systems,” in 30th Network and Distributed System Security Symposium, 2023.].





