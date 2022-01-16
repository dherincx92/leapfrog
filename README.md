# leapfrog
A simple CLI interface scraping reviews from `https://www.hospitalsafetygrade.org/`


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
