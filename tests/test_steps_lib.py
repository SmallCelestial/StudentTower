import pytest
import pygame
from steps_lib import StepTemplate, FloorSnowbiom, StepSnowbiom, StepJunglebiom, StepLavabiom
from unittest.mock import patch, Mock

@pytest.fixture
def my_StepTemplate():
    return StepTemplate(1)

@pytest.fixture
def my_FloorSnowbiom():
    with patch('pygame.image.load', return_value=Mock()):
        return FloorSnowbiom(100, 0)

@pytest.fixture
def my_StepSnowbiom():
    with patch('pygame.image.load', return_value=Mock()):
        return StepSnowbiom(100, 1)

def test_initialization_of_StepTemplate(my_StepTemplate):
    assert my_StepTemplate.tall == my_StepTemplate.width == my_StepTemplate.height == my_StepTemplate.biom_id == 0
    assert my_StepTemplate.topLeft == [0,0]
    assert my_StepTemplate.number == 1

def test_initialize_animation_frames(my_StepTemplate):
    my_StepTemplate.initialize_animation_frames()
    assert len(my_StepTemplate.animation_frames) == 5

def test_destruction_mechanic(my_StepTemplate):
    step_group = pygame.sprite.Group()
    destruction_ready_step = my_StepTemplate
    destruction_ready_step.destruction = True
    step_group.add(destruction_ready_step)
    pygame.sprite.Group.sprites(step_group)[0].destruction_mechanic()
    assert len(step_group) == 0

def test_initialisation_of_FloorSnowbiom(my_FloorSnowbiom):
    assert my_FloorSnowbiom.tall == 100
    assert my_FloorSnowbiom.width == 1000
    assert my_FloorSnowbiom.top_left == [0, 900]
    assert my_FloorSnowbiom.biom_id == 1

    assert my_FloorSnowbiom.height == 100
    assert my_FloorSnowbiom.number == 0

def test_initialisation_of_StepSnowbiom(my_StepSnowbiom):
    assert len(my_StepSnowbiom.animation_frames) == 5
    assert my_StepSnowbiom.number == 1
    assert my_StepSnowbiom.height == 100
    assert my_StepSnowbiom.biom_id == 1
    assert 300 <= my_StepSnowbiom.top_left[0] <= 600

    # Ensure the animation frames are mocks
    for frame in my_StepSnowbiom.animation_frames:
        assert isinstance(frame, Mock)

