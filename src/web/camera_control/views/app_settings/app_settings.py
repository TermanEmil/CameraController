from django.shortcuts import render, redirect


def app_settings(request):
    # return render(request, 'camera_control/app_settings/app_settings.html')
    return redirect('settings/favourite_configs_profiles')
