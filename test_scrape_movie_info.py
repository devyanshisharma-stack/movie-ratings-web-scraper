import unittest
import os
import scraping
import json
import pprint


class TestScrapeMovieInfo(unittest.TestCase):
    def run_test(self, slug, case_name, dump_diff=False):
        expected_fname = os.path.join(
            "scrapes", f"{case_name}_movies_info.json"
        )
        try:
            res = scraping.scrape_movie_info(slug)
        except Exception as e:
            self.fail(f"Unexpected Exception raised: {e}")
        res_json = json.dumps(res, sort_keys=True)
        with open(expected_fname, "r") as expected_file:
            expected_json = expected_file.read()
        res_json = res_json.strip()
        expected_json = expected_json.strip()

        expected_pprint = pprint.pformat(expected_json)
        res_pprint = pprint.pformat(res_json)

        # Read both from string
        # if we didn't do that then ints in expected would be read as strings
        res = json.loads(res_json)
        expected = json.loads(res_json)

        err_msg = f'ERROR: scrape_move_info("{slug}")\n gave wrong output.'
        if dump_diff:
            err_msg += "\nexpected:\n{expected_pprint}\nactual:\n{res_pprint}"

        self.assertEqual(expected, res, err_msg)

    def test_tiny_movie_info(self):
        url = "https://www.cis.upenn.edu/~cis110/movies/tiny_movies/"
        case_name = "tiny"
        self.run_test(url, case_name, dump_diff=True)

    # This test takes about two seconds to run!
    # Leave it commented until you pass the one that
    # comes before it.

    def test_small_movie_info(self):
        url = "https://www.cis.upenn.edu/~cis110/movies/small_movies/"
        case_name = "small"
        self.run_test(url, case_name, dump_diff=True)
