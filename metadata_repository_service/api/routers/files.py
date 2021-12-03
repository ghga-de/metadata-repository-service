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
"Routes for retrieving Files"

from fastapi import APIRouter
from fastapi.exceptions import HTTPException

from metadata_repository_service.dao.file import get_file
from metadata_repository_service.models import File

file_router = APIRouter()


@file_router.get("/files/{file_id}", response_model=File, summary="Get a File")
async def get_files(file_id: str, embedded: bool = False):
    """
    Given a File ID, get the File record from the metadata store.
    """
    file = await get_file(file_id, embedded)
    if not file:
        raise HTTPException(
            status_code=404,
            detail=f"{File.__name__} with id '{file_id}' not found",
        )
    return file
