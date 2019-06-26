# This import is redundant on Zapier
import requests


class MediumCrosspost:
    required_fields = [u"title", u"canonicalUrl", u"integrationToken", u"content"]
    query_blacklist = [u"integrationToken"]

    def __init__(self, input_data):
        self._input_data = None
        self._headers = None
        self._user_id = None
        self.input_data = input_data

    @property
    def input_data(self):
        return self._input_data

    @input_data.setter
    def input_data(self, input_data):
        self._input_data = input_data.copy()
        self.check_fields()

        tags = self._input_data.pop(u"tags", None)
        if tags:

            # For some reason, we may get a list containing
            # a single concatenated string
            tags = tags[0] if len(tags) == 1 else tags

            if isinstance(tags, str):
                self._input_data[u"tags"] = tags.split(u",")
            elif not isinstance(tags, list):
                self._input_data[u"tags"] = [tags]

    def check_fields(self):
        for field in self.required_fields:
            if not self.input_data.get(field):
                raise Exception(u"field {} required as input data".format(field))

    @property
    def headers(self):
        if not self._headers:
            self._headers = {
                u"Authorization": " ".join(
                    [u"Bearer", self.input_data.get(u"integrationToken")]
                )
            }

        return self._headers

    @property
    def user_id(self):
        if not self._user_id:
            # pylint: disable=undefined-variable
            response = requests.get(
                u"https://api.medium.com/v1/me", headers=self.headers
            )
            response.raise_for_status()  # in case the call fails
            self._user_id = response.json()[u"data"][u"id"]

        return self._user_id

    @property
    def query_data(self):
        # base values that are needed, but standard
        data = {u"contentFormat": u"html", u"publishStatus": u"draft"}

        # apply all input data
        # override base values, if specified
        for key, val in self.input_data.items():
            if key not in self.query_blacklist:
                data[key] = val

        return data

    def post(self):
        response = requests.post(
            u"https://api.medium.com/v1/users/{}/posts".format(self.user_id),
            headers=self.headers,
            json=self.query_data,
        )
        response.raise_for_status()
        return response.json()


# pylint: disable=invalid-name,undefined-variable
# Zapier has its own way to populate input_data
if "input_data" in locals():
    crosspost = MediumCrosspost(input_data)
    output = crosspost.post()
