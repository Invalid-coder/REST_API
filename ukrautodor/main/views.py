from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import *
from .trie import *
import time

start_time = time.time()
data = pd.read_csv("main/WIM_vehicles_search.csv")
mapping = dict()
numbers = list(map(str, data['govNumber_plate']))

for id, number in zip(data['Id'], numbers):
    mapping[number] = id

tree = Trie(mapping)
tree.build(numbers)

print("time elapsed: {:.2f}s".format(time.time() - start_time))

@csrf_exempt
def index(request):
    if 'rebuildTree' in request.POST and request.POST['rebuildTree']:
        done = True
        return JsonResponse({'RefreshedTree': done})

    number = ''
    func = 'autocomplete'
    found_numbers = []
    form = UserForm(request.POST or None)

    if request.method == "POST":
        func = request.POST["options"]
        if form.is_valid():
            number = form.cleaned_data.get("number")
            found_numbers = tree.execute(func, number)

    if 'from_postman' in request.POST and request.POST['from_postman']:
        return JsonResponse({'numbers': found_numbers})
    else:
        context = {'form': form,
                   'numbers': found_numbers,
                   }
        return render(request, 'main/index.html', context)


def about(request):
    return render(request, 'main/about.html')