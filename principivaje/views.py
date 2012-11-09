# -*- coding: utf-8 -*-
from pyramid.view import view_config
from deform import (
    Form,
    Button,
    ValidationFailure
)

from .schemes import (
    SchemaNevronskaMreza,
    SchemaDeltaAlgorithm
)

from neuralnetwork import Nevronska_mreza
from delta_algorithm import DeltaLearning

from colander import Invalid as colander_invalid


def get_resources(request, form=None):
    js_links_basics = ['deform_bootstrap:static/bootstrap.min.js']
    css_links_basics = ['deform_bootstrap:static/deform_bootstrap.css']
    if form is None:
        js_links = js_links_basics
        css_links = css_links_basics
    else:
        resources = form.get_widget_resources()
        js_resources = resources['js']
        css_resources = resources['css']
        js_links = ['deform:static/%s' % r for r in js_resources]
        js_links = ['deform_bootstrap:static/jquery-1.7.1.min.js',
                    'deform_bootstrap:static/jquery-ui-1.8.18.custom.min.js',
                    'deform_bootstrap:static/jquery.maskedinput-1.3.js'
                    ] + js_links_basics + js_links \
                    + ['deform_bootstrap:static/deform_bootstrap.js']
        css_links = ['deform:static/%s' % r for r in css_resources]
        css_links = css_links_basics + [
            'deform_bootstrap:static/jquery_chosen/chosen.css'] + css_links
    js_tags = ['<script type="text/javascript" src="%s"></script>' % link
               for link in map(request.static_url, js_links)]
    css_tags = ['<link rel="stylesheet" href="%s"/>' % link
                for link in map(request.static_url, css_links)]
    return js_tags, css_tags


def validator(form, value):
    if len(value['vhod']) != len(value['zeleni_izhod']):
        exc = colander_invalid(
            form, u'Vhod in Želeni izhod morata imeti enako število vrstic!')
        exc['vhod'] = u"Nima enako število vrstic kot želeni izhod!"
        exc['zeleni_izhod'] = u"Nima enako število vrstic kot vhod!"
        raise exc
    if "utezi" in value and len(value['vhod']) > 0:
        len_vhod = len(value['vhod'][0]) + 1
        len_utezi = len(value['utezi'])
        if len_vhod != len_utezi:
            exc = colander_invalid(
                form, u'Število uteži mora biti za eno več kot vhodov')
            exc['vhod'] = u"Posamezen vhod mora imeti za eno manj vrednosti kot uteži"
            exc['utezi'] = u"Utež mora imeto eno več vrednosti kot posamezen vhod"
            raise exc


@view_config(route_name='home', renderer='neural_network.mako')
@view_config(route_name='mlp', renderer='neural_network.mako')
def my_view(request):
    schema = SchemaNevronskaMreza(validator=validator)
    myform = Form(schema, buttons=('submit',))
    js_tags, css_tags = get_resources(request, myform)
    result = {'title': u"Nevronska mreža", "js_tags": js_tags,
              "css_tags": css_tags, "neural": True}
    appstruct = {'utezi_prvi_nivo': [
        (0, 0.2, -0.2, 0),
        (0, 0.1, 0, 0.5),
        (0, -0.3, 0, 0.4)
    ],
        'utezi_drugi_nivo': [
            (0, 0.5, -0.5, 0),
            (0, 0, -0.3, 0.8),
        ],
        'vhod': [
            (0, 0.4, -0.2),
            (0.3, -0.1, 0.5)
        ],
        'zeleni_izhod': [
            (0, 1),
            (1, 0)
        ]
    }
    if 'submit' in request.POST:
        controls = request.POST.items()
        try:
            appstruct = myform.validate(controls)
            #print appstruct
            nn = Nevronska_mreza(appstruct["eta"], appstruct["vhod"],
                                 appstruct["zeleni_izhod"],
                                 appstruct["utezi_prvi_nivo"],
                                 appstruct["utezi_drugi_nivo"],
                                 appstruct["utez_i"],
                                 appstruct["utez_j"],
                                 appstruct["utez_l"])
            nn.run()
            result["tabela"] = nn.tabela
            result["text_izhod"] = nn.text_izhod
        except ValidationFailure, e:
            result['form'] = e.render()
            return result
        except Exception, e:
            request.ext.flash_error(unicode(e), title="Napaka pri podatkih")
            result["form"] = myform.render(appstruct=appstruct)
            return result
        result["form"] = myform.render(appstruct=appstruct)
        return result
    # We are a GET not a POST
    result["form"] = myform.render(appstruct=appstruct)
    return result


@view_config(route_name='changes', renderer='changes.mako')
def changes(request):
    js_tags, css_tags = get_resources(request)
    result = {'title': u"Changelog", "js_tags": js_tags, "css_tags": css_tags}
    return result


@view_config(route_name='delta', renderer='neural_network.mako')
def delta_view(request):
    schema = SchemaDeltaAlgorithm(validator=validator)
    myform = Form(schema, buttons=('submit',))
    js_tags, css_tags = get_resources(request, myform)
    result = {'title': u"Učno pravilo delta", "js_tags": js_tags,
              "css_tags": css_tags, "delta": True}
    appstruct = {
        'utezi': [0.1, -0.1, 0.5],
        'vhod': [
            (0.7, 0.4),
            (0.3, 0.8)
        ],
        'zeleni_izhod': [
            (0.0,),
            (1.0,)
        ]
    }
    if 'submit' in request.POST:
        controls = request.POST.items()
        try:
            appstruct = myform.validate(controls)
            #print appstruct
            nn = DeltaLearning(appstruct['utezi'],
                               appstruct["vhod"],
                               appstruct["zeleni_izhod"],
                               appstruct["eta"],
                               epoch_learning=appstruct["paketno_ucenje"]
                               )
            nn.run()
            result["tabela"] = nn.table
            result["text_izhod"] = nn.text_output
            #print appstruct
        except ValidationFailure, e:
            result['form'] = e.render()
            return result
        except Exception, e:
            #print e
            request.ext.flash_error(unicode(e), title="Napaka pri podatkih")
            result["form"] = myform.render(appstruct=appstruct)
            return result
        result["form"] = myform.render(appstruct=appstruct)
        return result
    # We are a GET not a POST
    result["form"] = myform.render(appstruct=appstruct)
    return result
