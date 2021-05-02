from onvif import ONVIFCamera




def do_move(ptz, request):
    # Start continuous move
    global active
    if active:
        ptz.Stop({'ProfileToken': request.ProfileToken})
    active = True
    ptz.ContinuousMove(request)




# Create the media service
mycam = ONVIFCamera('192.168.13.100', 8080, 'admin', '215802')
media_service = mycam.create_media_service()


# Get Hostname
resp = mycam.devicemgmt.GetHostname()
print('My camera`s hostname: ' + str(resp.Name))


# Create ptz service
ptz = mycam.create_ptz_service()


# Get target profile
media_profile = media_service.GetProfiles()[0]


ptz.Stop({'ProfileToken': media_profile._token})
