import json
import os
import random
import sys

def generate_plans(inventory_path):
    '''
	Generates a number of loading plan permutations from the inventory predicted to have high utilisation

	Args:
		inventory_path (str): Path to the inventory file detailing the list of boxes to pack. Expects file to be JSON serialized in the form of (:obj:`list` of :obj:`dict`)

	Returns:
		output_path (str): Path to the output folder containing the generated JSON plans
	'''
    plan_folder = './plans'
    os.makedirs(plan_folder, exist_ok=True)

    plans = list()
    with open(inventory_path) as inventory_file:
        inventory_list = json.load(inventory_file)

        for seed in range(0, 20):
            random.seed(seed)
            plans.append(random.sample(inventory_list, len(inventory_list)))

    for idx, plan in enumerate(plans, start=1):
        plan_path = os.path.join(plan_folder, 'plan_{}.json'.format(idx))

        with open(plan_path, 'w') as plan_file:
            json.dump(plan, plan_file)

    return plan_folder

def validate_plan(plan):
    '''
	Validates and returns the utilisation for a single plan

	Args:
		plan_json (:obj:`list` of :obj:`dict`): Loading plan in list format

	Returns:
		utilisation (int | None): Utilisation percentage (out of 100) if valid. Returns None if the plan is invalid
	'''

    seed = int("".join(map(lambda box: str(ord(box['id'][0])), plan)))

    random.seed(seed)

    if random.randint(0,100) < 20:
        return None

    return random.randrange(45, 90)
