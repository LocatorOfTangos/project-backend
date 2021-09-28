import pytest

from src.auth import auth_register_v1
from src.error import InputError
from src.other import clear_v1
from src.channel import channel_details_v1, channel_join_v1
from src.channels import channels_create_v1


def test_invalid_channel_id():
    '''
    Test for invalid channel id
    '''
    clear_v1()
    u_id = auth_register_v1("testemail@gmail.com", "password", "vu", "luu")
    with pytest.raises(InputError):
        assert(channel_details_v1(u_id, 3))

@pytest.mark.skip(reason = "waiting for channels_create implementation")   
def test_valid_channel_id():
    '''
    Test for valid channel id and user id
    '''
    clear_v1()
    u_id = auth_register_v1("testemail@gmail.com", "password", "vu", "luu")
    channel_id = channels_create_v1(u_id, "test channel", True)
    channel_detail = {}
    channel_detail = channel_details_v1(u_id, channel_id)
    assert(channel_detail) == {
        'name': 'test channel',
        'is_public': True,
        'owner_members': [
            {
                'user_id': u_id,
                'name_first': 'vu',
                'name_last': 'luu',
            },
        ],
        'all_members': [
            {
                'user_id': u_id ,
                'name_first': 'vu',
                'name_last': 'luu',
            },
        ],
    }

@pytest.mark.skip(reason = "waiting for channels_create implementation")
def test_user_not_authorised():
    '''
    Test when channel_id is valid and the authorised user is not a member of the channel
    '''
    clear_v1()
    u_id = auth_register_v1("testemail@gmail.com", "password", "vu", "luu")
    u2_id = auth_register_v1("secondtestemail@gmail.com", "password", "david", "smith")
    channel_id = channels_create_v1(u_id, "test channel", True)
    with pytest.raises(AccessError):
        assert(channel_details_v1(u2_id, channel_id))







    
