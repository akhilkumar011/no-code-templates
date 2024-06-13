from django.http import JsonResponse,HttpResponse
from django.shortcuts import render ,redirect
from django.views.decorators.csrf import csrf_exempt
from .models import Business, CustomField,DESIGN_NAMES
import json
import uuid
import os
from django.template.loader import render_to_string,get_template
from django.template import Engine, Context
from datetime import datetime
from bson import ObjectId

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
            return render(request, 'leads/create_module.html', {'error': 'Module title is required'})

        # Handling dynamic fields
        dynamic_fields = []
        dynamic_field_keys = [key for key in request.POST.keys() if key.startswith('dynamic_field')]
        field_pairs = set('_'.join(field.split('_')[:3]) for field in dynamic_field_keys)

        for pair in field_pairs:
            field_name = request.POST.get(f'{pair}_name')
            field_type = request.POST.get(f'{pair}_type')
            field_value = request.POST.get(f'{pair}_value')

            field_entry = {
                'name': field_name,
                'type': field_type,
                'value': field_value
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
    print(modules,">>>>>>>>>>")
    return render(request, 'show_modules.html', {'modules': modules})

# def edit_module(request):
#     pipeline = []
#     modules = list(CustomField().aggregate_raw(pipeline))
#     for module in modules:
#         if '_id' in module:
#             module['id'] = str(module.pop('_id'))

#     if request.method == 'POST':
#         module_title = request.POST.get('module_title')
#         module_id = request.POST.get('id')
#         if not module_title:
#             return render(request, 'edit_module.html', {'module': modules, 'error': 'Module title is required'})

#         dynamic_fields = []
#         dynamic_field_keys = [key for key in request.POST.keys() if key.startswith('dynamic_field')]
#         field_pairs = set('_'.join(field.split('_')[:3]) for field in dynamic_field_keys)

#         for pair in field_pairs:
#             field_name = request.POST.get(f'{pair}_name')
#             field_type = request.POST.get(f'{pair}_type')
#             field_value = request.POST.get(f'{pair}_value')

#             field_entry = {
#                 'name': field_name,
#                 'type': field_type,
#                 'value': field_value
#             }
#             dynamic_fields.append(field_entry)

#         # Update data using CustomField
#         CustomField().update_one(
#             {'_id': module_id},
#             {'$set': {
#                 'module': module_title,
#                 'dynamicFields': dynamic_fields,
#                 'createdAt': datetime.now()
#             }}
#         )
#         return redirect('show_modules')

#     return render(request, 'edit_module.html', {'module': modules})

def edit_module(request, module_id):
    # Convert the string module_id to an ObjectId
    try:
        module_object_id = ObjectId(module_id)
    except Exception as e:
        return HttpResponse("Invalid module ID", status=400)
    
    # Create the aggregation pipeline with a match condition
    pipeline = [
        {'$match': {'_id': module_object_id}}
    ]
    modules = list(CustomField().aggregate_raw(pipeline))
    
    if not modules:
        return HttpResponse("Module not found", status=404)
    
    # Assume the first document is the one we want (since _id should be unique)
    module = modules[0]
    if '_id' in module:
        module['id'] = str(module.pop('_id'))

    if request.method == 'POST':
        module_title = request.POST.get('module_title')
        if not module_title:
            return render(request, 'leads/edit_module.html', {'module': module, 'error': 'Module title is required'})

        dynamic_fields = []
        dynamic_field_keys = [key for key in request.POST.keys() if key.startswith('dynamic_field')]
        field_pairs = set('_'.join(field.split('_')[:3]) for field in dynamic_field_keys)

        for pair in field_pairs:
            field_name = request.POST.get(f'{pair}_name')
            field_type = request.POST.get(f'{pair}_type')
            field_value = request.POST.get(f'{pair}_value')

            field_entry = {
                'name': field_name,
                'type': field_type,
                'value': field_value
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
