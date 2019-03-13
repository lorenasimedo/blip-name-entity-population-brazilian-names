import logging

from names.get_names import GetNames
from blip_population.set_name_entity_values import BlipPopulation

logging.basicConfig(
    format='%(asctime)s | %(levelname)s | %(message)s', level=logging.DEBUG)


def main():

    logging.warning("Starting the population")

    gn = GetNames()
    gn.get_names_list()
    bp = BlipPopulation()
    bp.populate(gn.names)
    entities = bp.list_entities()
    ("Entities: {}".format(entities))


if __name__ == "__main__":
    main()
