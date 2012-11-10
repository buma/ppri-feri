# -*- coding: utf-8 -*-
import colander
import deform


class SchemaRowZeleniIzhod(colander.TupleSchema):
    n_0 = colander.SchemaNode(colander.Float(), validator=colander.Range(0, 1))
    n_1 = colander.SchemaNode(colander.Float(), validator=colander.Range(0, 1))


class SchemaRowsZeleniIzhod(colander.SequenceSchema):
    row = SchemaRowZeleniIzhod()


class SchemaRowZeleniIzhodDelta(colander.TupleSchema):
    n_0 = colander.SchemaNode(colander.Float(), validator=colander.Range(0, 1))


class SchemaRowsZeleniIzhodDelta(colander.SequenceSchema):
    row = SchemaRowZeleniIzhodDelta()


class SchemaRowVhod(colander.TupleSchema):
    n_0 = colander.SchemaNode(
        colander.Float(), validator=colander.Range(-1, 1))
    n_1 = colander.SchemaNode(
        colander.Float(), validator=colander.Range(-1, 1))
    n_2 = colander.SchemaNode(
        colander.Float(), validator=colander.Range(-1, 1))


class SchemaRowsVhod(colander.SequenceSchema):
    row = SchemaRowVhod()


class SchemaRowUtez1(colander.TupleSchema):
    n_0 = colander.SchemaNode(
        colander.Float(), validator=colander.Range(-1, 1))
    n_1 = colander.SchemaNode(
        colander.Float(), validator=colander.Range(-1, 1))
    n_2 = colander.SchemaNode(
        colander.Float(), validator=colander.Range(-1, 1))
    n_3 = colander.SchemaNode(
        colander.Float(), validator=colander.Range(-1, 1))


class SchemaRowsUtez1(colander.SequenceSchema):
    row = SchemaRowUtez1()


class SchemaRowUtez2(colander.TupleSchema):
    n_0 = colander.SchemaNode(
        colander.Float(), validator=colander.Range(-1, 1))
    n_1 = colander.SchemaNode(
        colander.Float(), validator=colander.Range(-1, 1))
    n_2 = colander.SchemaNode(
        colander.Float(), validator=colander.Range(-1, 1))
    n_3 = colander.SchemaNode(
        colander.Float(), validator=colander.Range(-1, 1))


class SchemaRowsUtez2(colander.SequenceSchema):
    row = SchemaRowUtez2()


class SchemaNevronskaMreza(colander.MappingSchema):

    eta = colander.SchemaNode(colander.Float(),
                              validator=colander.Range(0, 1),
                              default=0.3,
                              description="Hitrost učenja")

    vhod = SchemaRowsVhod(description="Vhodne vrednosti brez biasa")
    zeleni_izhod = SchemaRowsZeleniIzhod(
        description=u"Kakšen bi moral biti izhod nevronske mreže",
        title=u"Želeni izhod"
    )

    utezi_prvi_nivo = SchemaRowsUtez1(validator=colander.Length(1, 3),
                                      widget=deform.widget.SequenceWidget(
                                      min_len=1,
                                      max_len=3),
                                      title=u"Uteži prvi nivo"
                                      )

    utezi_drugi_nivo = SchemaRowsUtez2(validator=colander.Length(1, 2),
                                       widget=deform.widget.SequenceWidget(
                                       min_len=1,
                                       max_len=2
                                       ),
                                       title=u"Uteži prvi nivo")

    utez_i = colander.SchemaNode(colander.Int(),
                                 validator=colander.Range(1, 3),
                                 default=1,
                                 description=u"w_i,j^(l) i koordinata uteži")
    utez_j = colander.SchemaNode(colander.Int(),
                                 colander=colander.Range(1, 3),
                                 default=2,
                                 description=u"w_i,j^(l) j koordinata uteži")
    utez_l = colander.SchemaNode(colander.Int(),
                                 colander=colander.Range(1, 2),
                                 default=1,
                                 description=u"w_i,j^(l) l koordinata uteži")


class SchemaRowInputDelta(colander.SequenceSchema):
    x = colander.SchemaNode(
        colander.Float(), validator=colander.Range(-1, 1))


class SchemaRowsInputDelta(colander.SequenceSchema):
    row = SchemaRowInputDelta(widget=deform.widget.TextInputCSVWidget())


class SchemaRowWeightHop(colander.SequenceSchema):
    x = colander.SchemaNode(
        colander.Int(), validator=colander.Range(-1, 1))


class SchemaRowsWeightHop(colander.SequenceSchema):
    row = SchemaRowWeightHop(widget=deform.widget.TextInputCSVWidget())


def validate_delta_input(node, value):
    """Validates inputs and makes sure that all inputs
    have the same number of inputs"""
# we get length of all inputs
    lens = map(len, value)
    all_same = all(lens[0] == input_len for input_len in lens)
    #print lens
    #print all_same
    if not all_same:
        raise colander.Invalid(node,
                               u"Vsi vhodi nimajo enakega števila elementov")
    return True


class SchemaDeltaAlgorithm(colander.MappingSchema):

    eta = colander.SchemaNode(colander.Float(),
                              validator=colander.Range(0, 1),
                              default=0.5,
                              description="Hitrost učenja")

    paketno_ucenje = colander.SchemaNode(colander.Bool(),
                                         default=True)

    neurons = (
        ('', '- Select -'),
        ('logistic', u'Logistična'),
        #('linear', 'Linearna'),
        #('step', u'Stopničasta'),
        ('tlu', 'TLU'),
    )
    neuron_type = colander.SchemaNode(colander.String(),
                                      default='logistic',
                                      #default='tlu',
                                      widget=deform.widget.SelectWidget(
                                          values=neurons)
                                      )
    learning_error_values = (
        ('', '- Select -'),
        ('mse', 'MSE'),
        ('cee', 'CEE')
    )
    learning_error = colander.SchemaNode(colander.String(),
                                         default='cee',
                                         #default='mse',
                                         widget=deform.widget.SelectWidget(
                                         values=learning_error_values)
                                         )
    vhod = SchemaRowsInputDelta(description="Vhodne vrednosti brez biasa",
                                validator=validate_delta_input)
    zeleni_izhod = SchemaRowsZeleniIzhodDelta(
        description=u"Kakšen bi moral biti izhod nevrona",
        title=u"Želeni izhod"
    )

    utezi = SchemaRowInputDelta(widget=deform.widget.TextInputCSVWidget(),
                                title=u"Uteži")


class SchemaHopfield(colander.MappingSchema):
    utez = SchemaRowsWeightHop(description=u"Utežna matrika W",
                               validator=validate_delta_input)
    functions = (
        (0, u'Funkcija 1'),
        #('linear', 'Linearna'),
        #('step', u'Stopničasta'),
        (1, 'Funkcija 2'),
    )
    function_type = colander.SchemaNode(colander.Int(),
                                        default=0,
                                        #default='tlu',
                                        validator=colander.OneOf(
                                        [x[0] for x in functions]),
                                        widget=deform.widget.SelectWidget(
                                        values=functions),
                                        title=u"Osveževalna funkcija"
                                        )
