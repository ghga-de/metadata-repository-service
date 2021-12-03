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

"""Test the api module"""

import nest_asyncio
import pytest
from fastapi import status
from fastapi.testclient import TestClient

from metadata_repository_service.api.main import app
from metadata_repository_service.config import Config, get_config

nest_asyncio.apply()


def get_config_override():
    return Config(db_url="mongodb://localhost:27017", db_name="metadata-store-test")


app.dependency_overrides[get_config] = get_config_override
client = TestClient(app)


def test_index():
    """Test the index endpoint"""

    client = TestClient(app)
    response = client.get("/")

    assert response.status_code == status.HTTP_200_OK
    assert response.text == '"Index of the Metadata Repository Service"'


@pytest.mark.parametrize(
    "route,entity_id,check_conditions",
    [
        (
            "datasets",
            "12461315-7bd4-40ff-9c2f-0e0fa4cd6c66",
            {"accession": "EGAD00001000174"},
        ),
        (
            "studies",
            "595c6fe1-1908-4596-b72a-ac89b7960375",
            {"accession": "EGAS00001000274"},
        ),
        (
            "experiments",
            "997dda34-5ed5-42f3-877b-c9cc327d35ff",
            {"has_study": "595c6fe1-1908-4596-b72a-ac89b7960375"},
        ),
        (
            "samples",
            "b66a6217-0db0-4619-af77-6f1e19339aaa",
            {"has_biospecimen": "3b7e3e84-5165-44d4-a636-3a0a825c2491"},
        ),
        (
            "biospecimens",
            "3b7e3e84-5165-44d4-a636-3a0a825c2491",
            {"name": "Biospecimen for Sample b66a6217-0db0-4619-af77-6f1e19339aaa"},
        ),
    ],
)
@pytest.mark.asyncio
async def test_get_entity_by_id(initialize_test_db, route, entity_id, check_conditions):
    response = client.get(f"/{route}/{entity_id}")
    assert response.status_code == 200
    data = response.json()
    assert "id" in data and data["id"] == entity_id
    for key, value in check_conditions.items():
        assert key in data and data[key] == value
