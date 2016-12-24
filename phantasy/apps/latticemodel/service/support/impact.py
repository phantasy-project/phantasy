# encoding: UTF-8
#
# Copyright (c) 2015 Facility for Rare Isotope Beams
#

"""
Handlers Module

.. moduleauthor:: Dylan Maxwell <maxwelld@frib.msu.edu>
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import re
import os.path
import logging
import hashlib
import random

from StringIO import StringIO
from datetime import datetime
from tornado.util import ObjectDict
from tornado.gen import coroutine
from tornado.gen import Return
from bson import ObjectId
from phantasy.library.lattice.impact import read_lattice
from phantasy.library.model.impact import build_result


LOGGER = logging.getLogger(__name__)



class ImpactLatticeSupport(object):

    _INITIAL_VERSION = 1

    _TEMPLATE_NAME = "latticemodel/lattice_impact_upload.html"

    def __init__(self, type_, name, handler):
        self.name = name
        self.type = type_
        self.handler = handler
        self.settings = handler.settings
        self.application = handler.application


    @coroutine
    def _create_upload_context(self):
        data = self.application.data
        ctx = ObjectDict()
        ctx.upload_active = True
        ctx.particle_types = yield data.find_particle_types()
        ctx.lattice_types = yield data.find_lattice_types()
        ctx.lattice = ObjectDict(lattice_type=self.type)
        ctx.lattice_autoversion = True
        ctx.errors = ObjectDict()
        raise Return(ctx)


    @coroutine
    def web_form_upload_get(self):
        """Entry point for web (browser) GET requests to upload Lattice.
        """
        ctx = yield self._create_upload_context()
        self._web_send_status(200, ctx)


    @coroutine
    def web_form_upload_post(self):
        """Entry point for web (browser) POST requests to upload Lattice.
        """
        yield self._form_upload_post(self._web_send_status)


    def _web_send_status(self, status, context):
        """Send response for web (browser) client.

        If the Lattice has been successfully created (ie status 201)
        then redirect the client to the new Lattice details.

        :param status: HTTP response status code
        :param context: dictionary response context
        """
        if status == 201:
            # redirect to created resource
            lattice_id = str(context.lattice._id)
            url = self.handler.reverse_url("lattice_details", lattice_id)
            self.handler.redirect(url, status=303)
        else:
            self.handler.set_status(status)
            self.handler.render(self._TEMPLATE_NAME, **context)


    @coroutine
    def rest_form_upload_post(self):
        """Entry point for REST API POST requests to upload Lattice.
        """
        yield self._form_upload_post(self._rest_send_status)


    @coroutine
    def _rest_send_status(self, status, context):
        """Send response for REST API client.

        If the Lattice has been successfully created (ie status 201)
        then respond with JSON containing link to new Lattice details.

        :param status: HTTP response status code
        :param context: dictionary response context
        """
        if status == 201:
            lattice_id = str(context.lattice._id)
            url = self.handler.reverse_url("rest_lattice_by_id", lattice_id)
            self.handler.set_status(status)
            self.handler.write_json({"links":{"replies":url}})
        else:
            self.handler.set_status(status)
            self.handler.write_json({"errors":context.errors})


    @coroutine
    def _form_upload_post(self, send_status):
        """Process the request and create new Lattice resource.

        :param send_status: callback method to signal completion
        """
        data = self.application.data
        ctx = yield self._create_upload_context()

        content_type = self.handler.request.headers["Content-Type"]
        if not content_type.startswith("multipart/form-data;"):
            send_status(415)
            return

        ctx.lattice.particle_type = self.handler.get_argument("particle_type", "")
        if len(ctx.lattice.particle_type) == 0:
            ctx.errors.particle_type = "Particle Type is required"
        else:
            for p in ctx.particle_types:
                if p["type"] == ctx.lattice.particle_type:
                    particle_type = ObjectDict(p)
                    break
            else:
                ctx.errors.particle_type = "Particle Type '{}' is invalid" \
                                             .format(ctx.lattice.particle_type)

        ctx.lattice.name = self.handler.get_argument("name", "")
        if len(ctx.lattice.name) == 0:
            ctx.errors.name = "Name is required"

        ctx.lattice.branch = self.handler.get_argument("branch", "")
        if len(ctx.lattice.branch) == 0:
            ctx.errors.branch = "Branch is required"

        if self.handler.get_argument("autoversion", "off") == "on":
            ctx.lattice_autoversion = True
        else:
            ctx.lattice_autoversion = False

        ctx.lattice.version = self.handler.get_argument("version", "")
        if not ctx.lattice_autoversion:
            if len(ctx.lattice.version) == 0:
                ctx.errors.version = "Version is required"
            else:
                try:
                    ctx.lattice.version = int(ctx.lattice.version)
                except ValueError:
                    ctx.lattice.version = self._INITIAL_VERSION
                    ctx.errors.version = "Version must be an integer"
                if ctx.lattice.version <= 0:
                    ctx.errors.version = "Version must be greater than zero"

        ctx.lattice.description = self.handler.get_argument("description", "")

        ctx.lattice.status_type = self.handler.get_argument("status_type", "")

        ctx.lattice.created_by = self.handler.current_user

        ctx.lattice.created_date = datetime.now()

        ctx.lattice._id = ObjectId()

        request_files = self.handler.request.files

        if "lattice_file" not in request_files:
            ctx.errors.lattice_file = "Lattice File is required"

        elif len(request_files["lattice_file"]) == 0:
            ctx.errors.lattice_file = "Lattice File is required"

        if ctx.errors:
            send_status(400, ctx)
            return

        # check for another lattice with name, branch and version
        if ctx.lattice_autoversion:
            lattice = yield data.find_lattice_by_name(ctx.lattice.name,
                                                        ctx.lattice.branch)
        else:
            lattice = yield data.find_lattice_by_name(ctx.lattice.name,
                                    ctx.lattice.branch, ctx.lattice.version)

        if ctx.lattice_autoversion:
            if lattice:
                ctx.lattice.version = lattice.version + 1
            else:
                ctx.lattice.version = self._INITIAL_VERSION
        else:
            if lattice:
                ctx.errors.version = "Version already exists"

        if ctx.errors:
            send_status(400, ctx)
            return

        lattice_file = request_files["lattice_file"][0]

        try:
            lattice = read_lattice(StringIO(lattice_file.body))
        except Exception as e:
            LOGGER.warning("Error reading lattice: %s", e)
            ctx.errors.lattice_file = "Lattice File invalid format"

        if ctx.errors:
            send_status(400, ctx)
            return

        ctx.lattice.properties = []

        ctx.lattice.properties.append(dict(
            name="ParticleMass",
            value=lattice.particleMass,
            unit="MeV/c^2"
        ))

        ctx.lattice.properties.append(dict(
            name="ParticleCount",
            value=lattice.nparticles
        ))

        ctx.lattice.properties.append(dict(
            name="ParticleCurrent",
            value=lattice.current,
            unit="A"
        ))

        ctx.lattice.properties.append(dict(
            name="PositionMismatch",
            value=lattice.mismatch
        ))

        ctx.lattice.properties.append(dict(
            name="EnergyMismatch",
            value=lattice.emismatch
        ))

        ctx.lattice.properties.append(dict(
            name="PositionOffset",
            value=lattice.offset
        ))

        ctx.lattice.properties.append(dict(
            name="EnergyOffset",
            value=lattice.eoffset
        ))

        ctx.lattice.properties.append(dict(
            name="DistSigma",
            value=lattice.distSigma
        ))

        ctx.lattice.properties.append(dict(
            name="DistLambda",
            value=lattice.distLambda
        ))

        ctx.lattice.properties.append(dict(
            name="DistMu",
            value=lattice.distMu
        ))

        ctx.lattice.properties.append(dict(
            name="OutputMode",
            value=lattice.outputMode
        ))

        ctx.lattice.properties.append(dict(
            name="IntegratorType",
            value=lattice.integrator
        ))

        nucleons = particle_type.protons + particle_type.neutrons

        # lattice charge states
        if isinstance(lattice.charge, (tuple, list)):
            lattice_charge = []
            for charge in lattice.charge:
                lattice_charge.append(int(charge * lattice.particleMass * nucleons))
        else:
            lattice_charge = int(lattice.charge * lattice.particleMass * nucleons)

        ctx.lattice.properties.append(dict(
            name="ParticleCharge",
            value=lattice_charge
        ))

        ctx.lattice.files = []
        file_content = {}

        file_id = _create_file_id()
        ctx.lattice.files.append(ObjectDict(
            id=file_id,
            name="LatticeFile",
            size=len(lattice_file.body),
            filename=lattice_file.filename,
            location=_create_file_location(lattice_file)
        ))
        file_content[file_id] = lattice_file.body

        for data_file in request_files.get("data_file", []):
            # find a unique file ID
            while True:
                file_id=_create_file_id()
                if file_id not in file_content:
                    break
            ctx.lattice.files.append(ObjectDict(
                id=file_id,
                name="DataFile",
                size=len(data_file.body),
                filename=data_file.filename,
                location=_create_file_location(data_file)
            ))
            file_content[file_id] = data_file.body

        # check that all the data files specified by the
        # lattice have been submitted as attachments
        for filename in lattice.files:
            for f in ctx.lattice.files:
                if f.filename == filename:
                    break
            else:
                ctx.errors.data_file = "Missing data file: " + filename
                send_status(400, ctx)
                return

        attachment_path = self.settings.get("attachment_path", "")
        if len(attachment_path) == 0:
            LOGGER.warn("setting 'attachment_path' not found")
            ctx.errors._global = "Attachment directory not specified"
            send_status(500, ctx)
            return

        if not os.path.isdir(attachment_path):
            LOGGER.error("attachment path '%s' not found", attachment_path)
            ctx.errors._global = "Attachment directory not found"
            send_status(500, ctx)
            return

        try:
            yield data.validate_lattice(ctx.lattice)
        except Exception as e:
            LOGGER.error("lattice validation error: %s", e)
            ctx.errors._global = "Lattice validation error"
            send_status(500, ctx)
            return

        lattice_elements = []
        for idx, element in enumerate(lattice.elements):
            lattice_element = ObjectDict()
            lattice_element.lattice_id = ctx.lattice._id
            lattice_element.order = idx+1
            lattice_element.name = element.name
            lattice_element.type = element.etype
            lattice_element.length = element.length
            lattice_element.position = element.position
            lattice_element.properties = []
            lattice_element.properties.append(dict(
                name="ITYPE",
                value=element.itype
            ))
            lattice_element.properties.append(dict(
                name="STEPS",
                value=element.steps
            ))
            for field in element.fields:
                lattice_element.properties.append(dict(
                    name = field.name,
                    unit = field.unit,
                    value = element.getfield(field.name)
                ))

            try:
                yield data.validate_lattice_element(lattice_element)
            except Exception as e:
                LOGGER.error("lattice element validation error: %s", e)
                ctx.errors._global = "Lattice element validation error"
                send_status(500, ctx)
                return

            lattice_elements.append(lattice_element)

        try:
            lattice_id = yield data.insert_lattice(ctx.lattice, validate=False)
        except Exception as e:
            LOGGER.error("lattice database insert error: %s", e)
            ctx.errors._global = "Lattice database insert error"
            send_status(500, ctx)
            return

        try:
            for lattice_element in lattice_elements:
                lattice_element.lattice_id = lattice_id
                data.insert_lattice_element(lattice_element, validate=False)
        except Exception as e:
            LOGGER.error("lattice element database insert error: %s", e)
            ctx.errors._global = "Lattice element database insert error"
            # Rollback?
            send_status(500, ctx)
            return

        try:
            for f in ctx.lattice.files:
                _write_file_content(attachment_path, f.location, file_content[f.id])
        except Exception as e:
            LOGGER.exception("lattice file write error: %s", e)
            ctx.errors._global = "Lattice file write error"
            #Rollback?
            send_status(500, ctx)
            return

        send_status(201, ctx)
        return



class ImpactModelSupport(object):

    _TEMPLATE_NAME = "latticemodel/model_impact_upload.html"

    def __init__(self, model_type, model_name, handler):
        self.model_name = model_name
        self.model_type = model_type
        self.handler = handler
        self.settings = handler.settings
        self.application = handler.application


    @coroutine
    def _create_upload_context(self):
        data = self.application.data
        ctx = ObjectDict()
        ctx.upload_active = True
        ctx.particle_types, ctx.model_types, ctx.lattices = yield [
            data.find_particle_types(), data.find_model_types(), data.find_lattices()
        ]
        ctx.model = ObjectDict(model_type=self.model_type)
        ctx.errors = ObjectDict()
        raise Return(ctx)


    @coroutine
    def web_form_upload_get(self):
        """Entry point for web (browser) GET requests to upload Model.
        """
        ctx = yield self._create_upload_context()
        self._web_send_status(200, ctx)


    @coroutine
    def web_form_upload_post(self):
        """Entry point for web (browser) POST request to upload Model.
        """
        yield self._form_upload_post(self._web_send_status)


    def _web_send_status(self, status_code, context):
        """Send response for web (browser) client

        If the Model has been successfully created (ie status 201)
        then redirect the client to the new Model details.

        :param status: HTTP response status code
        :param context: dictionary response context
        """
        if status_code == 201:
            # redirect to created resource
            model_id = str(context.model._id)
            url = self.handler.reverse_url("model_details", model_id)
            self.handler.redirect(url, status=303)
        else:
            self.handler.set_status(status_code)
            self.handler.render(self._TEMPLATE_NAME, **context)


    @coroutine
    def rest_form_upload_post(self):
        """Entry point for REST API POST requests to upload Model.
        """
        yield self._form_upload_post(self._rest_send_status)


    @coroutine
    def _rest_send_status(self, status_code, context):
        """Send response for REST API client.

        If the Model has been successfully created (ie status 201)
        then respond with JSON containing link to new Model details.

        :param status: HTTP response status code
        :param context: dictionary response context
        """
        if status_code == 201:
            model_id = str(context.model._id)
            url = self.handler.reverse_url("rest_model_by_id", model_id)
            self.handler.set_status(status_code)
            self.handler.write_json({"links":{"replies":url}})
        else:
            self.handler.set_status(status_code)
            self.handler.write_json({"errors":context.errors})


    @coroutine
    def _form_upload_post(self, send_status):
        """Process the POST request and create new Model resource from form data.

        :param send_status: callback method to signal completion
        """
        import time
        data = self.application.data
        ctx = yield self._create_upload_context()
        now = time.clock()

        content_type = self.handler.request.headers["Content-Type"]
        if not content_type.startswith("multipart/form-data;"):
            send_status(415, ctx)
            return

        ctx.model["lattice_id"] = self.handler.get_argument("lattice_id", "")
        if len(ctx.model["lattice_id"]) == 0:
            ctx.errors["lattice_id"] = "Lattice is required"
        else:
            ctx.model["lattice_id"] = ObjectId(ctx.model["lattice_id"])
            for lattice in ctx.lattices:
                if lattice._id == ctx.model["lattice_id"]:
                    break
            else:
                ctx.errors["lattice_id"] = "Lattice not found"

        ctx.model.name = self.handler.get_argument("name", "")
        if len(ctx.model.name) == 0:
            ctx.errors.name = "Name is required"

        ctx.model.description = self.handler.get_argument("description", "")

        ctx.model.status_type = self.handler.get_argument("status_type", "")

        ctx.model.created_by = self.handler.current_user

        ctx.model.created_date = datetime.now()

        ctx.model._id = ObjectId()

        ctx.model.files = []

        file_content = {}

        request_files = self.handler.request.files

        modelfiles = {
            "fort18":"model_fort18",
            "fort24":"model_fort24",
            "fort25":"model_fort25",
            "fort26":"model_fort26"
        }

        modelargs = {}

        for key, name in modelfiles.iteritems():
            if name in request_files and len(request_files[name]) > 0:
                modelargs[key] = StringIO(request_files[name][0].body)
                # find a unique file ID
                while True:
                    file_id=_create_file_id()
                    if file_id not in file_content:
                        break
                ctx.model.files.append(ObjectDict(
                    id=file_id,
                    name="ModelData",
                    size=len(request_files[name][0].body),
                    filename=request_files[name][0].filename,
                    location=_create_file_location(request_files[name][0])
                ))
                file_content[file_id] = request_files[name][0].body
            else:
                ctx.errors[name] = "Model data file is required"

        if ctx.errors:
            send_status(400, ctx)
            return

        for p in lattice.properties:
            if p.name == "OutputMode":
                outputMode = p.value
                break
        else:
            ctx.errors.lattice_id = "Lattice missing 'OutputMode' property"
            send_status(400, ctx)
            return

        if outputMode not in [1, 2, 3, 4, 5, 6]:
            ctx.errors.lattice_id = "Lattice 'OutputMode' unsupported"
            send_status(400, ctx)
            return

        try:
            model = build_result(**modelargs)
        except Exception as e:
            LOGGER.warning("Error building model: %s", e)
            ctx.errors._global = "Model invalid format"
            send_status(400, ctx)
            return

        ctx.model.properties = []

        if "attachments" in request_files:
            for attachment_file in request_files["attachments"]:
                while True:
                    file_id=_create_file_id()
                    if file_id not in file_content:
                        break
                ctx.model.files.append(ObjectDict(
                    id=file_id,
                    name="Attachment",
                    size=len(attachment_file.body),
                    filename=attachment_file.filename,
                    location=_create_file_location(attachment_file)
                ))
                file_content[file_id] = attachment_file.body


        attachment_path = self.settings.get("attachment_path", "")
        if len(attachment_path) == 0:
            LOGGER.warn("setting 'attachment_path' not found")
            ctx.errors._global = "Attachment directory not specified"
            send_status(500, ctx)
            return


        try:
            yield data.validate_model(ctx.model)
        except Exception as e:
            LOGGER.error("model validation error: %s", e)
            ctx.errors._global = "Model validation error"
            send_status(500, ctx)
            return

        idx = -1
        if outputMode in [1, 2]:
            # First line of data file is initial
            # values BEFORE the first element.
            idx = 0

        model_elements = []

        lattice_elements = yield data.find_lattice_elements_by_lattice_id(
                                                        ctx.model.lattice_id)

        for lattice_element in lattice_elements:

            for p in lattice_element.properties:
                if p.name == "ITYPE":
                    elem_itype =  p.value
                    break
            else:
                ctx.errors._global = ("Lattice Element ({}) missing ITYPE property"
                                                    .format(lattice_element.order))
                send_status(400, ctx)
                return

            for p in lattice_element.properties:
                if p.name == "STEPS":
                    elem_steps =  p.value
                    break
            else:
                ctx.errors._global = ("Lattice Element ({}) missing STEPS property"
                                                    .format(lattice_element.order))
                send_status(400, ctx)
                return

            if outputMode in [1, 2]:
                loop = elem_steps
                if elem_itype in [ -2, 4 ]:
                    # no output for these elements
                    loop = 0
                elif elem_itype < 0:
                    loop = elem_steps + 1
            elif outputMode in [3, 4]:
                loop = 0
                if elem_itype == -28:
                    # only output from monitor
                    loop = 1
            elif outputMode in [5, 6]:
                loop = 1

            for _ in range(loop):

                idx += 1

                try:
                    model_element = ObjectDict()
                    model_element._id = ObjectId()
                    model_element.order = idx+1
                    model_element.model_id = ctx.model._id
                    model_element.lattice_element_id = lattice_element._id
                    model_element.position = model.getSPosition(idx)
                    model_element.properties = []
                    model_element.properties.append(dict(
                        name="BeamCenterX",
                        value=model.getOrbit("X", idx),
                        unit="mm"
                    ))
                    model_element.properties.append(dict(
                        name="BeamCenterY",
                        value=model.getOrbit("Y", idx),
                        unit="mm"
                    ))
                    model_element.properties.append(dict(
                        name="BeamEnergy",
                        value=model.getEnergy(idx),
                        unit="eV"
                    ))
                    model_element.properties.append(dict(
                        name="BeamMomentumCenterX",
                        value=model.getBeamMomentumCentroid("X", idx),
                        unit="rad"
                    ))
                    model_element.properties.append(dict(
                        name="BeamMomentumCenterY",
                        value=model.getBeamMomentumCentroid("Y", idx),
                        unit="rad"
                    ))
                    model_element.properties.append(dict(
                        name="BeamMomentumCenterZ",
                        value=model.getBeamMomentumCentroid("Z", idx),
                        unit="MeV"
                    ))
                    model_element.properties.append(dict(
                        name="BeamRMSX",
                        value=model.getBeamRms("X", idx),
                        unit="mm"
                    ))
                    model_element.properties.append(dict(
                        name="BeamRMSY",
                        value=model.getBeamRms("Y", idx),
                        unit="mm"
                    ))
                    model_element.properties.append(dict(
                        name="BeamRMSZ",
                        value=model.getBeamRms("Z", idx),
                        unit="deg"
                    ))
                    model_element.properties.append(dict(
                        name="BeamMomentumRMSX",
                        value=model.getMomentumRms("X", idx),
                        unit="rad"
                    ))
                    model_element.properties.append(dict(
                        name="BeamMomentumRMSY",
                        value=model.getMomentumRms("Y", idx),
                        unit="rad"
                    ))
                    model_element.properties.append(dict(
                        name="BeamMomentumRMSZ",
                        value=model.getMomentumRms("Z", idx),
                        unit="MeV"
                    ))
                    model_element.properties.append(dict(
                        name="EmittanceX",
                        value=model.getEmittance("X", idx),
                        unit="m-rad"
                    ))
                    model_element.properties.append(dict(
                        name="EmittanceY",
                        value=model.getEmittance("Y", idx),
                        unit="m-rad"
                    ))
                    model_element.properties.append(dict(
                        name="EmittanceZ",
                        value=model.getEmittance("Z", idx),
                        unit="m-rad"
                    ))
                    model_element.properties.append(dict(
                        name="TwissBetaX",
                        value=model.getTwissBeta("X", idx),
                        unit=""
                    ))
                    model_element.properties.append(dict(
                        name="TwissBetaY",
                        value=model.getTwissBeta("Y", idx),
                        unit=""
                    ))
                    model_element.properties.append(dict(
                        name="TwissBetaZ",
                        value=model.getTwissBeta("Z", idx),
                        unit=""
                    ))
                    model_element.properties.append(dict(
                        name="TwissAlphaX",
                        value=model.getTwissAlpha("X", idx),
                        unit=""
                    ))
                    model_element.properties.append(dict(
                        name="TwissAlphaY",
                        value=model.getTwissAlpha("Y", idx),
                        unit=""
                    ))
                    model_element.properties.append(dict(
                        name="TwissAlphaZ",
                        value=model.getTwissAlpha("Z", idx),
                        unit=""
                    ))
                except IndexError:
                    ctx.errors._global = ("Model data not found at index: {}".format(idx))
                    send_status(400, ctx)
                    return

                try:
                    data.validate_model_element(model_element)
                except:
                    LOGGER.exception("model element validation error: %s", e)
                    ctx.errors._global = "Model Element validation error"
                    send_status(500, ctx)
                    return

                model_elements.append(model_element)

        try:
            yield data.insert_model(ctx.model, validate=False)
        except Exception as e:
            LOGGER.error("lattice database insert error: %s", e)
            ctx.errors._global = "Lattice database insert error"
            send_status(500, ctx)
            return


        try:
            for model_element in model_elements:
                #lattice_element.lattice_id = lattice_id
                data.insert_model_element(model_element, validate=False)
        except Exception as e:
            LOGGER.error("model element database insert error: %s", e)
            ctx.errors._global = "Mattice element database insert error"
            # Rollback?
            send_status(500, ctx)
            return


        try:
            for f in ctx.model.files:
                _write_file_content(attachment_path, f.location, file_content[f.id])
        except Exception as e:
            LOGGER.error("model attachment write error: %s", e)
            ctx.errors._global = "Model attachment write error"
            #Rollback?
            send_status(500, ctx)
            return

        LOGGER.debug("model processing complete: %ss", (time.clock() - now))

        send_status(201, ctx)
        return




def _create_file_id():
    return ''.join([ random.choice("abcdef0123456789") for _ in range(6) ])


def _create_file_location(request_file):
    digest = hashlib.md5(request_file.body).hexdigest()
    filename = re.sub(r"[^\.\-\(\)\w]", "", request_file.filename)
    return "{}_{}".format(digest, filename)


def _write_file_content(base_path, location, content):
    filename = os.path.join(base_path, location)
    if not os.path.exists(filename):
        with open(filename, 'w') as attfile:
            attfile.write(content)
