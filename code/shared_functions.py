###
# License:
#
# 2024 SBOM Plugfest Code Release
#
# Copyright 2025 Carnegie Mellon University.
#
# NO WARRANTY. THIS CARNEGIE MELLON UNIVERSITY AND SOFTWARE ENGINEERING INSTITUTE MATERIAL IS FURNISHED ON AN "AS-IS" BASIS. CARNEGIE MELLON UNIVERSITY MAKES NO WARRANTIES OF ANY KIND, EITHER EXPRESSED OR IMPLIED, AS TO ANY MATTER INCLUDING, BUT NOT LIMITED TO, WARRANTY OF FITNESS FOR PURPOSE OR
# MERCHANTABILITY, EXCLUSIVITY, OR RESULTS OBTAINED FROM USE OF THE MATERIAL. CARNEGIE MELLON UNIVERSITY DOES NOT MAKE ANY WARRANTY OF ANY KIND WITH RESPECT TO FREEDOM FROM PATENT, TRADEMARK, OR COPYRIGHT INFRINGEMENT.
#
# Licensed under a MIT (SEI)-style license, please see license.txt or contact permission@sei.cmu.edu for full terms.
#
# [DISTRIBUTION STATEMENT A] This material has been approved for public release and unlimited distribution.  Please see Copyright notice for non-US Government use and distribution.
#
# This Software includes and/or makes use of Third-Party Software each subject to its own license.
#
# DM25-0931
###


from dataclasses import dataclass
from enum import Enum, StrEnum
import os
import re
import pandas as pd


class SbomTarget(StrEnum):
    """ Enum for all of the sbom targets and using the filename convention for value """
    DEPENDENCY_TRACK = "dependency-track"
    GIN = "gin"
    HEXYL = "hexyl"
    HTTPIE = "httpie"
    JQ = "jq"
    MINE_COLONIES = "minecolonies"
    NODEJS_GOOF = "nodejs-goof"
    OPENCV = "opencv"
    PHP_MAILER = "phpmailer"
    UNKNOWN = ""

    @staticmethod
    def from_name(name):
        try:
            return SbomTarget(name)
        except ValueError:
            return SbomTarget.UNKNOWN

class SbomFormat(StrEnum):
    """ Enum for all of the sbom formats that we support and using the file extension convention for value """
    JSON = "json"
    XML = "xml"
    UNKNOWN = ""

    def isJson(fmt):
        return fmt is SbomFormat.JSON

    @staticmethod
    def from_name(name):
        try:
            return SbomFormat(name)
        except ValueError:
            return SbomFormat.UNKNOWN

class SbomStandard(StrEnum):
    """ Enum for all of the sbom standards that we support and using the filename convention for value """
    CYCLONEDX = ("cyclonedx")
    SPDX = ("spdx")
    UNKNOWN = ("")

    def isCycloneDx(std):
        return std is SbomStandard.CYCLONEDX

    def isSpdx(std):
        return std is SbomStandard.SPDX
    
    @staticmethod
    def from_name(name):
        try:
            return SbomStandard(name)
        except ValueError:
            return SbomStandard.UNKNOWN

class SbomPhase(Enum):
    """ Enum for all of the sbom lifecycle phases we support and using the filename convention for value """
    BUILD = ("build")
    SOURCE = ("source")
    UNKNOWN = ("")

    def isBuild(phase):
        return phase is SbomPhase.BUILD

    def isSource(phase):
        return phase is SbomPhase.SOURCE

    @staticmethod
    def from_name(name):
        try:
            return SbomPhase(name)
        except ValueError:
            return SbomPhase.UNKNOWN

@dataclass
class SbomFile:
    """ Data about an sbom that can be determined by our filenaming conventions """
    format: SbomFormat
    phase: SbomPhase
    standard: SbomStandard
    target: SbomTarget
    filepath: str
    submitter: str = ""
    isBaseline: bool = False

    def isValid(file):
        return (
            file.format is not SbomFormat.UNKNOWN and 
            file.phase is not SbomPhase.UNKNOWN and 
            file.standard is not SbomStandard.UNKNOWN and 
            file.target is not SbomTarget.UNKNOWN)

    @staticmethod
    def invalidFile(filepath: str):
        return SbomFile(
            filepath = filepath,
            format = SbomFormat.UNKNOWN,
            phase = SbomPhase.UNKNOWN,
            standard = SbomStandard.UNKNOWN,
            target = SbomTarget.UNKNOWN)

@dataclass
class SbomAnalysis:
    """Data resulting from analyzing a single SBOM"""
    component_df: pd.DataFrame
    component_versions_df: pd.DataFrame
    summary: dict
    submitter: str = ""
    isBaseline: bool = False

@dataclass
class TargetAnalysis:
    """Data resulting from analyzing all SBOMs for a given target"""
    target_component_df: pd.DataFrame
    target_component_versions_df: pd.DataFrame
    target_summary: dict
    target_file_count: int

sbom_by_target_dir = "../submissions_by_target/"
sbom_scrubbed_submission_dir = "../sbom-submissions/scrubbed-submissions/"
sbom_baseline_dir = "../baseline_sboms"

cyclone_output_dir = "../outputs/cycloneDX_sbom_data"
cyclone_baseline_output_dir = "cycloneDX_sbom_data/baseline"


component_similarity_dir = "component_similarity"
summary_stats_dir = "summary_files"
individual_info_dir = "individual_component_info"

baseline_submitters = ["mssbom", "syft", "trivy"]

# file name patter: vendor_target_type_standard_*.ext
all_targets = [target.value for target in SbomTarget]
file_pattern = re.compile(r"([a-zA-Z0-9]*)_({})_(build|source)_(cyclonedx|spdx)_.*\.(json|xml)".format("|".join(all_targets)))

def sbomInfoFromFile(filepath: str):
    info = SbomFile.invalidFile(filepath)
    filename = os.path.basename(filepath)
    match = file_pattern.match(filename)
    if match and match.lastindex == 5:
        info = SbomFile(
            submitter = match.group(1),
            isBaseline = match.group(1) in baseline_submitters,
            target = SbomTarget.from_name(match.group(2)),
            filepath = filepath,
            phase = SbomPhase.from_name(match.group(3)),
            standard = SbomStandard.from_name(match.group(4)),
            format = SbomFormat.from_name(match.group(5)))
    
    return info


