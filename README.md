# NYC Traffic Speed API

[![Build Status](https://travis-ci.org/tcufer/nyc_traffic_speed_api.svg?branch=master)](https://travis-ci.org/tcufer/nyc_traffic_speed_api)

Capture Real-time NYC Traffic Speed Data and make it available through API.  

## Description

API is capturing real-time traffic data of NYC from public source. Data is stored in MongoDB and avaliable in a meaningful way with Flask Restful API 
 
Credits to [@miguelgrinberg](https://github.com/miguelgrinberg) for awesome Flask tutorials and examples.
### Data

New York City DOT’s traffic speed detector feed is a free service that allows various user groups (i.e. the general public, private sector, commercial vendors, transportation agencies, researchers, media and others) to download traffic speed information on a regular basis to use in their applications and research efforts. This data feed contains 'real‐time' traffic information from locations where NYCDOT has installed sensors, mostly on major arterials and highways within the City limits. NYCDOT uses this information for emergency response and management.

More: [NYC Open Data, Real-Time Traffic Speed Data](https://data.cityofnewyork.us/Transportation/Real-Time-Traffic-Speed-Data/xsat-x5sa)

[Metadata](https://data.cityofnewyork.us/api/assets/5695AD48-E3BE-4C04-8E26-4170EBC34B55?download=true) 

## Install

### System dependencies:
* Python 2.7
* MongoDB v3.2.1
* virtualenv

### Installation and Python dependencies:

    $ git clone https://github.com/tcufer/nyc_traffic_speed_api.git
    $ cd nyc_traffic_speed_api
    $ virtualenv venv
    $ source venv/bin/activate
    (venv)$ pip install -r requirements.txt

### Unit Tests

To check your installation was successful you can run the unit tests:

    (venv)$ python manage.py test
    test_bad_url_insert_traffic_data (tests.common.test_data_ingestion.TestDataIngestion) ... ok
    test_insert_traffic_data (tests.common.test_data_ingestion.TestDataIngestion) ... ok
    test_bad_auth (tests.resources.test_resources.TestAPI) ... ok
    test_link (tests.resources.test_resources.TestAPI) ... ok
    test_password_auth (tests.resources.test_resources.TestAPI) ... ok
    test_speed (tests.resources.test_resources.TestAPI) ... ok
    
    Name                       Stmts   Miss  Cover   Missing
    --------------------------------------------------------
    common.py                      0      0   100%   
    common/auth.py                13      0   100%   
    common/data_ingestion.py      22      0   100%   
    common/helper.py               8      0   100%   
    common/models.py              32      1    97%   45
    resources.py                  18      0   100%   
    resources/link_data.py        20      0   100%   
    resources/speed_data.py       52      0   100%   
    --------------------------------------------------------
    TOTAL                        165      1    99%   
    ----------------------------------------------------------------------
    Ran 6 tests in 6.998s
    
    OK

The report above presents a summary of the test coverage.
## Examples

    http://localhost:5000/trafficSpeed
    
    http://localhost:5000/trafficSpeed/<int:id>
    
    http://localhost:5000/trafficSpeed/<int:id>/YYYY-MM-DD
    
    http://localhost:5000/trafficLink
    
    http://localhost:5000/trafficLink/<int:id>


## TODOs
Doing it one step at a time :) I appreciate pull requests and any suggestions!

* Pagination
* HTTP Caching
* Token Authentication
