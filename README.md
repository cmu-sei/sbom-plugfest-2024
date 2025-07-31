# sbom-plugfest-2024
The repository for SBOMs and code which can be shared from the 2024 SBOM Plugfest organized by the SEI on behalf of CISA.

SBOMs are provided as the SEI received them, with a few caveats:
- SBOMs are intended for informational use only.
- Where requested, we have anonymized the supplier of the SBOMs to the degree requested.
- When possible, we have provided readme files which accompanied SBOMs provided to us.

We have additionally made available some jupyter notebooks which we used to produce the data analyzed as part of this project. There are a few primary code files:

*cyclonedx_analyzer.ipynb*: the primary file used to produce data from sboms in the cyclonedx format.
*spdx_analyzer.ipynb*: the primary file used to produce data from sboms in the spdx format.
*shared_functions*: a separate file hosting a number of functions needed for processing SBOMs. Our intention was to migrate many functions in notebooks into separate python files and to convert notebooks into python scripts. Note: shared_functions.py should be co-located with the cyclonedx and spdx notebooks.

## Important: because some participants have chosen to redact their SBOMs or to not allow a public release of their SBOMs, we note that the data/results produced using this code and using the publicly releasable SBOMs may not match data released as part of the summarizing report for the 2024 Plugfest. 

## Recommended Directory Structure   
This directory structure was used to facilitate processing of .json sboms of each type (CycloneDX, SPDX). There are other more efficient ways to do this, but this is the methodology we used. As written, these notebooks should be run from the ```code``` location. Additionally, although only two targets are illustrated here, this structure should be replicated for sboms corresponding to additional targets.
```
📂project
┣ 📂code
┃ ┣ 📜cyclonedx_analyzer.ipynb
┃ ┣ 📜shared_functions.py
┃ ┗ 📜spdx_analyzer.ipynb
┣ 📂outputs
┣ 📂submissions_by_target
┃ ┣ 📂target_1
┃ ┃ ┣ 📂build
┃ ┃ ┃ ┣ 📂cyclone
┃ ┃ ┃ ┃ ┗ 📜cdx_build_target_2_sbom_1.json
┃ ┃ ┃ ┗ 📂spdx
┃ ┃ ┃   ┗ 📜spdx_build_target_2_sbom_1.json
┃ ┃ ┗ 📂source
┃ ┃   ┣ 📂cyclone
┃ ┃   ┃ ┗ 📜cdx_source_target_2_sbom_1.json
┃ ┃   ┗ 📂spdx
┃ ┃     ┗ 📜spdx_source_target_2_sbom_1.json
┃ ┗ 📂target_2
┃   ┣ 📂build
┃   ┃ ┣ 📂cyclone
┃   ┃ ┃ ┗ 📜cdx_build_target_2_sbom_1.json
┃   ┃ ┗ 📂spdx
┃   ┃   ┗ 📜spdx_build_target_2_sbom_1.json
┃   ┗ 📂source
┃     ┣ 📂cyclone
┃     ┃ ┗ 📜cdx_source_target_2_sbom_1.json
┃     ┗ 📂spdx
┃       ┗ 📜spdx_source_target_2_sbom_1.json
┗ 📂baseline_sboms
     ┣ 📂target_1
     ┃ ┗ 📜target_1_baseline_sbom_1.json
     ┗ 📂target_2
       ┗ 📜target_2_baseline_sbom_1.json
```

## Outputs

After running all cells in the cyclonedx notebook, you will produce:
- ```(bld/src)_comp_version_(target).csv```: files that summarize how many CycloneDX SBOMs of type (target; source or build) each (component, version) was found in. There will be one of these files produced for each phase (build/source) for each target.

- ```merged_cycloneDX_component_files.csv```: a file that combines all of the data from component version files (see previous bullet).

- ```(bld/src)_full_combined_(target).csv```: files that summarize information extracted from each component of all build/source sboms for each target. One file is produced for each phase (build/source) for each target. 

- ```(bld/src)_(target)_cyclonedx_summary.csv```: files that summarize top-level information about each sbom (primarily, minimum elements). There will be one of these files produced for each phase (build/source) for each target.

- ```merged_cycloneDX_summary_files.csv```: a file that combines all of the data from individual summary files (see previous bullet).


After we produced data for the SBOMs in CycloneDX format, for the purposes of the 2024 Plugfest, we decided to only produce merged files from which we did the remainder of the analysis on the (1) SBOM metadata and (2) high-level component data. Data on individual components within SPDX SBOMs was not extracted in support of the 2024 Plugfest, but can be through repurposing other code or writing code from scratch.

After running all cells, you will produce:
- ```merged_spdx_component_files.csv```: file that combines all data which summarizes how many SPDX SBOMs of type (target; source or build) each (component, version) was found in. There will be data for SBOMs of each phase for each target, but this was simply merged together and exported.

- ```merged_spdx_summary_files.csv```: a file that combines summarizing top-level information about each sbom (primarily, minimum elements). There will be data for SBOMs of each phase for each target, but this was simply merged together and exported.

# License Information:

2024 SBOM Plugfest Code Release

Copyright 2025 Carnegie Mellon University.

Licensed under a MIT (SEI)-style license, please see license.txt or contact permission@sei.cmu.edu for full terms.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

2024 SBOM Plugfest Code Release includes and/or can make use of certain third party software ("Third Party Software"). The Third Party Software that is used by 2024 SBOM Plugfest Code Release is dependent upon your system configuration, but typically includes the software identified in this license.txt file, and/or described in the documentation and/or read me file. By using 2024 SBOM Plugfest Code Release, you agree to comply with any and all relevant Third Party Software terms and conditions contained in any such Third Party Software or separate license file distributed with such Third Party Software. The parties who own the Third Party Software ("Third Party Licensors") are intended third party beneficiaries to this License with respect to the terms applicable to their Third Party Software. Third Party Software licenses only apply to the Third Party Software and not any other portion of 2024 SBOM Plugfest Code Release or 2024 SBOM Plugfest Code Release as a whole.

This material is based upon work funded and supported by the Department of Homeland Security under Contract No. FA8702-15-D-0002 with Carnegie Mellon University for the operation of the Software Engineering Institute, a federally funded research and development center sponsored by the United States Department of Defense.  

The view, opinions, and/or findings contained in this material are those of the author(s) and should not be construed as an official Government position, policy, or decision, unless designated by other documentation.

NO WARRANTY. THIS CARNEGIE MELLON UNIVERSITY AND SOFTWARE ENGINEERING INSTITUTE MATERIAL IS FURNISHED ON AN "AS-IS" BASIS. CARNEGIE MELLON UNIVERSITY MAKES NO WARRANTIES OF ANY KIND, EITHER EXPRESSED OR IMPLIED, AS TO ANY MATTER INCLUDING, BUT NOT LIMITED TO, WARRANTY OF FITNESS FOR PURPOSE OR MERCHANTABILITY, EXCLUSIVITY, OR RESULTS OBTAINED FROM USE OF THE MATERIAL. CARNEGIE MELLON UNIVERSITY DOES NOT MAKE ANY WARRANTY OF ANY KIND WITH RESPECT TO FREEDOM FROM PATENT, TRADEMARK, OR COPYRIGHT INFRINGEMENT.

[DISTRIBUTION STATEMENT A] This material has been approved for public release and unlimited distribution.  Please see Copyright notice for non-US Government use and distribution.


This Software includes and/or makes use of Third-Party Software each subject to its own license, including but not limited to the following:

     1. Python (https://docs.python.org/3/license.html) Copyright 2024 Python Software Foundation. 

DM25-0931
