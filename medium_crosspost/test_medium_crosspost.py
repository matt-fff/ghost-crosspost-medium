from unittest import TestCase
import mock
from .medium_crosspost import MediumCrosspost


class TestMediumCrosspost(TestCase):
    test_data = {
        u"title": u"test-title",
        u"canonicalUrl": u"http://www.example.com/test-url",
        u"integrationToken": u"golly, some token",
        u"content": u"<html><head></head><body>test html from ghost</body></html>",
        u"tags": u"python,testing,tag-stubs",
    }

    processed_test_data = {
        u"title": u"test-title",
        u"canonicalUrl": u"http://www.example.com/test-url",
        u"integrationToken": u"golly, some token",
        u"content": "<html><head></head><body>test html from ghost</body></html>",
        u"tags": [u"python", u"testing", u"tag-stubs"],
    }

    expected_headers = {u"Authorization": u"Bearer golly, some token"}

    # pylint: disable=protected-access
    def test_init(self):
        crosspost = MediumCrosspost(self.test_data)
        self.assertIsNone(crosspost._headers)
        self.assertIsNone(crosspost._user_id)
        self.assertDictEqual(self.processed_test_data, crosspost.input_data)

    def test_input_data(self):
        crosspost = MediumCrosspost(self.test_data)

        test_data = self.test_data.copy()
        processed_test_data = self.processed_test_data.copy()

        # Practically speaking, this line should do nothing
        crosspost.input_data = test_data
        self.assertDictEqual(processed_test_data, crosspost.input_data)

        test_data[u"tags"] = None
        processed_test_data.pop(u"tags")
        crosspost.input_data = test_data
        self.assertDictEqual(processed_test_data, crosspost.input_data)

        test_data[u"tags"] = ""
        crosspost.input_data = test_data
        self.assertDictEqual(processed_test_data, crosspost.input_data)

        test_data[u"tags"] = u"just-one"
        processed_test_data[u"tags"] = [u"just-one"]
        crosspost.input_data = test_data
        self.assertDictEqual(processed_test_data, crosspost.input_data)

    # pylint: disable=protected-access,broad-except
    def test_check_fields(self):
        crosspost = MediumCrosspost(self.test_data)

        # Check the standard case where all is well
        crosspost._input_data = self.processed_test_data
        crosspost.check_fields()

        # Make sure that missing any required field triggers and exception
        for field in MediumCrosspost.required_fields:
            processed_test_data = self.processed_test_data.copy()
            processed_test_data.pop(field)

            crosspost._input_data = processed_test_data

            try:
                crosspost.check_fields()
                self.fail(u"expected exception failed to trigger")
            except Exception as exc:
                self.assertIn(
                    u"field {} required as input data".format(field), str(exc)
                )

    def test_headers(self):
        crosspost = MediumCrosspost(self.test_data)
        self.assertDictEqual(self.expected_headers, crosspost.headers)

    @mock.patch("medium_crosspost.medium_crosspost.requests")
    def test_user_id(self, mock_requests):
        expected_user_id = u"asfu9sabd9324g729v8asf867saf82389f92gftest"

        # Set up the mocks
        mock_response = mock.MagicMock()
        mock_response.json.return_value = {
            u"data": {
                u"id": expected_user_id,
                u"username": u"testusername",
                u"name": u"testname",
                u"url": u"https://medium.com/@testusername",
                u"imageUrl": u"https://cdn-images-1.medium.com/fit/c/400/400/1*239ug3429gfb23.png",
            }
        }
        mock_requests.get.return_value = mock_response

        crosspost = MediumCrosspost(self.test_data)
        self.assertEqual(expected_user_id, crosspost.user_id)

        # Check that the Medium route got called
        mock_requests.get.assert_called_once()
        mock_requests.get.assert_has_calls(
            [mock.call(u"https://api.medium.com/v1/me", headers=self.expected_headers)]
        )
        mock_response.raise_for_status.assert_called_once()

        # Check that subsequent calls don't trigger a new request
        _ = crosspost.user_id
        mock_requests.get.assert_called_once()
        mock_response.raise_for_status.assert_called_once()

    def test_query_data(self):
        crosspost = MediumCrosspost(self.test_data)
        crosspost._input_data = {u"integrationToken": u"skipped"}

        self.assertDictEqual(
            {u"contentFormat": u"html", u"publishStatus": u"draft"},
            crosspost.query_data,
        )

        crosspost._input_data = {
            u"integrationToken": u"skipped",
            u"other": u"keys",
            u"and": True,
            u"stuff": [],
        }
        self.assertDictEqual(
            {
                u"contentFormat": u"html",
                u"publishStatus": u"draft",
                u"other": u"keys",
                u"and": True,
                u"stuff": [],
            },
            crosspost.query_data,
        )

        crosspost._input_data = {
            u"integrationToken": u"skipped",
            u"other": u"keys",
            u"and": True,
            u"stuff": [],
            u"contentFormat": u"override",
        }
        self.assertDictEqual(
            {
                u"contentFormat": u"override",
                u"publishStatus": u"draft",
                u"other": u"keys",
                u"and": True,
                u"stuff": [],
            },
            crosspost.query_data,
        )

    @mock.patch(
        "medium_crosspost.medium_crosspost.MediumCrosspost.query_data",
        new_callable=mock.PropertyMock,
    )
    @mock.patch("medium_crosspost.medium_crosspost.requests")
    def test_post(self, mock_requests, mock_query_data):
        expected_user_id = u"asfu9sabd9324g729v8asf867saf82389f92gftest"
        expected_post_id = u"239rasdfs8hfb9asdftest"

        # Set up the mocks
        mock_response = mock.MagicMock()
        mock_response.json.return_value = {
            u"data": {
                u"id": expected_post_id,
                u"title": self.processed_test_data[u"title"],
                u"authorId": expected_user_id,
                u"url": u"https://medium.com/@testusername/{}".format(expected_post_id),
                u"canonicalUrl": self.processed_test_data[u"canonicalUrl"],
                u"publishStatus": u"draft",
                u"license": "",
                u"licenseUrl": u"https://medium.com/policy/9db0094a1e0f",
                u"tags": self.processed_test_data[u"tags"],
            }
        }
        mock_requests.post.return_value = mock_response
        mock_query_data.return_value = {
            u"contentFormat": u"html",
            u"publishStatus": u"draft",
        }

        crosspost = MediumCrosspost(self.test_data)
        crosspost._user_id = expected_user_id

        self.assertDictEqual(mock_response.json.return_value, crosspost.post())

        # Check that the Medium route got called
        mock_requests.post.assert_called_once()
        mock_requests.post.assert_has_calls(
            [
                mock.call(
                    u"https://api.medium.com/v1/users/{}/posts".format(
                        expected_user_id
                    ),
                    headers=self.expected_headers,
                    json=mock_query_data.return_value,
                )
            ]
        )
        mock_response.raise_for_status.assert_called_once()
