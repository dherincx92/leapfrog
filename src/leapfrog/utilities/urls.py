
SEARCH_PARAMETERS = [
    'findBy',
    'zip_code',
    'radius' # only appears when searching for zip
    'city',
    'state_prov',
    'hospital',
]

class URL:
    def __init__(self, domain, params):
        self.domain = domain
        self.params = params

    @property
    def separator(self):
        return '&'
