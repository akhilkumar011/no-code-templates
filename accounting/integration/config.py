from util.app_enum import Environment

BASE_URLS = {
    Environment.PRODUCTION: 'https://erp.example.com',
    Environment.SANDBOX: 'https://staging.erp.example.com',
    Environment.STAGING: 'https://staging.erp.example.com',
    Environment.DEVELOPMENT: 'http://localhost:8080/api'
}
headers = {
    'Content-Type': 'application/json',
    'x-auth-token': '6fb50c12afb2eff0d5aa348ca81dff1212',
    'x-company': 'DF5EE3EC-F3DA-D79D-C1D9-60AF5915BD22'
}
ADD_MASTER = '/master/add'
LIST_MASTER = '/master/list'
ADD_TRANSACTION = '/transaction/add'
LIST_TRANSACTION = '/transaction/list'
