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

from oslo_config import cfg

user_group = cfg.OptGroup(
    name="iam",
    title="iam Options",
    help="""
iam related options.
""",
)

user_opts = [
    cfg.StrOpt(
        "get_auth_info_url",
        default="http://203.166.165.251:16056/?Action=GetAuthInfo",
        help="""
iam get_auth_info_url.
""",
    ),
]


def register_opts(conf):
    conf.register_group(user_group)
    conf.register_opts(user_opts, group=user_group)


def list_opts():
    return {user_group: user_opts}
