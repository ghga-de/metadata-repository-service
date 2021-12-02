# Copyright 2021 Universität Tübingen, DKFZ and EMBL
# for the German Human Genome-Phenome Archive (GHGA)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"Routes for retrieving Analysis Processes"

from typing import List

from fastapi import APIRouter

from metadata_repository_service.dao.analysis_process import (
    get_analysis_process,
    retrieve_analysis_processes,
)
from metadata_repository_service.models import AnalysisProcess

analysis_process_router = APIRouter()


@analysis_process_router.get(
    "/analysis_processes",
    response_model=List[AnalysisProcess],
    summary="Get all AnalysisProcess IDs",
)
async def get_all_analysis_processes():
    """
    Retrieve a list of AnalysisProcess IDs from the metadata store.
    """
    analysis_processes = await retrieve_analysis_processes()
    return analysis_processes


@analysis_process_router.get(
    "/analysis_process/{analysis_process_id}",
    response_model=AnalysisProcess,
    summary="Get an AnalysisProcess",
)
async def get_analysis_processes(analysis_process_id: str, embedded: bool = False):
    """
    Given an AnalysisProcess ID, get the AnalysisProcess record from the metadata store.
    """
    analysis_process = await get_analysis_process(analysis_process_id, embedded)
    return analysis_process
