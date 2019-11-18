from django.shortcuts import render
from .algorithm import generate_plans
from .businesslogic import calculate_utilisation, optimal_plan
import os
import json


def home_view(request, *args, **kwargs):
	#This is the home page.
	return render(request, "home.html", {})


def result_view(request, *args, **kwargs):
	'''
	After user submitting the document, the application redirects to the result display page.

	Before rendering the optimal loading plan result, business logic functions are implemented to
	calculate the result.
	'''

	#The application create the "/inventory" directory to store the inventory file in json format. 
	inventory_folder = './inventory'
	os.makedirs(inventory_folder, exist_ok=True)
	inventory_json = []

	if request.method == 'POST' and request.FILES['user_file']:
		#Retrieve data from the .txt format file, and save the result in inventory_list. 
		user_file = request.FILES['user_file']
		file_data = user_file.read().decode()
		inventory_list = file_data.split()

		#Remove "id,weight,dimensions" from the list.
		inventory_list.pop(0)

		#Save the inventory information in json format.          
		for each in inventory_list:
			each = each.split(',')
			item = {'id': each[0], 'weight': each[1], 'dimensions': each[2] }
			inventory_json.append(item)


		inventory_path = os.path.join(inventory_folder, 'inventory.json')
		with open(inventory_path, 'w') as inventory_file:
			json.dump(inventory_json, inventory_file)

		#This is the black box function, no changes were made. json file path is generated.
		output_path = generate_plans(inventory_path)

		'''
		This function generate two values. 
		optimal_plan_utilisation is the Utilisation percentage (out of 100)
		plans includes all valid loading plans.
		'''
		optimal_plan_utilisation, plans = calculate_utilisation(output_path)

		'''
		This function generate the params for the optimal loading plan. 
		Order sequence, total weight and total volume are inculded.
		'''
		optimal_plan_list = optimal_plan(optimal_plan_utilisation, plans)

		
	return render(request, "result.html", {"plans":optimal_plan_list, "utilisation":optimal_plan_utilisation})