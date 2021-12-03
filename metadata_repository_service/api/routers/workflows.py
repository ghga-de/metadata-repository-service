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
"Routes for retrieving Workflows"

from fastapi import APIRouter

from metadata_repository_service.dao.workflow import get_workflow
from metadata_repository_service.models import Workflow

workflow_router = APIRouter()


@workflow_router.get(
    "/workflows/{workflow_id}",
    response_model=Workflow,
    summary="Get a Workflow",
)
async def get_workflows(workflow_id: str, embedded: bool = False):
    """
    Given a Workflow ID, get the Workflow record from the metadata store.
    """
    workflow = await get_workflow(workflow_id, embedded)
    return workflow
