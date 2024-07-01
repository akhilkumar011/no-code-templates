from django.http import JsonResponse,HttpResponse
from django.shortcuts import render 
from django.views.decorators.csrf import csrf_exempt
from .models import Business, ModuleField,Menu
import json
import uuid
from datetime import datetime
from bson import ObjectId
from pymongo import MongoClient



client = MongoClient('localhost', 27017)
db = client['Hb_ERP_Utility']

def to_camel_case(snake_str):
    components = snake_str.split(' ')
    return components[0].lower() + ''.join(x.title() for x in components[1:])

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

@csrf_exempt
def create_module(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        module_title = data.get('title')
        dynamic_fields = data.get('fields', [])

        if not module_title:
            return JsonResponse({'error': 'Module title is required'}, status=400)

        custom_field = ModuleField(
            businessId="some_business_id", 
            module=module_title,
            dynamicFields=dynamic_fields,
            createdAt=datetime.now()
        )
        custom_field.save()
        return JsonResponse({'status': 'success'})

    return JsonResponse({'error': 'Invalid request method'}, status=405)


def show_modules(request):
    pipeline = []
    modules = list(ModuleField().aggregate_raw(pipeline))
    for module in modules:
        if '_id' in module:
            module['id'] = str(module.pop('_id'))
    return JsonResponse({'data': modules})


def edit_module(request, module_id):
    try:
        module_object_id = ObjectId(module_id)
    except Exception as e:
        return HttpResponse("Invalid module ID", status=400)
    
    pipeline = [
        {'$match': {'_id': module_object_id}}
    ]
    modules = list(ModuleField().aggregate_raw(pipeline))
    
    if not modules:
        return HttpResponse("Module not found", status=404)
    
    module = modules[0]
    if '_id' in module:
        module['id'] = str(module.pop('_id'))

    if request.method == 'PUT':
        module_title = request.put.get('module_title')
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
        ModuleField().update_by_query_data(query, data)

    return JsonResponse({'status': 'success'}, status=200)

@csrf_exempt
def create_module_entry(request, module_id):
    try:
        module_object_id = ObjectId(module_id)
    except Exception as e:
        return HttpResponse("Invalid module ID", status=400)
    
    pipeline = [
        {'$match': {'_id': module_object_id}}
    ]
    modules = list(ModuleField().aggregate_raw(pipeline))
    
    if not modules:
        return HttpResponse("Module not found", status=404)

    module = modules[0]
    if '_id' in module:
        module['id'] = str(module.pop('_id'))

    dynamic_fields = module.get('dynamicFields', [])

    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            return HttpResponse("Invalid JSON data", status=400)
        
        module_data = {}
        for field in dynamic_fields:
            field_name = field.get('name')
            field_type = field.get('type')
            field_value = data.get(field_name)  # Get value from JSON payload
            camel_case_name = to_camel_case(field_name)

            if field_type == 'number':
                if field_value is not None:
                    try:
                        field_value = float(field_value)
                    except ValueError:
                        return HttpResponse(f"Invalid input for field {field_name}: expected a number.", status=400)

            module_data[camel_case_name] = field_value

        # Add moduleReferenceID to the entry data
        module_data['moduleReferenceID'] = module_id

        db[module['module']].insert_one(module_data)
        return JsonResponse({'status': 'success'}, status=200)


@csrf_exempt
def view_entries(request,module_id):
    try:
        module_object_id = ObjectId(module_id)
    except Exception as e:
        return HttpResponse("Invalid module ID", status=400)

    pipeline = [
        {'$match': {'_id': module_object_id}}
    ]
    modules = list(ModuleField().aggregate_raw(pipeline))

    
    if not modules:
        return HttpResponse("Module not found", status=404)

    module = modules[0]
    if '_id' in module:
        module['id'] = str(module.pop('_id'))

    entries = list(db[module['module']].find({'moduleReferenceID': module_id}))
    entries_data = {}    

    for entry in entries:
        entry['id'] = str(entry['_id'])
        del entry['_id']
    entries_data['entries'] = entries
    entries_data['module'] = module

    return JsonResponse({'entriesData': entries_data}, status=200)

@csrf_exempt
def update_module_entry(request, module_id):
    if request.method == 'PUT':        
        data = json.loads(request.body.decode('utf-8'))
        collection_name = data.get('collectionName')
        entry_id = data.get('id')
        entry_object_id = ObjectId(entry_id)
        
        module_data = {k: v for k, v in data.items() if k != 'id' }
        del module_data['collectionName']

        result = db[collection_name].update_one(
            {'_id': entry_object_id},
            {'$set': module_data}
        )
        
        if result.matched_count:
            return JsonResponse({'status': 'success'}, status=200)
    else:
        return HttpResponse("Invalid request method", status=405)
    
@csrf_exempt
def get_module_data(request, module_id):
    try:
        module_object_id = ObjectId(module_id)
    except Exception as e:
        return HttpResponse("Invalid module ID", status=400)
    
    pipeline = [
        {'$match': {'_id': module_object_id}}
    ]
    modules = list(ModuleField().aggregate_raw(pipeline))
    
    if not modules:
        return HttpResponse("Module not found", status=404)
    
    module = modules[0]
    if '_id' in module:
        module['id'] = str(module.pop('_id'))

    return JsonResponse(module)

@csrf_exempt
def create_menu(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        menu_name = data.get("name")
        
        if not menu_name:
            return JsonResponse({'error': 'Menu title is required'}, status=400)
        menu_data: Menu = Menu(**data)
        menu_data.created_at =datetime.now()
        menu_data.save()
        return JsonResponse({'message': 'Menu created successfully'}, status=200)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def get_menus(request):
    pipeline = []
    modules = list(Menu().aggregate_raw(pipeline))
    for module in modules:
        if '_id' in module:
            module['id'] = str(module.pop('_id'))
    return JsonResponse({'data': modules})