import pytest
import pygame
from steps_lib import StepTemplate, FloorSnowbiom, StepSnowbiom, StepJunglebiom, StepLavabiom


@pytest.fixture
def my_stepTemplate():
    return StepTemplate(1)

@pytest.fixture
def my_stepSnowbiom():
    return StepSnowbiom(100,1)

def test_initialization_of_StepTemplate(my_stepTemplate):
    assert my_stepTemplate.tall == my_stepTemplate.width == my_stepTemplate.height == my_stepTemplate.biom_id == 0
    assert my_stepTemplate.topLeft == [0,0]
    assert my_stepTemplate.number == 1

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

