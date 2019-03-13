import logging
import os
import requests
import uuid
import simplejson as json

logging.basicConfig(
    format='%(asctime)s | %(levelname)s | %(message)s', level=logging.DEBUG)


class BlipPopulation:
    def __init__(self):
        self.blip_url = os.environ['BLIP_URL']
        self.blip_key = os.environ['BLIP_KEY']

    def format_names(self, names):
        values = []
        for n in names:
            value = {
                "name": n,
                "synonymous": []
            }
            values.append(value)
        resource = {
            "name": "Nome",
            "values": values
        }
        return resource

    def list_entities(self):
        '''Return all the entities in case of success
        and None otherwise'''
        request = None
        try:
            request = requests.post(
                url=self.blip_url,
                headers={
                    "Authorization": "Key {}".format(self.blip_key),
                    "Content-Type": "application/json; charset=utf-8",
                },
                data=json.dumps(
                    {
                        "id": str(uuid.uuid1()),
                        "to": "postmaster@ai.msging.net",
                        "method": "get",
                        "uri": "/entities"
                    }
                )
            )
        except Exception as e:
            logging.error(e)
            raise Exception("Exception while migrating")
        if "resource" in request.json():
            return request.json().get("resource").get("items")
        else:
            logging.warning(str(request.json()))
            raise Exception("Error in BLiP while migrating")

    def get_entity(self, entitie_id):
        '''Get a entitie by it`s entitie_id. Return None in case of fail.'''
        request = None
        try:
            request = requests.post(
                url=self.blip_url,
                headers={
                    "Authorization": "Key " + self.blip_key,
                    "Content-Type": "application/json; charset=utf-8",
                },
                data=json.dumps(
                    {
                        "id": str(uuid.uuid1()),
                        "to": "postmaster@ai.msging.net",
                        "method": "get",
                        "uri": "/entities/" + entitie_id
                    }
                )
            )
        except Exception as e:
            logging.error(e)
            raise Exception("Exception while populating")
        if "resource" in request.json():
            return request.json().get("resource").get("items")
        else:
            return None

    def set_entity(self, entity):
        '''Create a new entity. Return the id in case of succes and
        None otherwise'''
        request = None
        try:
            request = requests.post(
                url=self.blip_url,
                headers={
                    "Authorization": "Key " + self.blip_key,
                    "Content-Type": "application/json; charset=utf-8",
                },
                data=json.dumps(
                    {
                        "id": str(uuid.uuid1()),
                        "to": "postmaster@ai.msging.net",
                        "method": "set",
                        "uri": "/entities",
                        "type": "application/vnd.iris.ai.entity+json",
                        "resource": entity
                    }
                )
            )
        except Exception as e:
            logging.error(e)
            raise Exception("Exception while populating")
        if ("status" not in request.json() or
                request.json().get("status") != "success"):
            logging.warning(str(request.json()))
            raise Exception("Error in BLiP while populating")
        else:
            return request.json().get("resource").get("id")

    def delete_entity(self, entity_id):
        '''Delete a entity with entity_id. Return True in case of succes
        and False otherwise'''
        request = None
        try:
            request = requests.post(
                url=self.blip_url,
                headers={
                    "Authorization": "Key " + self.blip_key,
                    "Content-Type": "application/json; charset=utf-8",
                },
                data=json.dumps(
                    {
                        "id": str(uuid.uuid1()),
                        "to": "postmaster@ai.msging.net",
                        "method": "delete",
                        "uri": "/entities" + entity_id
                    }
                )
            )
        except Exception as e:
            logging.error(e)
            raise Exception("Exception while migrating")
        if ("status" not in request.json() or
                request.json().get("status") != "success"):
            logging.warning(str(request.json()))
            raise Exception("Error in BLiP while migrating")
        else:
            return True

    def train_model(self):
        '''Train model.
        Returns true in case of success and false otherwise'''
        request = None
        try:
            request = requests.post(
                url=self.blip_url,
                headers={
                    "Authorization": "Key " + self.blip_key,
                    "Content-Type": "application/json; charset=utf-8",
                },
                data=json.dumps(
                    {
                        "id": str(uuid.uuid1()),
                        "to": "postmaster@ai.msging.net",
                        "method": "set",
                        "uri": "/models",
                        "type": "application/vnd.iris.ai.model-training+json",
                        "resource": {
                        }
                    }
                )
            )
        except Exception as e:
            logging.error(e)
            raise Exception("Exception while populating")
        if ("status" not in request.json() or
                request.json().get("status") != "success"):
            logging.warning(str(request.json()))
            raise Exception("Error in BLiP while populating")
        request = None
        try:
            request = requests.post(
                url=self.blip_source_url,
                headers={
                    "Authorization": "Key " + self.blip_source_key,
                    "Content-Type": "application/json; charset=utf-8",
                },
                data=json.dumps(
                    {
                        "id": str(uuid.uuid1()),
                        "to": "postmaster@ai.msging.net",
                        "method": "get",
                        "uri": "/models"
                    }
                )
            )
        except Exception as e:
            logging.error(e)
            raise Exception("Exception while populating")
        if ("status" not in request.json() or
                request.json().get("status") != "success"):
            logging.warning(str(request.json()))
            raise Exception("Error in BLiP while populating")
        if ("resource" not in request.json()):
            logging.warning(str(request.json()))
            raise Exception("Error in BLiP while populating")
        ids = []
        for i in request.json().get("resource").get("items"):
            ids.append(i.get("id"))
        return ids

    def publish_model(self, ids):
        '''Publish models with the given ids.
        Returns true in case of success and false otherwise'''
        for i in ids:
            request = None
            try:
                request = requests.post(
                    url=self.blip_url,
                    headers={
                        "Authorization": "Key " + self.blip_key,
                        "Content-Type": "application/json; charset=utf-8",
                    },
                    data=json.dumps(
                        {
                            "id": str(uuid.uuid1()),
                            "to": "postmaster@ai.msging.net",
                            "method": "set",
                            "uri": "/models",
                            "type": ("application/vnd.iris.ai.model"
                                     "-publishing+json"),
                            "resource": {
                                "id": i
                            }
                        }
                    )
                )
            except Exception as e:
                logging.error(e)
                raise Exception("Exception while populating")
            if request.json().get("status") != "success":
                logging.warning(str(request.json()))
                raise Exception("Error in BLiP while populating")
        return True

    def populate(self, names_list):

        # Deleting old entity
        names = self.format_names(names_list)
        logging.info(names)
        if self.get_entity("nome") is not None:
            self.delete_entity("nome")
        valid = self.set_entity(names)
        if not valid:
            logging.error("Error while creating the entitie")

        # Training
        ids = self.train_model()
        if ids is None:
            logging.error("Error while training the model")
        else:
            # Publishing
            valid = self.publish_model(ids)
            if not valid:
                logging.error("Error while publishing the models")
