# Copyright 2015 Letv Cloud Computing
# All Rights Reserved
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
#

from neutronclient.i18n import _
from neutronclient.neutron import v2_0 as neutronV20


def _get_listener_id(client, listener_id_or_name):
    return neutronV20.find_resourceid_by_name_or_id(
        client, 'listener', listener_id_or_name, cmd_resource='listener')


class LbaasRuleMixin(object):

    def set_extra_attrs(self, parsed_args):
        self.parent_id = _get_listener_id(self.get_client(),
                                          parsed_args.listener)

    def add_known_arguments(self, parser):
        parser.add_argument(
            'listener', metavar='LISTENER',
            help=_('ID or name of the listener '
                   'that this rule belongs to.'))


class ListRule(LbaasRuleMixin, neutronV20.ListCommand):
    """LBaaS v2 List rules that belong to a given tenant."""

    resource = 'rule'
    shadow_resource = 'lbaas_rule'
    list_columns = ['id', 'name', 'description', 'rule',
                    'admin_state_up']
    pagination_support = True
    sorting_support = True


class ShowRule(LbaasRuleMixin, neutronV20.ShowCommand):
    """LBaaS v2 Show information of a given rule."""

    resource = 'rule'
    shadow_resource = 'lbaas_rule'


class CreateRule(neutronV20.CreateCommand):
    """LBaaS v2 Create a rule."""

    resource = 'rule'
    shadow_resource = 'lbaas_rule'

    def add_known_arguments(self, parser):
        parser.add_argument(
            '--admin-state-down',
            dest='admin_state', action='store_false',
            help=_('Set admin state up to false.'))
        parser.add_argument(
            '--description',
            help=_('Description of the rule.'))
        parser.add_argument(
            '--name', help=_('The name of the rule.'))
        parser.add_argument(
            '--rule-str',
            dest='rule_str', required=True,
            help=_('The haproxy rule string.'))
        parser.add_argument(
            'listener', metavar='LISTENER',
            help=_('ID or name of the listener '
                   'that this rule belongs to.'))

    def args2body(self, parsed_args):
        self.parent_id = _get_listener_id(self.get_client(),
                                          parsed_args.listener)
        body = {
            self.resource: {
                'admin_state_up': parsed_args.admin_state,
                'rule': parsed_args.rule_str
            },
        }
        neutronV20.update_dict(parsed_args, body[self.resource],
                               ['description', 'name',
                                'tenant_id'])
        return body


class UpdateRule(neutronV20.UpdateCommand):
    """LBaaS v2 Update a given rule."""

    resource = 'rule'
    shadow_resource = 'lbaas_rule'

    def add_known_arguments(self, parser):
        parser.add_argument(
            '--admin-state-down',
            dest='admin_state', action='store_false',
            help=_('Set admin state up to false.'))
        parser.add_argument(
            '--description',
            help=_('Description of the rule.'))
        parser.add_argument(
            '--name', help=_('The name of the rule.'))
        parser.add_argument(
            '--rule-str',
            dest='rule_str',
            help=_('The haproxy rule string.'))
        parser.add_argument(
            'listener', metavar='LISTENER',
            help=_('ID or name of the listener '
                   'that this rule belongs to.'))

    def args2body(self, parsed_args):
        self.parent_id = _get_listener_id(self.get_client(),
                                          parsed_args.listener)
        body = {
            self.resource: {'rule': parsed_args.rule_str}
        }
        neutronV20.update_dict(parsed_args, body[self.resource],
                               ['admin_state_up', 'name',
                                'description'])
        return body


class DeleteRule(LbaasRuleMixin, neutronV20.DeleteCommand):
    """LBaaS v2 Delete a given rule."""

    resource = 'rule'
    shadow_resource = 'lbaas_rule'
