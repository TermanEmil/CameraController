# Imports used by pinject


# noinspection PyUnresolvedReferences
def pinject_imports():
    import business.camera.capture_img_and_download_bl_rule
    import business.camera.hard_reset_all_cameras_bl_rule

    import business.scheduling.scheduling_startup_bl_rule
    import business.scheduling.timelapse_bl_rules
    import business.scheduling.cron_bl_rules

    import business.timelapse.get_timelapse_func_bl_rule
    import business.file_transfer.file_transfer_manager

    import business.app_logging.log_manager

    import adapters.camera.ctrl.camera_ctrl_service
    import adapters.camera.configs.camera_config_service
    import adapters.scheduling.schedule_service
    import adapters.scheduling.event_listeners
    import adapters.file_transfer.file_transfer_service
    import adapters.file_transfer.event_listeners
    import adapters.emailing.email_service

    import camera_ctrl.startup
