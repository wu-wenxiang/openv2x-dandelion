# Copyright 2022 99Cloud, Inc. All Rights Reserved.
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

from __future__ import annotations

from typing import Dict

from fastapi import APIRouter, Depends, status
from oslo_config import cfg
from sqlalchemy.orm import Session

from dandelion import crud, models, schemas
from dandelion.api import deps
from dandelion.api.deps import OpenV2XHTTPException as HTTPException
from dandelion.mqtt import cloud_server as mqtt_cloud_server

router = APIRouter()
CONF: cfg = cfg.CONF
mode_conf = CONF.mode
mqtt_conf = CONF.mqtt


@router.post(
    "",
    response_model=schemas.SystemConfig,
    status_code=status.HTTP_200_OK,
    description="""
Get detailed info of System Config.
""",
    responses={
        status.HTTP_200_OK: {"model": schemas.SystemConfig, "description": "OK"},
        **deps.RESPONSE_ERROR,
    },
)
def create(
    edge_in: schemas.SystemConfigCreate,
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> schemas.SystemConfig:
    """
    Set system configuration.
    """
    system_config = crud.system_config.get(db, id=1)
    system_config = (
        crud.system_config.update(db, db_obj=system_config, obj_in=edge_in)
        if system_config
        else crud.system_config.create(db, obj_in=edge_in)
    )
    if mqtt_cloud_server.MQTT_CLIENT:
        mqtt_cloud_server.MQTT_CLIENT.disconnect()
    mqtt_cloud_server.connect()
    while not mqtt_cloud_server.MQTT_CLIENT:
        if mqtt_cloud_server.ERROR_CONFIG:
            mqtt_cloud_server.ERROR_CONFIG = False
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Cloud MQTT Connection failed"
            )

    return system_config.to_dict()


@router.get(
    "/{system_config_id}",
    response_model=schemas.SystemConfig,
    status_code=status.HTTP_200_OK,
    description="""
Get detailed info of System Config.
""",
    responses={
        status.HTTP_200_OK: {"model": schemas.SystemConfig, "description": "OK"},
        **deps.RESPONSE_ERROR,
    },
)
def get(
    system_config_id: int,
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> schemas.SystemConfig:
    system_config = deps.crud_get(
        db=db,
        obj_id=system_config_id,
        crud_model=crud.system_config,
        detail="System config",
    )
    system_config.mode = mode_conf.mode
    return system_config.to_dict()


@router.get(
    "/edge/mqtt_config",
    response_model=Dict,
    status_code=status.HTTP_200_OK,
    description="""
Get edge site mqtt config.
""",
)
def get_edge_mqtt_config(
    current_user: models.User = Depends(deps.get_current_user),
) -> Dict:
    return {
        "username": CONF.mqtt.username,
        "password": CONF.mqtt.password,
    }
