# NYC Traffic Speed API

Storing Real-time NYC Traffic Speed Data in MongoDB and making it available for querying.  

## Description
 
### Data

New York City DOT’s traffic speed detector feed is a free service that allows various user groups (i.e. the general public, private sector, commercial vendors, transportation agencies, researchers, media and others) to download traffic speed information on a regular basis to use in their applications and research efforts. This data feed contains 'real‐time' traffic information from locations where NYCDOT has installed sensors, mostly on major arterials and highways within the City limits. NYCDOT uses this information for emergency response and management.

More: [NYC Open Data, Real-Time Traffic Speed Data](https://data.cityofnewyork.us/Transportation/Real-Time-Traffic-Speed-Data/xsat-x5sa)

[Metadata](https://data.cityofnewyork.us/api/assets/5695AD48-E3BE-4C04-8E26-4170EBC34B55?download=true) 

## Install

### System dependencies:
* Python 2.7
* MongoDB v3.0

### Python dependencies:
```
pip install -r requirements.txt
```

## Examples

```
http://localhost:5000/trafficSpeed
```
 
```
http://localhost:5000/trafficSpeed/<int:id>
```

```
http://localhost:5000/trafficLink
```

```
http://localhost:5000/trafficLink/<int:id>
```

### Sample output (JSON)
``` json
{
  "speedSensor": [
    {
      "borough": "Manhattan", 
      "dataAsOf": "Wed, 21 Oct 2015 12:52:36 GMT", 
      "linkName": "11th ave n ganservoort - 12th ave @ 40th st", 
      "sensorId": "1", 
      "speed": "8.08", 
      "travelTime": "647"
    }
  ]
}

```
## TODOs
Doing it one step at a time :) I appriciate any suggestions!

* Separate data about sensors and measured data in DB
* Add more options for querying
* Expand code coverage for unit tests
* Develop separate api client for data monitoring, visualizations,...   