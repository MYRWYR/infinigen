# Copyright (c) Princeton University.
# This source code is licensed under the BSD 3-Clause license found in the LICENSE file in the root directory of this source tree.

# Authors: Lingjie Mei
from collections.abc import Iterable

import numpy as np
from numpy.random import uniform

from infinigen.assets.utils.object import new_plane
from infinigen.assets.utils.uv import unwrap_normal
from infinigen.core.util.color import hsv2rgba
from infinigen.core.nodes.node_info import Nodes
from infinigen.core.nodes.node_wrangler import NodeWrangler
from infinigen.assets.materials import common
from infinigen.core.util.random import log_uniform


def shader_plaster(nw: NodeWrangler, plaster_colored, **kwargs):
    hue = uniform(0, 1)
    front_value = log_uniform(.5, 1.)
    back_value = front_value * uniform(.6, 1)
    if plaster_colored:
        front_color = hsv2rgba(hue, uniform(.3, .5), front_value)
        back_color = hsv2rgba(hue + uniform(-.1, .1), uniform(.3, .5), back_value)
    else:
        front_color = hsv2rgba(hue, 0, front_value)
        back_color = hsv2rgba(hue + uniform(-.1, .1), 0, back_value)
    uv_map = nw.new_node(Nodes.UVMap)
    musgrave = nw.new_node(Nodes.MusgraveTexture, [uv_map],
                           input_kwargs={'Detail': log_uniform(15, 30), 'Dimension': 0})
    noise = nw.new_node(Nodes.NoiseTexture, [uv_map],
                        input_kwargs={'Detail': log_uniform(15, 30), 'Distortion': log_uniform(4, 8)})
    difference = nw.new_node(Nodes.MixRGB, [musgrave, noise], attrs={'blend_type': 'DIFFERENCE'})
        'Height': nw.new_node(Nodes.MusgraveTexture, input_kwargs={'Scale': uniform(1e3, 2e3)})
    })
    principled_bsdf = nw.new_node(Nodes.PrincipledBSDF, input_kwargs={
        'Base Color': base_color,
        'Roughness': uniform(.7, .8),
    })


def apply(obj, selection=None, plaster_colored=None, **kwargs):
    if plaster_colored is None:
        plaster_colored = uniform() < .4
    for o in obj if isinstance(obj, Iterable) else [obj]:
        unwrap_normal(o, selection)
    common.apply(obj, shader_plaster, selection, plaster_colored=plaster_colored, **kwargs)


