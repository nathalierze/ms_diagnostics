from scipy.stats import chisquare
from .models import schueler
from django.core import serializers
import json
import logging

logging.basicConfig(filename='sample_ratio_mismatch.log', level=logging.INFO, force=True)

def sample_ratio_mismatch():
    
    schuelers = schueler.objects.all()
    serialized = serializers.serialize("json", schuelers, fields=('ID,interventiongroup'))
    user_data = json.loads(serialized)

    group_1,group_2,group_3,group_4,group_5,group_6 = 0,0,0,0,0,0
    for x in user_data:
        interventiongroup = x['fields']['interventiongroup']

        if interventiongroup=='1':
            group_1 = group_1+1
        elif interventiongroup=='2':
            group_2= group_2+1
        elif interventiongroup=='3':
            group_3=group_3+1
        elif interventiongroup=='4':
            group_4=group_4+1
        elif interventiongroup=='5':
            group_5=group_5+1
        elif interventiongroup=='6':
            group_6=group_6+1
    
    total_number_of_users = len(user_data)
    observed = [group_1,group_2,group_3,group_4,group_5,group_6]
    chi = chisquare(observed)
    kwargs = {'total_users':total_number_of_users,'group_1':group_1,'group_2':group_2,'group_3':group_3,'group_4':group_4,'group_5':group_5,'group_6':group_6,'chi':chi}

    if chi[1] <0.01:
        logging.info("WARNING SRM detected -- Total Users={total_users}, Group 1 = {group_1}, Group 2 = {group_2}, Group 3 = {group_3}, Group 4 = {group_4}, Group 5 = {group_5}, Group 6 = {group_6}, Chi = {chi}".format(**kwargs))
        return "Warning SRM detected"
    else:
        logging.info("NO SRM -- Total Users={total_users}, Group 1 = {group_1}, Group 2 = {group_2}, Group 3 = {group_3}, Group 4 = {group_4}, Group 5 = {group_5}, Group 6 = {group_6}, Chi = {chi}".format(**kwargs))
        return "No SRM detected"
