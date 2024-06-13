from django.http import JsonResponse,HttpResponse
from django.shortcuts import render ,redirect,get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .models import Business, CustomField
import json
import uuid
from datetime import datetime
from bson import ObjectId
from pymongo import MongoClient
from django.urls import reverse


client = MongoClient('localhost', 27017)
db = client['Hb_ERP_Utility']

@csrf_exempt
def create_business(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        business = Business(
            name=data['name'],
            description=data['description'],
            businessId= str(uuid.uuid4())
        )
        business.save()
        return JsonResponse({'status': 'success', 'businessId': str(business.businessId)})
    return render(request,'create_business.html')

def create_module(request):
    if request.method == 'POST':
        module_title = request.POST.get('module_title')
        if not module_title:
            return render(request, 'create_module.html', {'error': 'Module title is required'})

        dynamic_fields = []
        dynamic_field_keys = [key for key in request.POST.keys() if key.startswith('dynamic_field')]
        field_pairs = set('_'.join(field.split('_')[:3]) for field in dynamic_field_keys)

        for pair in field_pairs:
            field_name = request.POST.get(f'{pair}_name')
            field_type = request.POST.get(f'{pair}_type')

            field_entry = {
                'name': field_name,
                'type': field_type
            }
            dynamic_fields.append(field_entry)

        # Save data using CustomField
        custom_field = CustomField(
            businessId="some_business_id",  # Replace with actual businessId
            module=module_title,
            dynamicFields=dynamic_fields,
            createdAt=datetime.now()
        )
        custom_field.save()
        return redirect('show_modules')
    return render(request, 'create_module.html')

def show_modules(request):
    pipeline = []
    modules = list(CustomField().aggregate_raw(pipeline))
    for module in modules:
        if '_id' in module:
            module['id'] = str(module.pop('_id'))
    return render(request, 'show_modules.html', {'modules': modules})


def edit_module(request, module_id):
    try:
        module_object_id = ObjectId(module_id)
    except Exception as e:
        return HttpResponse("Invalid module ID", status=400)
    
    pipeline = [
        {'$match': {'_id': module_object_id}}
    ]
    modules = list(CustomField().aggregate_raw(pipeline))
    
    if not modules:
        return HttpResponse("Module not found", status=404)
    
    module = modules[0]
    if '_id' in module:
        module['id'] = str(module.pop('_id'))

    if request.method == 'POST':
        module_title = request.POST.get('module_title')
        if not module_title:
            return render(request, 'edit_module.html', {'module': module, 'error': 'Module title is required'})

        dynamic_fields = []
        dynamic_field_keys = [key for key in request.POST.keys() if key.startswith('dynamic_field')]
        field_pairs = set('_'.join(field.split('_')[:3]) for field in dynamic_field_keys)

        for pair in field_pairs:
            field_name = request.POST.get(f'{pair}_name')
            field_type = request.POST.get(f'{pair}_type')

            field_entry = {
                'name': field_name,
                'type': field_type,
            }
            dynamic_fields.append(field_entry)

        query = {'_id': module_object_id}
        data =  {'$set': {
                'module': module_title,
                'dynamicFields': dynamic_fields,
                'createdAt': datetime.now()
            }}
        # Update data using CustomField
        CustomField().update_by_query_data(query, data)
        return redirect('show_modules')

    return render(request, 'edit_module.html', {'module': module})


def create_module_entry(request, module_id):
    try:
        module_object_id = ObjectId(module_id)
    except Exception as e:
        return HttpResponse("Invalid module ID", status=400)
    
    pipeline = [
        {'$match': {'_id': module_object_id}}
    ]
    modules = list(CustomField().aggregate_raw(pipeline))
    
    if not modules:
        return HttpResponse("Module not found", status=404)

    module = modules[0]
    if '_id' in module:
        module['id'] = str(module.pop('_id'))

    # Ensuring dynamicFields is accessed correctly from the module dictionary
    dynamic_fields = module.get('dynamicFields', [])

    if request.method == 'POST':
        module_data = {}
        for field in dynamic_fields:
            field_name = field.get('name')
            field_type = field.get('type')
            field_value = request.POST.get(field_name)

            if field_type == 'number':
                try:
                    field_value = float(field_value)
                except ValueError:
                    return HttpResponse(f"Invalid input for field {field_name}: expected a number.", status=400)

            module_data[field_name] = field_value
        
        db[module['module']].insert_one(module_data)
        return redirect('show_modules')

    return render(request, 'create_module_entry.html', {'module': module, 'dynamicFields': dynamic_fields})