import pytest
import pygame
from steps_lib import StepTemplate, FloorSnowbiom, StepSnowbiom, StepJunglebiom, StepLavabiom
from unittest.mock import patch, Mock

@pytest.fixture
def my_stepTemplate():
    return StepTemplate(0,1)

@pytest.fixture
def my_floorSnowbiom():
    with patch('pygame.image.load', return_value=Mock()):
        return FloorSnowbiom(100, 0)

@pytest.fixture
def my_stepSnowbiom():
    with patch('pygame.image.load', return_value=Mock()):
        return StepSnowbiom(100, 1)

@pytest.fixture
def my_stepJunglebiom():
    with patch('pygame.image.load', return_value=Mock()):
        return StepJunglebiom(100, 1)

@pytest.fixture
def my_stepLavabiom():
    with patch('pygame.image.load', return_value=Mock()):
        return StepLavabiom(100, 1)

def test_initialization_of_StepTemplate(my_stepTemplate):
    assert my_stepTemplate.step_height == 0
    assert my_stepTemplate.step_number == 1

def test_initialize_animation_frames(my_stepTemplate):
    my_stepTemplate.initialize_animation_frames()
    assert len(my_stepTemplate.animation_frames) == 5

def test_destruction_mechanic(my_stepTemplate):
    step_group = pygame.sprite.Group()
    destruction_ready_step = my_stepTemplate
    destruction_ready_step.destruction = True
    step_group.add(destruction_ready_step)
    pygame.sprite.Group.sprites(step_group)[0].destruction_mechanic()
    assert len(step_group) == 0

def test_initialisation_of_FloorSnowbiom(my_floorSnowbiom):
    assert my_floorSnowbiom.step_height == 100
    assert my_floorSnowbiom.step_number == 0
    assert my_floorSnowbiom.top_left[0] == 0

def test_initialisation_of_StepSnowbiom(my_stepSnowbiom):
    assert len(my_stepSnowbiom.animation_frames) == 5
    assert my_stepSnowbiom.step_number == 1
    assert my_stepSnowbiom.step_height == 100
    assert 300 <= my_stepSnowbiom.top_left[0] <= 600

    for frame in my_stepSnowbiom.animation_frames:
        assert isinstance(frame, Mock)

def test_initialisation_of_StepJunglebiom(my_stepJunglebiom):
    assert len(my_stepJunglebiom.animation_frames) == 5
    assert my_stepJunglebiom.step_number == 1
    assert my_stepJunglebiom.step_height == 100
    assert 300 <= my_stepJunglebiom.top_left[0] <= 600

    for frame in my_stepJunglebiom.animation_frames:
        assert isinstance(frame, Mock)

def test_initialisation_of_StepLavabiom(my_stepLavabiom):
    assert len(my_stepLavabiom.animation_frames) == 5
    assert my_stepLavabiom.step_number == 1
    assert my_stepLavabiom.step_height == 100
    assert 300 <= my_stepLavabiom.top_left[0] <= 600

    for frame in my_stepLavabiom.animation_frames:
        assert isinstance(frame, Mock)


