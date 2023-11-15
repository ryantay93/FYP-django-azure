from django import template

from collaborative_filtering.recommender import *

register = template.Library()

@register.simple_tag
def admin_force_gen_tag():
    try:
        gen_similarity_matrix()
        return("Matrices generated!")
    except:
        return("Operation failed!")

@register.simple_tag
def buyer_recommendations_tag():
    #gen_similarity_matrix() # Only if you want to regenerate matrix everytime recommendations are viewed
    results = make_prediction() # list of [target, similarity threshold(0.3), how many similar reviewers(10), how many top products]
    #printout = []
    prodlist = []
    for i in range(len(results)):
        print("Predicted", results[i][0], "rating", results[i][1], "as", results[i][2])
        #printout.append("Predicted {0} rating {1} as {2}".format(results[i][0], results[i][1], results[i][2]))
        prodlist.append(results[i][1])
    #return printout
        