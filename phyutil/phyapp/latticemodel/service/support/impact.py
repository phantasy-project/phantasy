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

import os.path
import logging
import hashlib
import traceback

from StringIO import StringIO
from datetime import datetime
from tornado.util import ObjectDict
from tornado.web import HTTPError
from tornado.gen import coroutine
from tornado.gen import Return
from bson import ObjectId
from phyutil.phylib.lattice.impact import read_lattice
from phyutil.phylib.model.impact import build_result


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


    def _create_file_attachment(self, request_file):
        digest = hashlib.md5(request_file.body).hexdigest()
        location = "{}_{}".format(digest, request_file.filename)
        return ObjectDict(content=request_file.body, location=location)


    def _write_file_attachment(self, file_attachment, base_path):
        filename = os.path.join(base_path, file_attachment.location)
        if not os.path.exists(filename):
            with open(filename, 'w') as attfile:
                attfile.write(file_attachment.content)


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

        files = self.handler.request.files

        if "lattice_file" not in files:
            ctx.errors.lattice_file = "Lattice File is required"

        elif len(files["lattice_file"]) == 0:
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

        lattice_file = files["lattice_file"][0]

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
            name="RefParticleMass",
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
            name="mismatch",
            value=lattice.mismatch
        ))

        ctx.lattice.properties.append(dict(
            name="emismatch",
            value=lattice.emismatch
        ))

        ctx.lattice.properties.append(dict(
            name="offset",
            value=lattice.offset
        ))

        ctx.lattice.properties.append(dict(
            name="eoffset",
            value=lattice.eoffset
        ))

        ctx.lattice.properties.append(dict(
            name="sigma",
            value=lattice.distSigma
        ))

        ctx.lattice.properties.append(dict(
            name="lambda",
            value=lattice.distLambda
        ))

        ctx.lattice.properties.append(dict(
            name="mu",
            value=lattice.distMu
        ))

        nucleons = particle_type.protons + particle_type.neutrons

        # lattice charge states
        if isinstance(lattice.charge, (tuple, list)):
            lattice_charge = []
            for charge in lattice.charge:
                lattice_charge.append(int(charge * lattice.particleMass * nucleons))
        else:
            lattice_charge = int(lattice.charge * lattice.particleMass * nucleons)
        ctx.lattice.properties.append(dict(name="ParticleCharge",value=lattice_charge))

        pending_attachments = []
        ctx.lattice.files = []

        attachment = self._create_file_attachment(lattice_file)
        pending_attachments.append(attachment)
        ctx.lattice.files.append(dict(
            _id=ObjectId(),
            name="LatticeFile",
            filename=lattice_file.filename,
            location=attachment.location
        ))

        if "attachments" in files:
            for attachment_file in files["attachments"]:
                attachment = self._create_file_attachment(attachment_file)
                pending_attachments.append(attachment)
                ctx.lattice.files.append(dict(
                    _id=ObjectId(),
                    name="Attachment",
                    filename=attachment_file.filename,
                    location=attachment.location
                ))

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
            for attachment in pending_attachments:
                self._write_file_attachment(attachment, attachment_path)
        except Exception as e:
            LOGGER.error("lattice attachment write error: %s", e)
            ctx.errors._global = "Lattice attachment write error"
            #Rollback?
            send_status(500, ctx)
            return

        send_status(201, ctx)
        return



