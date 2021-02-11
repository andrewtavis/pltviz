"""
Utilities Tests
-----------
"""

from colormath.color_objects import sRGBColor

from pltviz import utils


def test_round_if_int():
    assert utils.round_if_int(2.0) == 2


def test_add_num_commas():
    assert utils.add_num_commas(1234) == "1,234"
    assert utils.add_num_commas(1234.5) == "1,234.5"


def test_gen_list_of_lists():
    test_list = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    assert utils.gen_list_of_lists(
        original_list=test_list, new_structure=[3, 3, 3]
    ) == [[0, 1, 2], [3, 4, 5], [6, 7, 8]]


def test_hex_to_rgb():
    assert utils.hex_to_rgb("#ffffff").get_value_tuple() == (1.0, 1.0, 1.0)


def test_rgb_to_hex():
    assert utils.rgb_to_hex((1, 1, 1)) == "#ffffff"


def test_scale_saturation():
    assert utils.scale_saturation((1, 1, 1), 0.95) == (0.95, 0.95, 0.95)


def test_create_color_palette():
    start_rgb = utils.hex_to_rgb("#ffffff")
    end_rgb = utils.hex_to_rgb("#000000")
    num_colors = 10
    assert (
        len(
            utils.create_color_palette(
                start_rgb=start_rgb,
                end_rgb=end_rgb,
                num_colors=num_colors,
                colorspace=sRGBColor,
            )
        )
        == num_colors
    )


def test_gen_random_colors(white_black_hexes):
    num_groups = 10
    assert (
        len(utils.gen_random_colors(num_groups=num_groups, colors=white_black_hexes))
        == num_groups
    )
