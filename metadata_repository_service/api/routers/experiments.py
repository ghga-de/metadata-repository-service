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
"Routes for retrieving Experiments"

from typing import List

from fastapi import APIRouter

from metadata_repository_service.dao.experiment import (
    get_experiment,
    retrieve_experiments,
)
from metadata_repository_service.models import Experiment

experiment_router = APIRouter()


@experiment_router.get(
    "/experiments", response_model=List[str], summary="Get all Experiment IDs"
)
async def get_all_experiments():
    """
    Retrieve a list of Experiment IDs from the metadata store.
    """
    experiments = await retrieve_experiments()
    return experiments


@experiment_router.get(
    "/experiments/{experiment_id}",
    response_model=Experiment,
    summary="Get an Experiment",
)
async def get_experiments(experiment_id: str, embedded: bool = False):
    """
    Given a Experiment ID, get the Experiment record from the metadata store.
    """
    experiment = await get_experiment(experiment_id, embedded)
    return experiment
