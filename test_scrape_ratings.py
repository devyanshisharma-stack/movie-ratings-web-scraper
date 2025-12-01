import unittest
import os
import scraping
import json
import pprint


class TestScrapeRatings(unittest.TestCase):
    def run_test(self, slug, ids_fname, case_name, dump_diff=False):
        expected_fname = os.path.join("scrapes", f"{case_name}_movies.json")
        try:
            ids = set()
            with open(ids_fname, "r") as f:
                ids = set(
                    f.read().replace("{", "").replace("}", "").split(", ")
                )
                ids = set(map(int, ids))
            res = scraping.scrape_ratings(slug, ids)
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

        err_msg = f'ERROR: scrape_ratings("{slug}")\n gave wrong output.'
        if dump_diff:
            err_msg += "\n\ninput movie_ids:{ids}\nexpected:\n{expected_pprint}\nactual:\n{res_pprint}"

        self.assertEqual(expected, res, err_msg)

    def test_tiny_ratings(self):
        url = "https://www.cis.upenn.edu/~cis110/movies/tiny_movies/"
        ids_fname = os.path.join("scrapes", "tiny_movies_ids.txt")
        case_name = "tiny"
        self.run_test(url, ids_fname, case_name, dump_diff=True)

    # This test takes about 10 seconds to run!
    # Leave it commented until you pass the one that
    # comes before it.

    def test_small_ratings(self):
        url = "https://www.cis.upenn.edu/~cis110/movies/small_movies/"
        ids_fname = os.path.join("scrapes", "small_movies_ids.txt")
        case_name = "small"
        self.run_test(url, ids_fname, case_name, dump_diff=True)
