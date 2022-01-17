# leapfrog
A simple CLI interface hospital grades from `https://www.hospitalsafetygrade.org/`

### Development

If you wish to develop or improve this repository, use the following workflow:

```
$ git clone https://github.com/dherincx92/leapfrog.git
$ cd leapfrog
$ python3 -m venv venv
$ source venv/bin/activate
$ (venv) pip install -e .
```

### Usage
This simple, yet dynamic interface allows users to scrape reviews from Leapfrog by using the `scrape` command. Users can indicate whether they want scraping results by city, zip code, hospital name, or state. For supporting documentation on the `scrape` command, run `leapfrog scrape --help`. Examples:

```
# scraping reviews for the zip code: 90280
$ leapfrog scrape zip -z 90280 -o {file-path-for-output}

# returning a single review from the state of CA (-t used for testing results and will only return 1 review)
$ leapfrog scrape state -s CA -o {file-path-for-output} -t True

```


### Data Format

The data will be dumped as a JSON file to a specified directory (pending TODO)

```
[
  {
    'distance': '39.868766455952',
    'grade': 'c',
    'lat': '33.5610516',
    'lon': '-117.6654654',
    'name': 'Providence Mission Hospital Mission Viejo',
    'slug': 'providence-mission-hospital-mission-viejo',
    'address': '27700 Medical Center Road\nMission Viejo, CA 92691-6426'
  },
  {
    'distance': '39.923588963069',
    'grade': 'b',
    'lat': '34.2892065',
    'lon': '-118.745137',
    'name': 'Adventist Health Simi Valley',
    'slug': 'adventist-health-simi-valley',
    'address': '2975 N. Sycamore Drive\nSimi Valley, CA 93065-1201'
  }
]
```
