from django.db import connection
from company.models import Company


def hostname_from_request(request):
    # split on `:` to remove port
    return request.get_host().split(":")[0].lower()


def tenant_schema_from_request(request):
    hostname = hostname_from_request(request) 
    schema = hostname.split(".")[0].lower()
    return schema

    '''
    if hostname == "www.wisemen":
        return "www"
    else:
        tenants_map = get_tenants_map()
        print(tenants_map)
        return tenants_map.get(hostname)
    '''

def set_tenant_schema_for_request(request):
    schema = tenant_schema_from_request(request)
    
    with connection.cursor() as cursor:
        cursor.execute(f"SET search_path to {schema}")
    

def get_tenants_map():     
    return dict(Company.objects.values_list('company_host', 'company_domain')) 
