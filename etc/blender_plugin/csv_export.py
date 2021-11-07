

import os
import csv
import math

import bpy
from bpy_extras.io_utils import ExportHelper
from bpy.types import Operator
from bpy.props import StringProperty, BoolProperty, FloatProperty, IntProperty

bl_info = {
    "name": "csv exporter",
    "author": "",
    "version": (0, 5, 0),
    "blender": (2, 80, 0),
    "location": "File > Export > csv exporter (.csv)",
    "description": "Export > csv exporter (.csv)",
    "warning": "",
    "category": "Import-Export"
}


class ExportCsv(Operator, ExportHelper):
    bl_idname = "export_animation.folder"
    bl_label = "csv exporter"
    filename_ext = ''
    use_filter_folder = True

    obj_name: bpy.props.StringProperty(
        name="Name identifier",
        description="Name identifier for obj",
        default="test"
    )

    filepath: StringProperty(
        name="File Path",
        description="File path used for exporting csv files",
        maxlen=1024,
        subtype='DIR_PATH',
        default=""
    )

    def execute(self, context):

        create_folder_if_does_not_exist(self.filepath)
        scene = context.scene
        objects = context.visible_objects

        obj = ([None] + [i for i in objects if i.name == self.obj_name])[-1]

        frame_start = scene.frame_start
        frame_end = scene.frame_end

        if obj is None:
            self.report({'ERROR'}, "Object '%s' not found" % obj.name)
            return {'FINISHED'}

        with open(os.path.join(self.filepath, '{}.csv'.format(obj.name.lower())), 'w') as csv_file:
            animation_file_writer = csv.writer(
                csv_file,
                delimiter=',',
                quotechar='|',
                quoting=csv.QUOTE_MINIMAL
            )

            animation_file_writer.writerow([
                os.path.splitext(bpy.path.basename(bpy.data.filepath))[0]
            ])

            for frame_number in range(frame_start, frame_end + 1):
                scene.frame_set(frame_number)
                x, y, z = obj.matrix_world.to_translation()
                rot_x, rot_y, rot_z = obj.matrix_world.to_euler('XYZ')

                animation_file_writer.writerow([
                    str(frame_number),
                    round(x, 5), round(y, 5), round(z, 5),
                    round(rot_x, 5), round(rot_y, 5), round(rot_z, 5)
                ])

            self.report({'WARNING'}, "Animation file exported for drone '%s'" % obj.name)
        return {'FINISHED'}


def create_folder_if_does_not_exist(folder_path):
    if os.path.isdir(folder_path):
        return
    os.mkdir(folder_path)


def menu_func(self, context):
    self.layout.operator(
        ExportCsv.bl_idname,
        text="csv exporter (.csv)"
    )


def register():
    bpy.utils.register_class(ExportCsv)
    bpy.types.TOPBAR_MT_file_export.append(menu_func)


def unregister():
    bpy.utils.unregister_class(ExportCsv)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func)


if __name__ == "__main__":
    register()