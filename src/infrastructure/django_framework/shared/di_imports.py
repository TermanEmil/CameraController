# Imports used by pinject


# noinspection PyUnresolvedReferences
def pinject_imports():
    import business.camera.ctrl.autodetect_bl_rule
    import business.camera.ctrl.get_all_cameras_bl_rule
    import business.camera.ctrl.get_camera_bl_rule
    import business.camera.ctrl.remove_bl_rule
    import business.camera.ctrl.reconnect_bl_rule
    import business.camera.ctrl.capture_img_and_download_bl_rule
    import business.camera.ctrl.capture_preview_bl_rule

    import business.camera.config.get_all_config_names_bl_rule
    import business.camera.config.get_config_bl_rule
    import business.camera.config.set_config_bl_rule
    import business.camera.config.get_all_configs_bl_rule

    import business.scheduling.scheduling_startup_bl_rule
    import business.scheduling.timelapse_bl_rules
    import business.scheduling.cron_bl_rules

    import business.timelapse.get_timelapse_func_bl_rule

    import adapters.camera.ctrl.camera_ctrl_service
    import adapters.camera.configs.camera_config_service