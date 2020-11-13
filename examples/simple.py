#!/usr/bin/env python3
import cavaliercontours as cavc

vertex_data = [[45., 30., 10., 10., 0., 0., 45.], # x
               [20., 35., 35., 50., 50., 0., 0.], # y
               [0.41421, 0., 0., 0., 0., 0., 0.]] # bulge

polyline = cavc.Polyline(vertex_data, is_closed=True)

print('is_closed\t:', polyline.is_closed())
print('vertex_count\t:', polyline.vertex_count())
print('path_length\t:', polyline.get_path_length())
print('area\t\t:', polyline.get_area())

point = (10., 20.)
print('winding_number\t:', polyline.get_winding_number(point))
print('extents\t\t:', polyline.get_extents())
point = (50., 40.)
print('closest_point\t:', polyline.get_closest_point(point))

polyline_list = polyline.parallel_offset(delta=-3.0, check_self_intersect=False)
print('offset get_area\t:', polyline_list[0].get_area())
print('offset vertex_data:\n', polyline_list[0].vertex_data())

# combine_plines(self, other, combine_mode)
