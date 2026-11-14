from xobis.tests.fixtures import connection


def test_obis_view(connection):

    count = connection.sql("SELECT count(*) FROM obis").fetchall()[0][0]
    assert count > 30000000, "Too few entries for an obis database"
