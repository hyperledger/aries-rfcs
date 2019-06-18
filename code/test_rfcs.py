import os
import pytest
import tempfile

@pytest.fixture
def scratch_space():
    x = tempfile.TemporaryDirectory()
    yield x
    x.cleanup()

def test_index(scratch_space):
    temp_idx = os.path.join(scratch_space.name, 'index.md')
    import generate_index
    generate_index.main(temp_idx)
    perm_idx = os.path.join(os.path.dirname(__file__), '../index.md')
    if os.system('diff %s %s' % (perm_idx, temp_idx)):
        pytest.fail("/index.md needs to be updated. Run python code/generate_index.py.")
    
def test_links():
    import check_links
    assert check_links.main() == 0