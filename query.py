"""

This file is the place to write solutions for the
practice part of skills-sqlalchemy. Remember to
consult the exercise instructions for more complete
explanations of the assignment.

All classes from model.py are being imported for you
here, so feel free to refer to classes by just their
class name (and not model.ClassName).

"""

from model import *

init_app()

# -------------------------------------------------------------------
# Part 2: SQLAlchemy Queries


# Get the brand with the brand_id of ``ram``.
q1 = db.session.query(Brand).filter(Brand.brand_id == "ram").first()

# Get all models with the name ``Corvette`` and the brand_id ``che``.
q2 = db.session.query(Model).filter(Model.name == "Corvette",
                                    Model.brand_id == "che").all()

# Get all models that are older than 1960.
q3 = db.session.query(Model).filter(Model.year < 1960).all()

# Get all brands that were founded after 1920.
q4 = db.session.query(Brand).filter(Brand.founded > 1920).all()

# Get all models with names that begin with ``Cor``.
q5 = db.session.query(Model).filter(Model.name.like('Cor%')).all()

# Get all brands that were founded in 1903 and that are not yet discontinued.
q6 = db.session.query(Brand).filter(Brand.founded == 1903,
                                    Brand.discontinued.is_(None)).all()

    # The below also works, but Sublime complains about using == or != with None.
    # q6 = db.session.query(Brand).filter(Brand.founded == 1903,
    #                                     Brand.discontinued == None).all()

# Get all brands that are either 1) discontinued (at any time) or 2) founded
# before 1950.
q7 = db.session.query(Brand).filter(db.or_(Brand.founded < 1950,
                                           Brand.discontinued.isnot(None))).all()

    # The below also works, but Sublime complains about using == or != with None.
    # q7 = db.session.query(Brand).filter(db.or_(Brand.founded < 1950,
    #                                     Brand.discontinued != None)).all()

# Get all models whose brand_id is not ``for``.
q8 = db.session.query(Model).filter(Model.brand_id != 'for').all()



# -------------------------------------------------------------------
# Part 3: Write Functions


def get_model_info(year):
    """Takes in a year and prints out each model name, brand name, and brand
    headquarters for that year using only ONE database query."""

    models_by_year = (db.session.query(Model.name,
                                       Brand.name,
                                       Brand.headquarters)
                      .filter(Model.year == year)
                      .join(Brand).all())

    print "\nModels from " + str(year) + ":\n"

    for model, brand, hq in models_by_year:
        print ("Model: " + model + "\n\tBrand: " + brand + "\n\tHQ: " + hq)


def get_brands_summary():
    """Prints out each brand name (once) and all of that brand's models,
    including their year, using only ONE database query."""

    brands = Brand.query.group_by(Brand.brand_id).join(Model).all()

    for brand in brands:
        print brand.name + ":"
        for i in brand.models:
            print "\t" + i.name + " - " + str(i.year)


def search_brands_by_name(mystr):
    """Returns all Brand objects corresponding to brands whose names include
    the given string."""

    brands_w_str = (db.session.query(Brand)
                    .filter(Brand.name.like('%'+mystr+'%'))
                    .all())

    return brands_w_str


def get_models_between(start_year, end_year):
    """Returns all Model objects corresponding to models made between
    start_year (inclusive) and end_year (exclusive)."""

    model_yrs = db.session.query(Model).filter(Model.year > start_year,
                                               Model.year < end_year).all()

    return model_yrs
