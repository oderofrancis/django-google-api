from django.conf import settings
from django.shortcuts import redirect
from urllib.parse import urlencode
import requests
import json
import datetime
from humanfriendly import format_timespan
from django.http import JsonResponse

# Create your mixins here.

def FormErrors(*args):
    '''
    This function handles form error that are passed back to AJAX calls
    '''
    message = ""
    for f in args:
        if f .errors:
            message += f .errors.as_text()
    return message

def get_captcha_score(token):
    '''
   reCaptch validation
    '''
    
    results = requests.post(
        'https://www.google.com/recaptcha/api/siteverify',
        data={
            'secret': settings.RECAPTCHA_SECRET_KEY,
            'response': token
        }
    )
    results = json.loads(results.text)

def reCAPTCHAValidation(**kwargs):
    '''
    This function handles redirecting with parameters
    '''
    url = kwargs.get('url')
    params = kwargs.get('params')
    response = redirect(url)

    if params:
        query_string = urlencode(params)
        response['Location'] += '?' + query_string
    return response

class AjaxFormMixin(object):
    '''
    This mixin handles form validation for AJAX calls
    '''
    def form_invalid(self, form):
        response = super(AjaxFormMixin, self).form_invalid(form)
        if self.request.is_ajax():
            message = FormErrors(form)
            return JsonResponse({'success': False, 'message': message})
        return response

    def form_valid(self, form):
        response = super(AjaxFormMixin, self).form_valid(form)
        if self.request.is_ajax():
            form.save()
            return JsonResponse({'results': 'success', 'message': 'Form submitted successfully'})
        return response

def Directions(**args):
    '''
    This function handles the directions between two locations from Google
    '''
    lat_a = args.get('lat_a')
    lon_a = args.get('lon_a')
    lat_b = args.get('lat_b')
    lon_b = args.get('lon_b')
    # lat_c = args.get('lat_c')
    # lon_c = args.get('lon_c')
    # lat_d = args.get('lat_d')
    # lon_d = args.get('lon_d')

    origin = f'{lat_a},{lon_a}'
    destination = f'{lat_b},{lon_b}'
    # waypoints = f'{lat_c},{lon_c}|{lat_d},{lon_d}'

    results = requests.get(
        'https://maps.googleapis.com/maps/api/directions/json',
        params={
            'origin': origin,
            'destination': destination,
            # 'waypoints': waypoints,
            'key': settings.GOOGLE_MAPS_API_KEY
        }
    )

    directions = results.json()
    if directions['status'] == 'OK':
        routes = directions['routes'][0]['legs']
        distance = 0
        duration = 0

        for route in range(len(routes)):
            distance += int(routes[route]['distance']['value'])
            duration += int(routes[route]['duration']['value'])

            route_steps ={
                'origin': routes[route]['start_address'],
                'destination': routes[route]['end_address'],
                'distance': routes[route]['distance']['text'],
                'duration': routes[route]['duration']['text'],

                # 'waypoints': waypoints,

                'steps': [
                    [
                        step['html_instructions'],
                        step['distance']['text'],
                        step['duration']['text']
                    ] 
                    for step in routes[route]['steps']
                ]
                
            }
    return {
        'origin': origin,
        'destination': destination,
        'distance': f"{round(distance/1000, 2)} km",
        'duration': format_timespan(duration),
        'route_steps': route_steps
    }