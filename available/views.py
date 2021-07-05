from django.shortcuts import render
from django.views.generic import TemplateView, CreateView
from .forms import LocationForm, DistrictForm
import requests, json
from find_availability import AvailableSlots


def form_handle(request):
    form = LocationForm()
    state = ""
    print("state : ", request.method)
    if request.method == 'POST':
        form = LocationForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            cd = form.cleaned_data
            print(form.cleaned_data)
            # now in the object cd, you have the form as a dictionary.
            state = cd.get('state')
            return state
    return state
    # blah blah encode parameters for a url blah blah
    # and make another post request


def load_districts(request):
    if request.method == 'GET':
        state_form = LocationForm(request.GET)
        print(state_form.is_valid())
        if state_form.is_valid():
            state_data = state_form.cleaned_data
            state_id = state_data.get('state')
            URL = "https://cdn-api.co-vin.in/api/v2/admin/location/districts/{}".format(state_id)
            PARAMS = {"state_id": state_id}
            headers = {
                "accept": 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                "accept-language": 'en-US,en;q=0.9',
                "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 Edg/90.0.818.56',
            }
            res = requests.get(url=URL, params=PARAMS, headers=headers)
            list_of_districts = json.loads(res.content.decode())['districts']
            return render(request, 'available/districts_dropdown_options.html', {'districts': list_of_districts})
    elif request.method == "POST":
        print(request.__dict__)
    return render(request, 'available/districts_dropdown_options.html', {})


def load_slots(request, *args, **kwargs):
    district_id = request.POST.get('district')
    return render(request, 'available/districts_dropdown_options.html', {})


class Availability(CreateView):

    def get(self, request, *args, **kwargs):
        # import pdb
        # pdb.set_trace()
        form_class = LocationForm
        URL = "https://cdn-api.co-vin.in/api/v2/admin/location/states"
        PARAMS = {}
        headers = {
            "accept": 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            "accept-language": 'en-US,en;q=0.9',
            "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 Edg/90.0.818.56',
        }
        res = requests.get(url=URL, params=PARAMS, headers=headers)
        list_of_dicts = json.loads(res.content.decode())['states']
        return render(request, 'available/index.html', {"items": list_of_dicts})
