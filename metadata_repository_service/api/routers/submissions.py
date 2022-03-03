# Copyright 2021 - 2022 Universität Tübingen, DKFZ and EMBL
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
"Routes to support Submissions"

import copy

from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException

from metadata_repository_service.api.deps import get_config
from metadata_repository_service.config import Config
from metadata_repository_service.core.utils import (
    delete_document,
    get_timestamp,
    link_embedded,
    parse_document,
    store_document,
    update_document,
)
from metadata_repository_service.dao.submission import (
    get_submission,
    update_submission_values,
)
from metadata_repository_service.models import (
    CreateSubmission,
    Submission,
    SubmissionStatusPatch,
)

submission_router = APIRouter()


@submission_router.post(
    "/submissions",
    summary="Add a submission object to a metadata store",
    response_model=Submission,
)
async def add_submission(
    input_submission: CreateSubmission, config: Config = Depends(get_config)
):
    """Add a submission object to a metadata store."""
    if input_submission is None:
        raise HTTPException(
            status_code=400,
            detail="Unexpected error",
        )

    document = input_submission.dict()
    docs = await parse_document(document)
    docs = await link_embedded(docs)
    docs = await update_document(document, docs)

    await store_document(docs, config)

    return docs["parent"][1]


@submission_router.get(
    "/submissions/{submission_id}",
    response_model=Submission,
    summary="Get a Submission",
)
async def get_submissions(
    submission_id: str, embedded: bool = False, config: Config = Depends(get_config)
):
    """
    Given a Submission ID, get the corresponding Submission record
    from the metadata store.
    """
    submission = await get_submission(
        submission_id=submission_id, embedded=embedded, config=config
    )
    if not submission:
        raise HTTPException(
            status_code=404,
            detail=f"{Submission.__name__} with id '{submission_id}' not found",
        )
    return submission


@submission_router.patch(
    "/submissions/{submission_id}",
    response_model=Submission,
    summary="Update the status of a submission",
)
async def update_status(
    submission_id: str,
    status: SubmissionStatusPatch,
    config: Config = Depends(get_config),
):
    """
    Given a Submission ID and a status, update the status of corresponding
    Submission record from the metadata store.
    """
    submission = await get_submission(
        submission_id=submission_id, embedded=False, config=config
    )
    if not submission:
        raise HTTPException(
            status_code=404,
            detail=f"{Submission.__name__} with id '{submission_id}' not found",
        )

    if (status.status is not None) and (submission.status != status.status.value):
        update_json = {}
        update_json["status"] = status.status.value
        update_json["update_date"] = await get_timestamp()
        submission = await update_submission_values(submission_id, update_json, config)

    return submission


@submission_router.put(
    "/submissions/{submission_id}",
    response_model=Submission,
    summary="Update the submission",
)
async def update_submission(
    submission_id: str,
    input_submission: CreateSubmission,
    config: Config = Depends(get_config),
):
    """
    Given a Submission ID and an updated submission object,
    update the submission in the metadata store.
    """
    submission = await get_submission(
        submission_id=submission_id, embedded=False, config=config
    )
    if not submission:
        raise HTTPException(
            status_code=404,
            detail=f"{Submission.__name__} with id '{submission_id}' not found",
        )

    document = input_submission.dict()
    old_document = copy.deepcopy(submission.dict())
    await delete_document(old_document, "Submission", config=config)
    docs = await parse_document(document)
    docs = await link_embedded(docs)
    docs = await update_document(document, docs, old_document)
    await store_document(docs)

    return docs["parent"][1]
