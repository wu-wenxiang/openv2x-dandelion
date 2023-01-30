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

# flake8: noqa
# fmt: off

"""intersection_fk

Revision ID: a04def91cc98
Revises: 3e1d76cb6ae9
Create Date: 2022-11-25 16:04:52.062438

"""
import sqlalchemy as sa
from alembic import op
from oslo_config import cfg

import dandelion.conf
from dandelion import constants, version

CONF: cfg = dandelion.conf.CONF

CONF(
    args=["--config-file", constants.CONFIG_FILE_PATH],
    project=constants.PROJECT_NAME,
    version=version.version_string(),
)
# revision identifiers, used by Alembic.
revision = "a04def91cc98"
down_revision = "3e1d76cb6ae9"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    if not CONF.database.connection.startswith("sqlite"):
        op.drop_constraint("map_ibfk_1", "map", type_="foreignkey")
        op.drop_constraint("rsi_event_ibfk_1", "rsi_event", type_="foreignkey")
        op.drop_constraint("rsu_ibfk_1", "rsu", type_="foreignkey")
        op.drop_constraint("edge_node_rsu_ibfk_1", "edge_node_rsu", type_="foreignkey")
        op.drop_index(op.f("area_code"), table_name="map")
        op.drop_index(op.f("area_code"), table_name="rsi_event")
        op.drop_index(op.f("area_code"), table_name="rsu")
        op.drop_index(op.f("area_code"), table_name="edge_node_rsu")
    op.drop_index(op.f("ix_rsi_event_address"), table_name="rsi_event")

    with op.batch_alter_table("map", schema=None) as batch_op:
        batch_op.add_column(  # type: ignore[attr-defined]
            sa.Column("intersection_code", sa.String(length=64), nullable=False))
        batch_op.drop_column("address")  # type: ignore[attr-defined]
        batch_op.drop_column("area_code")  # type: ignore[attr-defined]
        batch_op.create_foreign_key(  # type: ignore[attr-defined]
            "intersection_fk_code_map", "intersection", ["intersection_code"], ["code"],
            onupdate='CASCADE', ondelete='RESTRICT'
        )

    with op.batch_alter_table("rsi_event", schema=None) as batch_op:
        batch_op.add_column( # type: ignore[attr-defined]
            sa.Column("intersection_code", sa.String(length=64), nullable=False))
        batch_op.drop_column("address")  # type: ignore[attr-defined]
        batch_op.drop_column("area_code")  # type: ignore[attr-defined]
        batch_op.create_foreign_key(  # type: ignore[attr-defined]
            "intersection_fk_code_rsi_event", "intersection", ["intersection_code"], ["code"],
            onupdate='CASCADE', ondelete='RESTRICT'
        )

    with op.batch_alter_table("rsu", schema=None) as batch_op:
        batch_op.add_column(  # type: ignore[attr-defined]
            sa.Column("intersection_code", sa.String(length=64), nullable=False))
        batch_op.drop_column("address")  # type: ignore[attr-defined]
        batch_op.drop_column("area_code")  # type: ignore[attr-defined]
        batch_op.create_foreign_key(  # type: ignore[attr-defined]
            "intersection_fk_code_rsu", "intersection", ["intersection_code"], ["code"],
            onupdate='CASCADE', ondelete='RESTRICT'
        )

    with op.batch_alter_table("edge_node_rsu", schema=None) as batch_op:
        batch_op.add_column(  # type: ignore[attr-defined]
            sa.Column("intersection_code", sa.String(length=64), nullable=False))
        batch_op.drop_column("area_code")  # type: ignore[attr-defined]
        batch_op.create_foreign_key(  # type: ignore[attr-defined]
            "intersection_fk_code_edge_node_rsu", "intersection", ["intersection_code"], ["code"],
            onupdate='CASCADE', ondelete='RESTRICT'
        )
    # mypy: end ignore
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    # mypy: begin ignore
    with op.batch_alter_table("rsu", schema=None) as batch_op:
        batch_op.add_column(sa.Column("area_code", sa.VARCHAR(length=64), nullable=True))  # type: ignore[attr-defined]
        batch_op.add_column(sa.Column("address", sa.VARCHAR(length=255), nullable=False))  # type: ignore[attr-defined]
        batch_op.drop_constraint("intersection_fk_code_rsu", type_="foreignkey")  # type: ignore[attr-defined]
        batch_op.create_foreign_key(None, "area", ["area_code"], ["code"])  # type: ignore[attr-defined]
        batch_op.drop_column("intersection_code")  # type: ignore[attr-defined]

    with op.batch_alter_table("rsi_event", schema=None) as batch_op:
        batch_op.add_column(sa.Column("area_code", sa.VARCHAR(length=64), nullable=True))  # type: ignore[attr-defined]
        batch_op.add_column(sa.Column("address", sa.VARCHAR(length=255), nullable=False))  # type: ignore[attr-defined]
        batch_op.drop_constraint("intersection_fk_code_rsi_event", type_="foreignkey")  # type: ignore[attr-defined]
        batch_op.create_foreign_key(None, "area", ["area_code"], ["code"])  # type: ignore[attr-defined]
        batch_op.drop_column("intersection_code")  # type: ignore[attr-defined]
    op.create_index(op.f("ix_rsi_event_address"), "rsi_event", ["address"], unique=False)

    with op.batch_alter_table("map", schema=None) as batch_op:
        batch_op.add_column(sa.Column("area_code", sa.VARCHAR(length=64), nullable=True))  # type: ignore[attr-defined]
        batch_op.add_column(sa.Column("address", sa.VARCHAR(length=255), nullable=False))  # type: ignore[attr-defined]
        batch_op.drop_constraint("intersection_fk_code_map", type_="foreignkey")  # type: ignore[attr-defined]
        batch_op.create_foreign_key(None, "area", ["area_code"], ["code"])  # type: ignore[attr-defined]
        batch_op.drop_column("intersection_code")  # type: ignore[attr-defined]

    with op.batch_alter_table("edge_node_rsu", schema=None) as batch_op:
        batch_op.add_column(sa.Column("area_code", sa.VARCHAR(length=64), nullable=True))  # type: ignore[attr-defined]
        batch_op.drop_constraint("intersection_fk_code_edge_node_rsu", type_="foreignkey")  # type: ignore[attr-defined]
        batch_op.create_foreign_key(None, "area", ["area_code"], ["code"])  # type: ignore[attr-defined]
        batch_op.drop_column("intersection_code")  # type: ignore[attr-defined]
    # mypy: end ignore
    # ### end Alembic commands ###
