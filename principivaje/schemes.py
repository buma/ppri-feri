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

    paketno_ucenje = colander.SchemaNode(colander.Bool(),
                                         default=True)

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

    vhod = SchemaRowsInputDelta(description="Vhodne vrednosti brez biasa",
                                validator=validate_delta_input)
    zeleni_izhod = SchemaRowsZeleniIzhodDelta(
        description=u"Kakšen bi moral biti izhod nevrona",
        title=u"Želeni izhod"
    )

    utezi = SchemaRowInputDelta(widget=deform.widget.TextInputCSVWidget())
