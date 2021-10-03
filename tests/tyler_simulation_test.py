import pytest

from src.error import (
    AccessError,
    InputError
)

from src.auth import (
    auth_login_v1,
    auth_register_v1
)
from src.channel import (
    channel_invite_v1,
    channel_details_v1,
    channel_join_v1
)
from src.channels import (
    channels_list_v1,
    channels_listall_v1,
    channels_create_v1
)

from src import validation as valid


def test_simulation_v1():
    # FAILED REGISTER
    with pytest.raises(InputError):
        assert auth_register_v1('tylergmail.com', '', 'Tyler', 'Gan')

    # REGISTERING SUCCESS
    person1_reg = auth_register_v1('tyler@gmail.com', 'ilovepasswords', 'Tyler', 'Gan')

    # LOGIN FAILURE
    with pytest.raises(InputError):
        auth_login_v1('tyler@yahoo.com.sg', 'ilovepasswords')
    with pytest.raises(InputError):
        auth_login_v1('tyler@gmail.com', 'idontlovepasswords')

    # LOGIN SUCCESS
    person1_login = auth_login_v1('tyler@gmail.com', 'ilovepasswords')
    assert person1_reg == person1_login

    # TRYING TO ADD A CHANNNEL AND FAILING
    with pytest.raises(AccessError):
        channels_create_v1(20002482, 'firstchannel', True)
    with pytest.raises(InputError):
        channels_create_v1(person1_reg['auth_user_id'], 'ilovehavingasuperlongchannelname', True)
    with pytest.raises(InputError):
        channels_create_v1(person1_reg['auth_user_id'], '', True)

    # CREATING NEW CHANNELS
    channels_create_v1(person1_reg['auth_user_id'], 'channel1', True)
    channels_create_v1(person1_reg['auth_user_id'], 'channel2', False)
    channels_create_v1(person1_reg['auth_user_id'], 'channel3', True)

    assert channels_list_v1(person1_reg['auth_user_id']) == {
        'channels': [
            {
                'channel_id': 0,
                'name': 'channel1',
            },
            {
                'channel_id': 1,
                'name': 'channel2',
            },
            {
                'channel_id': 2,
                'name': 'channel3',
            }
        ]
    }

    assert channel_details_v1(person1_reg['auth_user_id'], 1) == {
        'name': 'channel2',
        'is_public': False,
        'owner_members': [
            {
                'u_id': person1_reg['auth_user_id'],
                'name_first': 'tyler',
                'name_last': 'gan',
                'email': 'tyler@gmail.com',
                'handle_str': 'tylergan'
            },
        ],
        'all_members': [
            {
                'u_id': person1_reg['auth_user_id'],
                'name_first': 'tyler',
                'name_last': 'gan',
                'email': 'tyler@gmail.com',
                'handle_str': 'tylergan'
            }
        ],
    }

    # REGISTERING A SECOND USER
    person2_reg = auth_register_v1('blake@gmail.com', 'blakelovespasswords', 'Blake', 'Morris')
    person2_login = auth_login_v1('blake@gmail.com', 'blakelovespasswords')
    assert person2_reg == person2_login

    channels_create_v1(person2_reg['auth_user_id'], 'channel1', True)
    channels_create_v1(person2_reg['auth_user_id'], 'channel2', False)
    channels_create_v1(person2_reg['auth_user_id'], 'channel3', True)

    assert channels_list_v1(person2_reg['auth_user_id']) == {
        'channels': [
            {
                'channel_id': 3,
                'name': 'channel1',
            },
            {
                'channel_id': 4,
                'name': 'channel2',
            },
            {
                'channel_id': 5,
                'name': 'channel3',
            }
        ]
    }

    assert channels_listall_v1(person1_reg['auth_user_id']) == {
        'channels': [
            {
                'channel_id': 0,
                'name': 'channel1',
            },
            {
                'channel_id': 1,
                'name': 'channel2',
            },
            {
                'channel_id': 2,
                'name': 'channel3',
            },
            {
                'channel_id': 3,
                'name': 'channel1',
            },
            {
                'channel_id': 4,
                'name': 'channel2',
            },
            {
                'channel_id': 5,
                'name': 'channel3',
            }
        ]
    }

    # INVITING A USER
    assert channel_invite_v1(person1_reg['auth_user_id'], 0, person2_reg['auth_user_id']) == {}, 'PUBLIC INVITE FAILED'
    assert valid.user_is_member(person2_reg['auth_user_id'], 0)

    # JOINING A CHANNEL
    channel_join_v1(person1_reg['auth_user_id'], 3)
    assert valid.user_is_member(person1_reg['auth_user_id'], 3)

    with pytest.raises(AccessError):
        assert channel_join_v1(person2_reg['auth_user_id'], 1)
