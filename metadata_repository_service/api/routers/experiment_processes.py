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
"Routes for retrieving ExperimentProcesses"

from typing import List

from fastapi import APIRouter

from metadata_repository_service.dao.experiment_process import (
    get_experiment_process,
    retrieve_experiment_processes,
)
from metadata_repository_service.models import ExperimentProcess

experiment_process_router = APIRouter()


@experiment_process_router.get(
    "/experiment_processes",
    response_model=List[str],
    summary="Get all ExperimentProcess IDs",
)
async def get_all_experiment_processes():
    """
    Retrieve a list of ExperimentProcess IDs from the metadata store.
    """
    experiment_processes = await retrieve_experiment_processes()
    return experiment_processes


@experiment_process_router.get(
    "/experiment_processes/{experiment_process_id}",
    response_model=ExperimentProcess,
    summary="Get a ExperimentProcess",
)
async def get_experiment_processes(experiment_process_id: str, embedded: bool = False):
    """
    Given a ExperimentProcess ID, get the ExperimentProcess record from the metadata store.
    """
    experiment_process = await get_experiment_process(experiment_process_id, embedded)
    return experiment_process
