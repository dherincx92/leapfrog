'''
Formats a URL to include query strings

author(s): Derek Herincx, derek663@gmail.com
last_updated: 01/15/2022
'''
from typing import Dict, List, Union

class URL:
    """Generic class that helps create a URL with properly formatted query
    strings.

    Args:
        domain: str
            A URL domain. This includes everything before the query string
            operator, inclusive of the operator itself
        query_dct: dict
            A dictionary containing the domain's query parameters
        keys_to_exlude: list
            A list of keys to be excluded from being included in the final URL
    """
    def __init__(
        self,
        domain: str,
        query_dct: Dict[str, Union[str, int]],
        keys_to_exclude: List[str]
    ) -> "URL":
        self.domain = domain
        self.query_dct = {
            k:v for k,v in query_dct.items() if k not in keys_to_exclude
        }

    def __call__(self) -> str:
        """Shortcut for main method"""
        return self.main()

    @property
    def whitespace_encoding(self) -> str:
        """Character used to encode whitespaces in parameters"""
        return "+"

    @property
    def separator(self) -> str:
        """Ampersand used to separate query parameters in URL"""
        return "&"

    def _create_query_string(self, key: str, value: Union[str, int]) -> str:
        """Creates individual query strings from a single query dictionary
        object
        """
        if value:
            encoded = value.replace(" ", self.whitespace_encoding)
        else:
            encoded = ""
        return f"{key}={encoded}{self.separator}"


    def main(self) -> str:
        """Primary method for generating a complete URL with query string
        parameters.
        """
        query_lst= [
            self._create_query_string(k, v) for k,v in self.query_dct.items()
        ]
        queries_as_string = "".join(query_lst)
        return f"{self.domain}{queries_as_string}"
