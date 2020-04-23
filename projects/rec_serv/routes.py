import os
import json
import string
import random
import logging
import pymongo

from bson.objectid import ObjectId
from flask import Blueprint, send_from_directory, Flask, render_template, request, jsonify, current_app

log = logging.getLogger('tester.sub')

bp_rec_serv = Blueprint( "bp_rec_serv", __name__, 
	template_folder = 'templates', 
	static_url_path = '/static/rec_serv',
	static_folder = 'static')

EXPECTED_PARAMAS = ['assignmentId', 'hitId', 'workerId', 'turkSubmitTo']

NUM_OF_EXPECTED_COMPANIES 	= 5
EXPECTED_COMPANIES       	= ['comp_{}'.format(i) for i in range( 0, NUM_OF_EXPECTED_COMPANIES ) ]
GOLDS 			   		 	= ['g_{}'.format(i) for i in range( 0, NUM_OF_EXPECTED_COMPANIES ) ]
FIRST_LETTER_FOR_GOLD		= 7
first_letters = list( range(10) )
first_letters.remove( FIRST_LETTER_FOR_GOLD )

URL_MONGO = os.environ["URL_MONGO"]

client = pymongo.MongoClient(URL_MONGO)
db     = client.get_default_database()

# def id_generator(size=9, chars=string.ascii_uppercase + string.digits):
# 	return ''.join(random.choice(chars) for _ in range(size))
def id_generator(size=9, chars=string.digits):
	return ''.join(random.choice(chars) for _ in range(size))


@bp_rec_serv.route('/rec_serv', methods = ['GET'] )
def get():

	data = request.args.to_dict()

	current_app.logger.debug( 'GET request received by "rec_serv" endpoint' )
	current_app.logger.debug( '  - data: {}'.format( data ) )

	current_app.logger.debug( EXPECTED_COMPANIES)

	if not all(elem in data.keys() for elem in EXPECTED_COMPANIES):
		return "Error: Invalid request."

	assert all(elem in data.keys() for elem in EXPECTED_COMPANIES), "Some expected companies were not given"

	current_app.logger.debug('Ecco')

	received_companies = [ data[c] for c in EXPECTED_COMPANIES ]

	current_app.logger.debug( received_companies )

	companies = list( db.companies.find( { '_id' : { '$in' : [ ObjectId(c) for c in received_companies   ] } } ) ) 

	current_app.logger.debug( '{} companies found: '.format(companies) )

	if len( companies ) != NUM_OF_EXPECTED_COMPANIES: 
		current_app.logger.debug( "Some companies were not found in the DB.") 
		return "Error: Missing companies."


	for i, company in enumerate( companies ) : 

		company['id_in_db'] = received_companies[i]

		if 'g' in company.keys():

			company['g'] = str(FIRST_LETTER_FOR_GOLD) + company['g']
		else:
			company['g'] = str( random.choice( first_letters)) + id_generator()

	current_app.logger.debug( 'Companies:' )
	for i, company in enumerate(companies):
		current_app.logger.debug( str(i) + ') {} '.format(company['name']) )
		current_app.logger.debug( company )
		current_app.logger.debug( '-------------'  )

	'''
	sample =  	[  	{   
	'country': 'France',
	'country_code': 'fr',
	'full_address': 'M. le Président du Conseil Exécutif  ',
	'locality': None,
	'name': 'COLLECTIVITÉ DE CORSE',
	'opencorporates_id': '/companies/fr/200076958',
	'postcode': None,
	'street_address': 'M. le Président du Conseil Exécutif',
	'g': '4UK000556'
	},{   
	'country': 'France',
	'country_code': 'fr',
	'full_address': '101 rue de Tolbiac Paris 75013',
	'locality': 'Paris',
	'name': 'Unicancer ACHATS',
	'opencorporates_id': '/companies/fr/532834090',
	'postcode': '75013',
	'street_address': '101 rue de Tolbiac',
	'g': '5NC000892'
	}]
	data['companies'] = sample[1:4]
	'''
	
	data['companies'] = companies

	return render_template( 'rec_serv/rec_serv.html', data = data)

@bp_rec_serv.after_request
def after_request(response):

	response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
	response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
	response.headers["Expires"] = 0
	response.headers["Pragma"] = "no-cache"
	return response
