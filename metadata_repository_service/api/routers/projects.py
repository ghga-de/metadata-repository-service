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
"Routes for retrieving Projects"

from fastapi import APIRouter

from metadata_repository_service.dao.project import get_project
from metadata_repository_service.models import Project

project_router = APIRouter()


@project_router.get(
    "/projects/{project_id}",
    response_model=Project,
    summary="Get a Project",
)
async def get_projects(project_id: str, embedded: bool = False):
    """
    Given a Project ID, get the Project record from the metadata store.
    """
    project = await get_project(project_id, embedded)
    return project
