import adsk.core, adsk.fusion, traceback, math, os
from .lib import fusionAddInUtils as futil

handlers = []

def roll_camera(degrees):
    app = adsk.core.Application.get()
    viewport = app.activeViewport
    cam = viewport.camera

    view_axis = cam.eye.vectorTo(cam.target)
    view_axis.normalize()

    rot_matrix = adsk.core.Matrix3D.create()
    rot_matrix.setToRotation(math.radians(degrees), view_axis, adsk.core.Point3D.create(0, 0, 0))

    new_up = cam.upVector.copy()
    new_up.transformBy(rot_matrix)

    cam.upVector = new_up
    cam.isSmoothTransition = True
    viewport.camera = cam

class RollExecuteHandler(adsk.core.CommandEventHandler):
    def __init__(self, angle):
        super().__init__()
        self.angle = angle

    def notify(self, args):
        try:
            roll_camera(self.angle)
        except:
            futil.handle_error('RollExecuteHandler')

class RollCreatedHandler(adsk.core.CommandCreatedEventHandler):
    def __init__(self, angle):
        super().__init__()
        self.angle = angle

    def notify(self, args):
        cmd = args.command
        on_execute = RollExecuteHandler(self.angle)
        cmd.execute.add(on_execute)
        handlers.append(on_execute)

def run(context):
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface

        addin_dir = os.path.dirname(os.path.realpath(__file__))
        res_dir = os.path.join(addin_dir, 'resources')

        commands = [
            ('Roll45CCW', 'Roll View 45° CCW', 'Rotates the active view 45 degrees counter-clockwise.', 45, os.path.join(res_dir, 'CCW')),
            ('Roll45CW', 'Roll View 45° CW', 'Rotates the active view 45 degrees clockwise.', -45, os.path.join(res_dir, 'CW'))
        ]

        nav_toolbar = ui.toolbars.itemById('NavToolbar')
        inspect_panel = ui.allToolbarPanels.itemById('InspectPanel')

        for cmd_id, name, tooltip, angle, icon_folder in commands:
            if nav_toolbar:
                old_nav = nav_toolbar.controls.itemById(cmd_id)
                if old_nav:
                    old_nav.deleteMe()
            if inspect_panel:
                old_insp = inspect_panel.controls.itemById(cmd_id)
                if old_insp:
                    old_insp.deleteMe()

            existing = ui.commandDefinitions.itemById(cmd_id)
            if existing:
                existing.deleteMe()

            cmd_def = ui.commandDefinitions.addButtonDefinition(cmd_id, name, tooltip, icon_folder)
            on_created = RollCreatedHandler(angle)
            cmd_def.commandCreated.add(on_created)
            handlers.append(on_created)

            if nav_toolbar:
                nav_toolbar.controls.addCommand(cmd_def)

            if inspect_panel:
                ctrl = inspect_panel.controls.addCommand(cmd_def)
                ctrl.isPromoted = False
                ctrl.isPromotedByDefault = False
    except:
        futil.handle_error('run', show_message_box=True)

def stop(context):
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        nav_toolbar = ui.toolbars.itemById('NavToolbar')
        inspect_panel = ui.allToolbarPanels.itemById('InspectPanel')

        for cmd_id in ['Roll45CCW', 'Roll45CW']:
            if nav_toolbar:
                ctrl = nav_toolbar.controls.itemById(cmd_id)
                if ctrl:
                    ctrl.deleteMe()
            if inspect_panel:
                ctrl = inspect_panel.controls.itemById(cmd_id)
                if ctrl:
                    ctrl.deleteMe()
            cmd_def = ui.commandDefinitions.itemById(cmd_id)
            if cmd_def:
                cmd_def.deleteMe()
    except:
        futil.handle_error('stop')
