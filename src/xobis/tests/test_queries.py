from xobis.tests.fixtures import connection

DEMO_QUERY = """
    select
        dataset_id, _id as id,
        interpreted.*,
        source.scientificName as originalScientificName,
        flags,
        dropped,
        absence
    from obis
    where interpreted.speciesid = 141433
    and dropped is not true and absence is not true;
"""


def test_source_column_names(connection):
    columns = connection.query("select * from obis").columns
    expected = sorted(
        [
            "_id",
            "_event_id",
            "_occurrence_id",
            "dataset_id",
            "node_ids",
            "source",
            "interpreted",
            "extensions",
            "missing",
            "invalid",
            "flags",
            "dropped",
            "absence",
            "tags",
            "geometry",
        ]
    )
    assert sorted(columns) == expected


def test_demo_query_column_names(connection):
    columns = connection.query(DEMO_QUERY).columns
    assert len(columns) == 282
    ## test some of the more interesting subsets of columns
    # some ids
    assert set(
        [
            "dataset_id",
            "id",
            "datasetID",
            "eventID",
            "identificationID",
            "locationID",
            "institutionID",
            "occurrenceID",
            "orderid",
            "organismID",
            "parentEventID",
            "sectionid",
        ]
    ) <= set(columns)

    # Associations
    assert set(
        [
            "associatedMedia",
            "associatedOccurrences",
            "associatedOrganisms",
            "associatedReferences",
            "associatedSequences",
            "associatedTaxa",
        ]
    ) <= set(columns)

    # Date related
    assert set(
        [
            "dateIdentified",
            "date_end",
            "date_mid",
            "date_start",
            "date_year",
            "day",
            "month",
            "year",
            "endDayOfYear",
            "startDayOfYear",
            "eventDate",
            "eventTime",
            "modified",
        ]
    ) <= set(columns)

    # location
    assert set(
        [
            "areas",
            "coordinatePrecision",
            "coordinateUncertaintyInMeters",
            "country",
            "countryCode",
            "county",
            "decimalLatitude",
            "decimalLongitude",
            "depth",
            "island",
            "islandGroup",
            "kingdom",
            "municipality",
            "shoredistance",
            "stateProvince",
            "waterBody",
            "pointRadiusSpatialFit",
            "locality",
            "locationAccordingTo",
            "locationID",
            "locationRemarks",
            "maximumDepthInMeters",
            "maximumDistanceAboveSurfaceInMeters",
            "maximumElevationInMeters",
            "hab",
            "habitat",
        ]
    ) <= set(columns)

    # species
    assert set(
        [
            "species",
            "speciesid",
            "subclass",
            "subclassid",
            "subdivision",
            "subdivisionid",
            "subfamily",
            "subfamilyid",
            "tribe",
            "tribeid",
            "variety",
            "varietyid",
            "organismID",
            "organismName",
            "organismQuantity",
            "organismQuantityType",
            "organismRemarks",
            "organismScope",
        ]
    ) <= set(columns)

    # verbatim
    assert set(
        [
            "verbatimCoordinateSystem",
            "verbatimCoordinates",
            "verbatimDepth",
            "verbatimElevation",
            "verbatimEventDate",
            "verbatimIdentification",
            "verbatimLabel",
            "verbatimLatitude",
            "verbatimLocality",
            "verbatimLongitude",
            "verbatimSRS",
            "verbatimTaxonRank",
        ]
    ) <= set(columns)

    # special booleans
    assert set(["brackish", "hab", "marine", "wrims", "dropped", "absence"]) <= set(
        columns
    )


def test_demo_query_column_types(connection):
    columns = connection.query(DEMO_QUERY).columns
    dtypes = connection.query(DEMO_QUERY).dtypes
    by_name = dict(zip(columns, dtypes))

    T_VARCHAR = "VARCHAR"
    T_BIGINT = "BIGINT"
    T_DOUBLE = "DOUBLE"
    T_BOOLEAN = "BOOLEAN"

    assert by_name["id"] == T_VARCHAR
    assert by_name["dataset_id"] == T_VARCHAR
    assert by_name["species"] == T_VARCHAR
    assert by_name["decimalLatitude"] == T_DOUBLE
    assert by_name["date_start"] == T_BIGINT
    assert by_name["dropped"] == T_BOOLEAN
