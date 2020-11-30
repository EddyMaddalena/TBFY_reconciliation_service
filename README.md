## Company reconciliation Task

#### Requirements

* The task runs in *Flask* app (Python microframework, https://palletsprojects.com/p/flask/) that runs in an *Heroku Dyno* (https://www.heroku.com/dynos).
* Workers are recruited from *Amazon Mechanical Turk (MTurk)* (https://www.mturk.com/). 
* The interaction with the *MTurk* API takes place by *IPython* Notebooks (https://ipython.org/). 
* Companies to be resolved has to be stored in a *MongoDB* instance (this example uses MLab).

Several guides and tutorial are available to use such technologies:
* https://stackabuse.com/deploying-a-flask-application-to-heroku/
* https://docs.aws.amazon.com/AWSMechTurk/latest/AWSMturkAPI/Welcome.html

#### Environment variable
The service requires the following environment variable:

| Variable name | Description | 
|-----|:-----|
| URL_MONGO	| Standard MongoDB URI (https://docs.mlab.com/connecting/#connect-string) of the DB where companies are stored. |
| IAM_USER_ACCESS_KEY |	Amazon ITM Access Key | 
| IAM_USER_SECRET_KEY	| Amazon ITM Secret Key |
| MTURK_REGION_NAME	| us-east-1 |
| URL_MTURK_SANDBOX	| https://mturk-requester-sandbox.us-east-1.amazonaws.com |
| URL_MTURK_PRODUCTION | https://mturk-requester.us-east-1.amazonaws.com |

To know more about IAM have a look at this: https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction.html

#### Input Data and Golden Standard
The companies that require to be resolved has to be stored in a database named **companies** Mongo DB instance in this way: 
```JSON 
{
    "_id": {
        "$oid": "5e4bfc63zzzef924f306bd06"
    },
    "ocid": "ocds-0c46vo-1234-567890-1234",
    "name": "Fancy Company",
    "opencorporates_id": "/companies/fr/200047835",
    "country_code": "fr",
    "full_address": "rue du somewhere, La Rochelle 12345",
    "street_address": "rue du France",
    "locality": "Somewhere in France",
    "postcode": "12345",
    "country": "France",
    "g": "1234567890"
}
```
The attribute **g** has to be present for each company. Companies that are golden standard (the ones for which we already have the opencorporate id and we want to use as indicator of the reliability of the worker) need to have the g attribute starting with the number 7, followed by the *opencorporate id* of the company. For example, the *Fancy Company* is a golden standard company, since the attribute g begins with 7, and after that the expected *opencorporate id*. All the others, not-golden standard companies, have to have the attribute **g** starting by a number different than 7, followed by a few of random digits.
#### Scripts
The folder *ipython* contains two *notebooks*, with some *examples* to use the *reconciliation service*: 
* *HITs-Launcher.ipynb* - Is a script to setup and launch new HITs, based on the list of required companies, the qualification to filter out low-quality workers, and other params, such as, HIT title, description, and amount of payment for resolution.
* *Results Viewer.ipynb* - This script downloads the results of one or more HITS and store them in a Pandas Dataframe  for further analysis. (https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html)


