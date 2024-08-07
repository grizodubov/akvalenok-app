import pytest

from app.spaces.dao import SpacesDAO


@pytest.mark.parametrize(
    "space_id,is_present",
    [
        (1, True),
        (6, True),
        (7, False),
    ],
)
async def test_find_space_by_id(space_id: int, is_present: bool):
    space = await SpacesDAO.find_one_or_none(id=space_id)

    if is_present:
        assert space
        assert space.id == space_id
    else:
        assert not space
