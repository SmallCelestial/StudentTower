import pytest
import pygame
from steps_lib import StepTemplate, FloorSnowbiom, StepSnowbiom, StepJunglebiom, StepLavabiom
from unittest.mock import patch, Mock


@pytest.fixture
def my_step_template():
    return StepTemplate(0, 1)


@pytest.fixture
def my_floor_snowbiom():
    with patch('pygame.image.load', return_value=Mock()):
        return FloorSnowbiom(100, 0)


@pytest.fixture
def my_step_snowbiom():
    with patch('pygame.image.load', return_value=Mock()):
        return StepSnowbiom(100, 1)


@pytest.fixture
def my_step_junglebiom():
    with patch('pygame.image.load', return_value=Mock()):
        return StepJunglebiom(100, 1)


@pytest.fixture
def my_step_lavabiom():
    with patch('pygame.image.load', return_value=Mock()):
        return StepLavabiom(100, 1)


def test_initialization_of_StepTemplate(my_step_template):
    assert my_step_template.step_height == 0
    assert my_step_template.step_number == 1


def test_initialize_animation_frames(my_step_template):
    my_step_template.initialize_animation_frames()
    assert len(my_step_template.animation_frames) == 5


def test_destruction_mechanic(my_step_template):
    step_group = pygame.sprite.Group()
    destruction_ready_step = my_step_template
    destruction_ready_step.destruction = True
    step_group.add(destruction_ready_step)
    pygame.sprite.Group.sprites(step_group)[0].destruction_mechanic()
    assert len(step_group) == 0


def test_initialisation_of_FloorSnowbiom(my_floor_snowbiom):
    assert my_floor_snowbiom.step_height == 100
    assert my_floor_snowbiom.step_number == 0
    assert my_floor_snowbiom.top_left[0] == 0


def test_initialisation_of_StepSnowbiom(my_step_snowbiom):
    assert len(my_step_snowbiom.animation_frames) == 5
    assert my_step_snowbiom.step_number == 1
    assert my_step_snowbiom.step_height == 100
    assert 100 <= my_step_snowbiom.top_left[0] <= 600

    for frame in my_step_snowbiom.animation_frames:
        assert isinstance(frame, Mock)


def test_initialisation_of_StepJunglebiom(my_step_junglebiom):
    assert len(my_step_junglebiom.animation_frames) == 5
    assert my_step_junglebiom.step_number == 1
    assert my_step_junglebiom.step_height == 100
    assert 100 <= my_step_junglebiom.top_left[0] <= 600

    for frame in my_step_junglebiom.animation_frames:
        assert isinstance(frame, Mock)


def test_initialisation_of_StepLavabiom(my_step_lavabiom):
    assert len(my_step_lavabiom.animation_frames) == 5
    assert my_step_lavabiom.step_number == 1
    assert my_step_lavabiom.step_height == 100
    assert 100 <= my_step_lavabiom.top_left[0] <= 600

    for frame in my_step_lavabiom.animation_frames:
        assert isinstance(frame, Mock)
