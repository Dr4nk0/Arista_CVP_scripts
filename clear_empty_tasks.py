from cvprac.cvp_client import CvpClient
import os
import urllib3

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Retrieving Authentication Credentials
USERNAME : str = os.getenv('CVP_USERNAME')
PASSWORD : str = os.getenv('CVP_PASSWORD')
CVP_SERVER : str = os.getenv('CVP_HOSTNAME')

# Connecting to the CVP client
client = CvpClient()
client.connect([CVP_SERVER], username=USERNAME, password=PASSWORD)

# Retrieve the complete list of tasks by filtering for those with a "Pending" status.
full_task_list = client.api.get_tasks_by_status(status='Pending')

empty_tasks : list = []

for task in full_task_list :
    
    # Retrieve the compliance code of the device to which the task is applied (since only one task can be assigned to a device at a time).
    net_element_compliance_code = client.api.check_compliance(node_key=task['data']['NETELEMENT_ID'], node_type="netelement")
    
    print (f"Task ID : {task['workOrderId']} on NETELEMENT_ID : {task['data']['NETELEMENT_ID']} and compliance code is : {net_element_compliance_code['complianceCode']}")
    
    # Add the IDs of all empty tasks to a list.
    if net_element_compliance_code['complianceCode'] == '0000' : empty_tasks.append(task['workOrderId'])
    
if empty_tasks : 
    
    for task in empty_tasks : 
        
        # Send a request to cancel the task.
        result = client.api.cancel_task(task_id=task)
        print (f"Task ID : {task} cancellation result : {result['data']}")
