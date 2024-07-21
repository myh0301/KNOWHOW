# KNOWHOW
A Interpretable and Accurate APT Attack Detection Approach Based on CTI-Knowledge-Driven Provenance Analysis

## Code Descrpition
### optimized_subject_verb_object_extraction.py
The optimized svo extractor according to the method from our submission which is in Section 5.3. You can run this script to generated the information in the type of AMID needed from the open-source CTI.

### alert_generate.py
This script is to generate the event-level alert with the knowledge in AMID, bulid the attack graph and reasoning the attack life cycles just like Section 6 describes. You can run this script with the AMID information to detect the event level alert.

###  parse.py
This script is the optimized version of ''alert_generation.py'' with the speed-up optimized methods mentioned in Section 5.2. You can run this script to get the event-level alert with higher speed.

### sysdig_graph_benign.py & sysdig_graph_detect.py
These two scripts are to transform the detection result into graph. And the benign one is also the get the Grubbs’ Test in the benign data according to Section 6.1 & 6.2. It is worth mentioning that KNOWHOW also supports other data sources, such as ETW and FreeBSD, as was done in our experiments. In order to improve the reading experience, we do not include these similar pre-parsing code together, but use the parsing of the sysdig data source as an example.

### chainsummary.py
This script is to generate the attack life cycle according to the result from ''alert_generate.py'', which is the final result of KNOWHOW.



