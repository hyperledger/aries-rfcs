import os
import pytest
import tempfile

@pytest.fixture
def code_cwd():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

@pytest.fixture
def scratch_space():
    x = tempfile.TemporaryDirectory()
    yield x
    x.cleanup()

def test_index(code_cwd, scratch_space):
    temp_idx = os.path.join(scratch_space.name, 'index.md')
    import generate_index
    generate_index.main(temp_idx)
    if os.system('diff ../index.md ' + temp_idx):
        pytest.fail("/index.md needs to be updated. Run python code/generate_index.py.")
    

