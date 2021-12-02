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
"Routes for retrieving Analyses"

from typing import List

from fastapi import APIRouter

from metadata_repository_service.dao.analysis import get_analysis, retrieve_analyses
from metadata_repository_service.models import Analysis

analysis_router = APIRouter()


@analysis_router.get(
    "/analyses", response_model=List[str], summary="Get all Analysis IDs"
)
async def get_all_analyses():
    """
    Retrieve a list of Analysis IDs from the metadata store.
    """
    analyses = await retrieve_analyses()
    return analyses


@analysis_router.get(
    "/analyses/{analysis_id}", response_model=Analysis, summary="Get an Analysis"
)
async def get_analyses(analysis_id: str, embedded: bool = False):
    """
    Given an Analysis ID, get the Analysis record from the metadata store.
    """
    analysis = await get_analysis(analysis_id, embedded)
    return analysis