class ImpactModelSupport(object):

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
    def get_upload(self):
        ctx = yield self._create_upload_context()
        self.handler.render("latticemodel/model_impact_upload.html", ctx)


    @coroutine
    def post_upload(self):
        content_type = self.handler.request.headers["Content-Type"]
        if not content_type.startswith("multipart/form-data;"):
            raise HTTPError(415)

        ctx = yield self._create_upload_context()

        ctx.model["lattice_id"] = self.handler.get_argument("lattice_id", "")
        if len(ctx.model["lattice_id"]) == 0:
            ctx.errors["lattice_id"] = "Lattice is required"
        else:
            ctx.model["lattice_id"] = ObjectId(ctx.model["lattice_id"])
            for l in ctx.lattices:
                if l["_id"] == ctx.model["lattice_id"]:
                    break
            else:
                ctx.errors["lattice_id"] = "Lattice not found"

        ctx.model.name = self.handler.get_argument("name", "")
        if len(ctx.model.name) == 0:
            ctx.errors.name = "Name is required"

        ctx.model.description = self.handler.get_argument("description", "")

        #ctx.lattice.status_type = self.handler.get_argument("status_type", "")

        ctx.model.created_by = self.handler.current_user

        ctx.model.created_date = datetime.now()

        ctx.model._id = ObjectId()

        ctx.model.files = []

        pending_attachments = []

        files = self.handler.request.files
 
        modelfiles = {
            "fort18":"model_fort18",
            "fort24":"model_fort24",
            "fort25":"model_fort25",
            "fort26":"model_fort26",
            "modelmap":"model_map"
        }
 
        modelargs = {}

        for key, name in modelfiles.iteritems():
            if name in files and len(files[name]) > 0:
                modelargs[key] = StringIO(files[name][0].body)
                attachment = _create_file_attachment(files[name][0])
                pending_attachments.append(attachment)
                ctx.model.files.append(dict(
                    _id=ObjectId(),
                    name="ModelData",
                    filename=files[name][0].filename,
                    location=attachment.location
                ))
            else:
                ctx.errors[name] = "Model data file is required"

        if ctx.errors:
            self.handler.set_status(400)
            self.handler.render("latticemodel/model_impact_upload.html", ctx)
            return

        try:
            model = build_result(**modelargs)
        except Exception as e:
            LOGGER.warning("Error building model: %s", e)
            ctx.errors._global = "Model invalid format"
            self.handler.set_status(400)
            self.handler.render("latticemodel/model_impact_upload.html", ctx)
            return

        ctx.model.properties = []

        if "attachments" in files:
            for attachment_file in files["attachments"]:
                attachment = _create_file_attachment(attachment_file)
                pending_attachments.append(attachment)
                ctx.model.files.append(dict(
                    _id=ObjectId(),
                    name="Attachment",
                    filename=attachment_file.filename,
                    location=attachment.location
                ))

        attachment_path = self.settings.get("attachment_path", "")
        if len(attachment_path) == 0:
            self.handler.set_status(500)
            LOGGER.warn("setting 'attachment_path' not found")
            ctx.errors._global = "Attachment directory not specified"
            self.handler.render("latticemodel/model_impact_upload.html", ctx)
            return
#

        data = self.application.data

        try:
            yield data.validate_model(ctx.model)
        except Exception as e:
            self.handler.set_status(500)
            LOGGER.error("model validation error: %s", e)
            ctx.errors._global = "Model validation error"
            self.handler.render("latticemodel/model_impact_upload.html", ctx)
            return

        model_elements = []

        for name, order_dict in model._modelmap.iteritems():
            
            for order, indexes in order_dict.iteritems():
                lattice_element = yield data.find_lattice_element_by_name(ctx.model.lattice_id, name, order)

                if not lattice_element:
                    return

                idx = indexes[-1]

                model_element = ObjectDict()
                model_element._id = ObjectId()
                model_element.model_id = ctx.model._id
                model_element.lattice_element_id = lattice_element._id
                #print(type(model.getSPosition(idx)))
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
                    name="BeamMomentumRMSY",
                    value=model.getBeamRms("Y", idx),
                    unit="mm"
                ))
                model_element.properties.append(dict(
                    name="BeamRMSZ",
                    value=model.getBeamRms("Z", idx),
                    unit="MeV"
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

                try:
                    data.validate_model_element(model_element)
                except:
                    return

                model_elements.append(model_element)


        try:
            model_id = yield data.insert_model(ctx.model, validate=False)
        except Exception as e:
            self.handler.set_status(500)
            LOGGER.error("lattice database insert error: %s", e)
            ctx.errors._global = "Lattice database insert error"
            self.handler.render("latticemodel/model_impact_upload.html", ctx)
            return


        try:
            for model_element in model_elements:
                #lattice_element.lattice_id = lattice_id
                data.insert_model_element(model_element, validate=False)
        except Exception as e:
            LOGGER.error("model element database insert error: %s", e)
            ctx.errors._global = "Mattice element database insert error"
            # Rollback?
            self.handler.set_status(500)
            self.handler.render("latticemodel/model_impact_upload.html", ctx)
            return

        try:
            for attachment in pending_attachments:
                _write_file_attachment(attachment, attachment_path)
        except Exception as e:
            self.handler.set_status(500)
            LOGGER.error("model attachment write error: %s", e)
            ctx.errors._global = "Model attachment write error"
            #Rollback?
            self.handler.render("latticemodel/model_impact_upload.html", ctx)
            return

        self.handler.redirect(self.handler.reverse_url("model_details", str(model_id)))
        return




def _create_file_attachment(request_file):
    digest = hashlib.md5(request_file.body).hexdigest()
    location = "{}_{}".format(digest, request_file.filename)
    return ObjectDict(content=request_file.body, location=location)


def _write_file_attachment(file_attachment, base_path): 
    filename = os.path.join(base_path, file_attachment.location)
    if not os.path.exists(filename):
        with open(filename, 'w') as attfile:
            attfile.write(file_attachment.content)

