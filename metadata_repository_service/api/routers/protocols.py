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
"Routes for retrieving Protocols"

from typing import List

from fastapi import APIRouter

from metadata_repository_service.dao.protocol import get_protocol, retrieve_protocols
from metadata_repository_service.models import Protocol

protocol_router = APIRouter()


@protocol_router.get(
    "/protocols", response_model=List[str], summary="Get all Protocol IDs"
)
async def get_all_protocols():
    """
    Retrieve a list of Protocol IDs from the metadata store.
    """
    protocols = await retrieve_protocols()
    return protocols


@protocol_router.get(
    "/protocols/{protocol_id}",
    response_model=Protocol,
    summary="Get a Protocol",
)
async def get_protocols(protocol_id: str, embedded: bool = False):
    """
    Given a Protocol ID, get the Protocol record from the metadata store.
    """
    protocol = await get_protocol(protocol_id, embedded)
    return protocol
