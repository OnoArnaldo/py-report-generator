# pylint: disable=unused-variable
import os
from reportlab.lib import pagesizes
from reportlab.lib.units import cm
from reportgen.elements import Image
from ..utils import Ignore

ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
ASSETS_DIR = os.path.join(ROOT_DIR, 'assets')


def assets(image):
    return os.path.join(ASSETS_DIR, image)


def test_image(canvas):
    img = Image(canvas).parent_size(*pagesizes.A4).parent_position(0, 0).margin(cm).filename(assets('150.png')).draw()

    assert object.__getattribute__(canvas, 'log') == [
        [
            'canvas/drawImage(..)',
            (Ignore, 28.346456692913385, 28.346456692913385, 538.5826771653544, 785.196850393701),
            {'preserveAspectRatio': True},
        ]
    ]
